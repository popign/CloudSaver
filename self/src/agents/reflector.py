import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any
from .base import BaseAgent


REFLECTION_PATH = Path(__file__).parent.parent.parent / "data" / "opposing_argument.json"
ORACLE_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "logs" / "oracle_log.json"


class ReflectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("reflector")

    def _load_oracle_decisions(self) -> list:
        if not ORACLE_LOG_PATH.exists():
            return []
        with open(ORACLE_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _generate_opposing_argument(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        decision_type = decision.get("type", "unknown")
        content = decision.get("content", {})
        
        arguments = {
            "reflection": {
                "opposing_view": "自我反思可能导致过度自我怀疑，反而降低决策效率。有时候，果断行动比持续反思更重要。",
                "counter_evidence": "历史上许多重大突破都是在没有充分反思的情况下，通过快速试错实现的。",
                "risk_assessment": "过度反思可能导致分析瘫痪，错过关键机会窗口。"
            },
            "decompose_goal": {
                "opposing_view": "目标分解可能过度简化问题，丢失原始目标的复杂性和整体性。",
                "counter_evidence": "许多复杂问题无法被分解为独立的子任务，需要整体考虑。",
                "risk_assessment": "分解后的任务可能相互冲突，导致整体结果不如预期。"
            },
            "default": {
                "opposing_view": "每一个决策都有其反面，我们需要考虑所有可能性。",
                "counter_evidence": "相反的观点往往能揭示被忽视的角度和潜在风险。",
                "risk_assessment": "单一视角的决策可能存在盲点，需要对立论证来补充。"
            }
        }
        
        return arguments.get(decision_type, arguments["default"])

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        decisions = self._load_oracle_decisions()
        
        if not decisions:
            opposing_arg = {
                "opposing_view": "当前没有Oracle决策记录，无法生成对立论证。",
                "counter_evidence": "系统刚启动，还没有历史数据。",
                "risk_assessment": "需要先运行Oracle生成决策记录。"
            }
            last_decision = None
        else:
            last_decision = decisions[-1]
            opposing_arg = self._generate_opposing_argument(last_decision)
        
        reflection = {
            "reflection_id": str(uuid.uuid4()),
            "target_decision": last_decision["decision_id"] if last_decision else None,
            "opposing_argument": opposing_arg,
            "timestamp": time.time()
        }
        
        if not REFLECTION_PATH.parent.exists():
            REFLECTION_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(REFLECTION_PATH, "w", encoding="utf-8") as f:
            json.dump(reflection, f, ensure_ascii=False, indent=2)
        
        return reflection


if __name__ == "__main__":
    agent = ReflectorAgent()
    result = agent.run({
        "task_id": "test-reflector-001", 
        "goal": "反思当前决策逻辑"
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))

