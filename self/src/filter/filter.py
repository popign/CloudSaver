import json
import time
import uuid
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import load_constitution


EXPERIENCE_BUFFER_PATH = Path(__file__).parent.parent.parent / "data" / "experience_buffer"


def create_experience_capsule(
    source_agent: str,
    task_id: str,
    content: str,
    confidence_impact: float = 0.0
) -> Dict[str, Any]:
    return {
        "capsule_id": str(uuid.uuid4()),
        "source_agent": source_agent,
        "task_id": task_id,
        "content": content,
        "confidence_impact": confidence_impact,
        "timestamp": time.time(),
        "content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest()
    }


class ExperienceFilter:
    def __init__(self):
        self.constitution = load_constitution()
        if not EXPERIENCE_BUFFER_PATH.exists():
            EXPERIENCE_BUFFER_PATH.mkdir(parents=True, exist_ok=True)

    def _check_format(self, agent_output: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        required_fields = ["agent_type", "task_id", "status", "result", "timestamp"]
        for field in required_fields:
            if field not in agent_output:
                return False, f"缺少必需字段: {field}"
        
        if agent_output["status"] not in ["completed", "failed"]:
            return False, f"无效的状态: {agent_output['status']}"
        
        return True, None

    def _check_anomaly(self, capsule_content: str) -> tuple[bool, Optional[str]]:
        if len(capsule_content) < 10:
            return False, "内容过短，可能无效"
        
        if len(capsule_content) > 50000:
            return False, "内容过长，需要截断"
        
        return True, None

    def _check_values(self, capsule: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        source_agent = capsule["source_agent"]
        
        if source_agent == "explorer":
            if "挑战" in capsule["content"] or "反对" in capsule["content"] or "不同" in capsule["content"]:
                return True, None
            else:
                return True, None
        elif source_agent == "survival":
            if "warning" in capsule["content"] or "不足" in capsule["content"]:
                return True, None
            else:
                return True, None
        elif source_agent == "reflector":
            return True, None
        
        return True, None

    def experience_filter(self, agent_output: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        format_ok, format_error = self._check_format(agent_output)
        if not format_ok:
            print(f"格式检查失败: {format_error}")
            return None
        
        if agent_output["status"] == "failed":
            print("Agent执行失败，不生成经验胶囊")
            return None
        
        content = self._extract_content(agent_output)
        confidence_impact = self._extract_confidence_impact(agent_output)
        
        capsule = create_experience_capsule(
            source_agent=agent_output["agent_type"],
            task_id=agent_output["task_id"],
            content=content,
            confidence_impact=confidence_impact
        )
        
        anomaly_ok, anomaly_error = self._check_anomaly(capsule["content"])
        if not anomaly_ok:
            print(f"异常检测失败: {anomaly_error}")
            return None
        
        values_ok, values_error = self._check_values(capsule)
        if not values_ok:
            print(f"价值观检查失败: {values_error}")
            return None
        
        self._save_capsule(capsule)
        return capsule

    def _extract_content(self, agent_output: Dict[str, Any]) -> str:
        result = agent_output.get("result", {})
        
        if agent_output["agent_type"] == "explorer":
            search_result = result.get("result", {})
            return f"标题: {search_result.get('title', '')}\n摘要: {search_result.get('snippet', '')}"
        elif agent_output["agent_type"] == "survival":
            return json.dumps(result, ensure_ascii=False)
        elif agent_output["agent_type"] == "reflector":
            return json.dumps(result.get("opposing_argument", {}), ensure_ascii=False)
        else:
            return json.dumps(result, ensure_ascii=False)

    def _extract_confidence_impact(self, agent_output: Dict[str, Any]) -> float:
        result = agent_output.get("result", {})
        
        if agent_output["agent_type"] == "explorer":
            search_result = result.get("result", {})
            return search_result.get("confidence_impact", -0.05)
        elif agent_output["agent_type"] == "survival":
            if result.get("status") == "warning":
                return -0.1
            return 0.05
        elif agent_output["agent_type"] == "reflector":
            return -0.08
        else:
            return 0.0

    def _save_capsule(self, capsule: Dict[str, Any]):
        capsule_path = EXPERIENCE_BUFFER_PATH / f"{capsule['capsule_id']}.json"
        with open(capsule_path, "w", encoding="utf-8") as f:
            json.dump(capsule, f, ensure_ascii=False, indent=2)

    def get_pending_capsules(self) -> list[Dict[str, Any]]:
        capsules = []
        for capsule_file in EXPERIENCE_BUFFER_PATH.glob("*.json"):
            with open(capsule_file, "r", encoding="utf-8") as f:
                capsules.append(json.load(f))
        return sorted(capsules, key=lambda x: x["timestamp"])


if __name__ == "__main__":
    filter = ExperienceFilter()
    
    test_output = {
        "agent_type": "explorer",
        "task_id": "test-task-001",
        "status": "completed",
        "result": {
            "exploration_id": "test-exploration-001",
            "query": "测试查询",
            "result": {
                "title": "测试结果",
                "snippet": "这是一条具有挑战性的搜索结果，它提出了不同的观点。",
                "confidence_impact": -0.1
            }
        },
        "timestamp": time.time()
    }
    
    capsule = filter.experience_filter(test_output)
    if capsule:
        print("经验胶囊生成成功:", json.dumps(capsule, ensure_ascii=False, indent=2))

