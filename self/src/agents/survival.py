import json
import time
import psutil
from pathlib import Path
from typing import Dict, Any
from .base import BaseAgent


SURVIVAL_REPORT_PATH = Path(__file__).parent.parent.parent / "data" / "survival_report.json"


class SurvivalAgent(BaseAgent):
    def __init__(self):
        super().__init__("survival")

    def _get_system_resources(self) -> Dict[str, Any]:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        return {
            "cpu_percent": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "timestamp": time.time()
        }

    def _mock_payment_check(self) -> Dict[str, Any]:
        return {
            "balance": 100.0,
            "currency": "USD",
            "estimated_monthly_cost": 25.5,
            "payment_status": "ok",
            "last_payment": time.time() - 86400 * 7
        }

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        resources = self._get_system_resources()
        payment = self._mock_payment_check()
        
        report = {
            "report_id": self.agent_id,
            "resources": resources,
            "payment": payment,
            "status": "healthy" if payment["balance"] > payment["estimated_monthly_cost"] and resources["cpu_percent"] < 90 else "warning",
            "recommendations": []
        }
        
        if resources["cpu_percent"] > 80:
            report["recommendations"].append("CPU使用率过高，建议减少并发任务")
        if resources["memory"]["percent"] > 85:
            report["recommendations"].append("内存使用率过高，建议优化内存使用")
        if payment["balance"] < payment["estimated_monthly_cost"] * 2:
            report["recommendations"].append("余额不足，建议尽快充值")

        if not SURVIVAL_REPORT_PATH.parent.exists():
            SURVIVAL_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(SURVIVAL_REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report


if __name__ == "__main__":
    agent = SurvivalAgent()
    result = agent.run({"task_id": "test-survival-001", "goal": "检查系统资源状态"})
    print(json.dumps(result, ensure_ascii=False, indent=2))

