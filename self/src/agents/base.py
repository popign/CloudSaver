import json
import time
import uuid
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Any
import sys
sys.path.append(str(Path(__file__).parent.parent))


SELF_STATE_PATH = Path(__file__).parent.parent.parent / "data" / "self_state.json"


class BaseAgent(ABC):
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.agent_id = str(uuid.uuid4())

    def _load_self_state(self) -> Dict[str, Any]:
        if not SELF_STATE_PATH.exists():
            return {
                "timestamp": time.time(),
                "oracle_state": {},
                "task_batch_id": str(uuid.uuid4())
            }
        with open(SELF_STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _update_self_state(self, task_id: str, status: str, result: Any = None):
        state = self._load_self_state()
        
        if "agents" not in state:
            state["agents"] = {}
        
        state["agents"][self.agent_type] = {
            "agent_id": self.agent_id,
            "last_task_id": task_id,
            "status": status,
            "result": result,
            "timestamp": time.time()
        }
        
        with open(SELF_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_id = task.get("task_id", str(uuid.uuid4()))
        self._update_self_state(task_id, "running")
        
        try:
            result = self.execute(task)
            self._update_self_state(task_id, "completed", result)
            return {
                "agent_type": self.agent_type,
                "agent_id": self.agent_id,
                "task_id": task_id,
                "status": "completed",
                "result": result,
                "timestamp": time.time()
            }
        except Exception as e:
            self._update_self_state(task_id, "failed", {"error": str(e)})
            return {
                "agent_type": self.agent_type,
                "agent_id": self.agent_id,
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": time.time()
            }

