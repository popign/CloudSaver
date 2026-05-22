import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any
import requests
from .base import BaseAgent


EXPLORATION_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "exploration_log.json"


class ExplorerAgent(BaseAgent):
    def __init__(self):
        super().__init__("explorer")

    def _mock_search(self, query: str) -> Dict[str, Any]:
        mock_results = {
            "挑战现有知识": {
                "title": "科学范式转换：当旧理论被新证据推翻",
                "snippet": "科学史上充满了范式转换的例子，从地心说到日心说，从牛顿力学到相对论。每一次转换都伴随着激烈的争论和新证据的发现。",
                "url": "https://example.com/science/paradigm-shift",
                "challenging": True,
                "confidence_impact": -0.15
            },
            "人工智能": {
                "title": "AI的未来：通用人工智能是否可能？",
                "snippet": "关于通用人工智能(AGI)的可能性，学术界存在严重分歧。一部分专家认为几十年内就能实现，另一部分则认为这是一个无法企及的目标。",
                "url": "https://example.com/ai/agi-debate",
                "challenging": True,
                "confidence_impact": -0.1
            },
            "default": {
                "title": "探索性搜索结果",
                "snippet": "这是一条模拟的搜索结果，代表了与当前认知可能不同的观点。在真实系统中，这里会接入真实的搜索API。",
                "url": "https://example.com/search/result",
                "challenging": True,
                "confidence_impact": -0.05
            }
        }
        
        for key, result in mock_results.items():
            if key in query:
                return result
        return mock_results["default"]

    def _search_web(self, query: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_html": 1,
                    "skip_disambig": 1
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("Heading", "Search Result"),
                    "snippet": data.get("Abstract", "No abstract available"),
                    "url": data.get("AbstractURL", ""),
                    "challenging": True,
                    "confidence_impact": -0.08
                }
        except Exception:
            pass
        
        return self._mock_search(query)

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        goal = task.get("goal", "探索未知领域")
        
        search_result = self._search_web(goal)
        
        exploration = {
            "exploration_id": str(uuid.uuid4()),
            "query": goal,
            "result": search_result,
            "timestamp": time.time()
        }
        
        if not EXPLORATION_LOG_PATH.parent.exists():
            EXPLORATION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        log_data = []
        if EXPLORATION_LOG_PATH.exists():
            with open(EXPLORATION_LOG_PATH, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        
        log_data.append(exploration)
        
        with open(EXPLORATION_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        return exploration


if __name__ == "__main__":
    agent = ExplorerAgent()
    result = agent.run({
        "task_id": "test-explorer-001", 
        "goal": "搜索可能挑战现有知识的信息"
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))

