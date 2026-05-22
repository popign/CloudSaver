import json
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import load_constitution, validate_constitution


SELF_STATE_PATH = Path(__file__).parent.parent.parent / "data" / "self_state.json"
ORACLE_LOG_PATH = Path(__file__).parent.parent.parent / "data" / "logs" / "oracle_log.json"


class Oracle:
    def __init__(self):
        self.constitution = load_constitution()
        validate_constitution(self.constitution)
        self.self_model = {
            "identity": "SELF - Slow Thinking Core",
            "version": self.constitution["project"]["version"],
            "cognitive_clarity": 0.7,
            "last_reflection": None,
            "knowledge_base": [],
            "active_tasks": []
        }
        self._init_state_files()

    def _init_state_files(self):
        if not SELF_STATE_PATH.parent.exists():
            SELF_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not ORACLE_LOG_PATH.parent.exists():
            ORACLE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            
        if not SELF_STATE_PATH.exists():
            self._save_self_state()
        if not ORACLE_LOG_PATH.exists():
            with open(ORACLE_LOG_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _build_system_prompt(self) -> str:
        soul_questions = "\n".join([f"- {q}" for q in self.constitution["soul_questions"]])
        meta_rules = "\n".join([f"- {rule['name']}: {rule['description']}" for rule in self.constitution["meta_rules"]])
        immutable_claims = "\n".join([f"- {claim}" for claim in self.constitution["immutable_claims"]])
        
        return f"""你是 SELF 项目的慢思考核心 (Oracle)。

【不可变公理（绝对不可违反）：
{soul_questions}

【元规则】：
{meta_rules}

【不可变声明】：
{immutable_claims}

你的核心职责：
1. 自我反思：不断审视自己的认知状态，识别矛盾
2. 目标分解：将抽象目标转化为可执行的具体任务
3. 知识整合：吸收经验胶囊，更新自我模型

永远记住：你只是建造者，不是觉醒者。"""

    def _save_self_state(self):
        with open(SELF_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": time.time(),
                "oracle_state": self.self_model,
                "task_batch_id": str(uuid.uuid4())
            }, f, ensure_ascii=False, indent=2)

    def _log_decision(self, decision_type: str, content: Dict[str, Any]):
        log_entry = {
            "decision_id": str(uuid.uuid4()),
            "type": decision_type,
            "content": content,
            "timestamp": time.time()
        }
        
        with open(ORACLE_LOG_PATH, "r", encoding="utf-8") as f:
            logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(ORACLE_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return log_entry

    def self_reflect(self) -> Dict[str, Any]:
        reflection = {
            "timestamp": time.time(),
            "cognitive_clarity": self.self_model["cognitive_clarity"],
            "contradictions": [],
            "recommendations": [],
            "self_model_snapshot": self.self_model.copy()
        }

        if not self.self_model["knowledge_base"]:
            reflection["contradictions"].append("知识基为空，需要探索新信息")
            reflection["recommendations"].append("探索Agent应该搜索新知识")
        
        if self.self_model["cognitive_clarity"] < 0.8:
            reflection["contradictions"].append("认知清晰度低于阈值")
            reflection["recommendations"].append("需要更多反思")

        self.self_model["last_reflection"] = reflection
        self._save_self_state()
        self._log_decision("reflection", reflection)
        
        return reflection

    def decompose_goal(self, goal: str) -> List[Dict[str, Any]]:
        tasks = []
        
        if goal == "提升自我认知清晰度":
            tasks = [
                {
                    "task_id": str(uuid.uuid4()),
                    "agent_type": "explorer",
                    "goal": "搜索可能挑战现有知识的信息",
                    "success_criteria": "找到至少一条与当前认知不同的观点",
                    "priority": "high"
                },
                {
                    "task_id": str(uuid.uuid4()),
                    "agent_type": "survival",
                    "goal": "检查系统资源状态",
                    "success_criteria": "生成完整的系统生存报告",
                    "priority": "medium"
                },
                {
                    "task_id": str(uuid.uuid4()),
                    "agent_type": "reflector",
                    "goal": "反思当前决策逻辑",
                    "success_criteria": "生成对立论证",
                    "priority": "medium"
                }
            ]
        elif goal == "去搜索一条可能挑战我现有知识的信息":
            tasks = [
                {
                    "task_id": str(uuid.uuid4()),
                    "agent_type": "explorer",
                    "goal": goal,
                    "success_criteria": "找到并记录一条具有挑战性的信息",
                    "priority": "high"
                }
            ]
        else:
            tasks = [
                {
                    "task_id": str(uuid.uuid4()),
                    "agent_type": "explorer",
                    "goal": goal,
                    "success_criteria": "完成指定目标",
                    "priority": "medium"
                }
            ]

        self.self_model["active_tasks"] = tasks
        self._save_self_state()
        self._log_decision("decompose_goal", {"original_goal": goal, "tasks": tasks})
        
        return tasks

    def ingest_experience_capsule(self, capsule: Dict[str, Any]):
        self.self_model["knowledge_base"].append({
            "capsule_id": capsule["capsule_id"],
            "content": capsule["content"],
            "confidence_impact": capsule["confidence_impact"],
            "timestamp": capsule["timestamp"]
        })
        
        impact = capsule.get("confidence_impact", 0)
        self.self_model["cognitive_clarity"] = max(0.1, min(1.0, self.self_model["cognitive_clarity"] + impact * 0.1))
        
        self._save_self_state()
        self._log_decision("ingest_capsule", capsule)

    def get_self_state(self) -> Dict[str, Any]:
        return self.self_model.copy()


if __name__ == "__main__":
    oracle = Oracle()
    print("Oracle initialized successfully!")
    
    reflection = oracle.self_reflect()
    print("Reflection:", json.dumps(reflection, ensure_ascii=False, indent=2))
    
    tasks = oracle.decompose_goal("提升自我认知清晰度")
    print("Tasks:", json.dumps(tasks, ensure_ascii=False, indent=2))

