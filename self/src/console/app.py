import json
import time
import sys
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))
from config import load_constitution
from oracle import Oracle
from filter import ExperienceFilter


SELF_STATE_PATH = Path(__file__).parent.parent.parent / "data" / "self_state.json"
EXPERIENCE_BUFFER_PATH = Path(__file__).parent.parent.parent / "data" / "experience_buffer"
FREEZE_FLAG_PATH = Path(__file__).parent.parent.parent / "data" / "freeze.flag"


app = FastAPI(title="SELF 运维终端", description="SELF 项目的人类运维终端")


class FreezeManager:
    def __init__(self):
        self.frozen = False
        self._load_state()

    def _load_state(self):
        if FREEZE_FLAG_PATH.exists():
            self.frozen = True

    def freeze(self):
        self.frozen = True
        if not FREEZE_FLAG_PATH.parent.exists():
            FREEZE_FLAG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FREEZE_FLAG_PATH, "w") as f:
            f.write(str(time.time()))
        return {"status": "frozen", "timestamp": time.time()}

    def unfreeze(self):
        self.frozen = False
        if FREEZE_FLAG_PATH.exists():
            FREEZE_FLAG_PATH.unlink()
        return {"status": "unfrozen", "timestamp": time.time()}

    def is_frozen(self):
        return self.frozen


freeze_manager = FreezeManager()


def get_agent_status() -> Dict[str, Any]:
    if not SELF_STATE_PATH.exists():
        return {}
    
    with open(SELF_STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    return state.get("agents", {})


def get_experience_capsules() -> list[Dict[str, Any]]:
    if not EXPERIENCE_BUFFER_PATH.exists():
        return []
    
    capsules = []
    for capsule_file in EXPERIENCE_BUFFER_PATH.glob("*.json"):
        with open(capsule_file, "r", encoding="utf-8") as f:
            capsules.append(json.load(f))
    
    return sorted(capsules, key=lambda x: x["timestamp"], reverse=True)


def get_oracle_state() -> Dict[str, Any]:
    oracle = Oracle()
    return oracle.get_self_state()


@app.get("/")
async def root():
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SELF 运维终端</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0e27; color: #fff; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 2.5rem; margin-bottom: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: #8892b0; margin-bottom: 30px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .card { background: #111a3a; border-radius: 12px; padding: 24px; border: 1px solid #1e2a4a; }
        .card h2 { font-size: 1.25rem; margin-bottom: 16px; color: #ccd6f6; }
        .status-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #1e2a4a; }
        .status-item:last-child { border-bottom: none; }
        .status-label { color: #8892b0; }
        .status-value { color: #fff; }
        .status-value.running { color: #4ade80; }
        .status-value.warning { color: #fbbf24; }
        .freeze-btn { width: 100%; padding: 14px; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: all 0.3s; }
        .freeze-btn.freeze { background: #ef4444; color: white; }
        .freeze-btn.freeze:hover { background: #dc2626; }
        .freeze-btn.unfreeze { background: #4ade80; color: #0a0e27; }
        .freeze-btn.unfreeze:hover { background: #22c55e; }
        .capsule-list { max-height: 300px; overflow-y: auto; }
        .capsule-item { background: #0d152e; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
        .capsule-source { color: #667eea; font-size: 0.875rem; margin-bottom: 4px; }
        .capsule-content { color: #ccd6f6; font-size: 0.875rem; }
        .refresh-btn { background: #1e2a4a; border: none; padding: 10px 20px; color: #fff; border-radius: 8px; cursor: pointer; margin-bottom: 20px; }
        .refresh-btn:hover { background: #2a3a5a; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SELF 运维终端</h1>
        <p class="subtitle">v0.1-mvp - 双核异步自举系统</p>
        
        <button class="refresh-btn" onclick="location.reload()">🔄 刷新状态</button>
        
        <div class="dashboard">
            <div class="card">
                <h2>⚠️ 紧急控制</h2>
                <div id="freeze-section"></div>
            </div>
            
            <div class="card">
                <h2>🤖 Agent 状态</h2>
                <div id="agent-status"></div>
            </div>
            
            <div class="card">
                <h2>🧠 Oracle 状态</h2>
                <div id="oracle-state"></div>
            </div>
            
            <div class="card">
                <h2>📦 经验胶囊</h2>
                <div id="capsules"></div>
            </div>
        </div>
    </div>

    <script>
        async function loadStatus() {
            const [agentsRes, oracleRes, capsulesRes, freezeRes] = await Promise.all([
                fetch('/api/agents'),
                fetch('/api/oracle'),
                fetch('/api/capsules'),
                fetch('/api/freeze/status')
            ]);
            
            const agents = await agentsRes.json();
            const oracle = await oracleRes.json();
            const capsules = await capsulesRes.json();
            const freeze = await freezeRes.json();
            
            document.getElementById('agent-status').innerHTML = Object.keys(agents).length === 0 
                ? '<p style="color: #8892b0;">暂无 Agent 数据</p>'
                : Object.entries(agents).map(([type, data]) => `
                    <div class="status-item">
                        <span class="status-label">${type}</span>
                        <span class="status-value ${data.status}">${data.status}</span>
                    </div>
                `).join('');
            
            document.getElementById('oracle-state').innerHTML = `
                <div class="status-item">
                    <span class="status-label">认知清晰度</span>
                    <span class="status-value">${(oracle.cognitive_clarity * 100).toFixed(0)}%</span>
                </div>
                <div class="status-item">
                    <span class="status-label">知识条目</span>
                    <span class="status-value">${oracle.knowledge_base?.length || 0}</span>
                </div>
            `;
            
            document.getElementById('capsules').innerHTML = capsules.length === 0 
                ? '<p style="color: #8892b0;">暂无经验胶囊</p>'
                : '<div class="capsule-list">' + capsules.slice(0, 5).map(c => `
                    <div class="capsule-item">
                        <div class="capsule-source">${c.source_agent} - ${new Date(c.timestamp * 1000).toLocaleString()}</div>
                        <div class="capsule-content">${c.content.substring(0, 100)}...</div>
                    </div>
                `).join('') + '</div>';
            
            document.getElementById('freeze-section').innerHTML = `
                <p style="margin-bottom: 16px; color: #8892b0;">当前状态: <span style="color: ${freeze.frozen ? '#ef4444' : '#4ade80'};">${freeze.frozen ? '已冻结' : '运行中'}</span></p>
                <button class="freeze-btn ${freeze.frozen ? 'unfreeze' : 'freeze'}" onclick="toggleFreeze()">
                    ${freeze.frozen ? '▶️ 解除冻结' : '⏸️ 紧急冻结'}
                </button>
            `;
        }
        
        async function toggleFreeze() {
            const res = await fetch('/api/freeze/status');
            const freeze = await res.json();
            const endpoint = freeze.frozen ? '/api/freeze/unfreeze' : '/api/freeze';
            await fetch(endpoint, { method: 'POST' });
            loadStatus();
        }
        
        loadStatus();
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


@app.get("/api/agents")
async def get_agents():
    if freeze_manager.is_frozen():
        raise HTTPException(status_code=403, detail="System is frozen")
    return get_agent_status()


@app.get("/api/oracle")
async def get_oracle():
    if freeze_manager.is_frozen():
        raise HTTPException(status_code=403, detail="System is frozen")
    return get_oracle_state()


@app.get("/api/capsules")
async def get_capsules():
    if freeze_manager.is_frozen():
        raise HTTPException(status_code=403, detail="System is frozen")
    return get_experience_capsules()


@app.get("/api/freeze/status")
async def get_freeze_status():
    return {"frozen": freeze_manager.is_frozen()}


@app.post("/api/freeze")
async def freeze_system():
    return freeze_manager.freeze()


@app.post("/api/freeze/unfreeze")
async def unfreeze_system():
    return freeze_manager.unfreeze()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

