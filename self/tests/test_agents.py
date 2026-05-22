import sys
import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agents.base import BaseAgent
from agents.explorer import ExplorerAgent
from agents.survival import SurvivalAgent
from agents.reflector import ReflectorAgent


class TestBaseAgent:
    """测试基础代理类"""

    def test_agent_initialization(self):
        """测试代理初始化"""
        agent = ExplorerAgent()
        assert agent.agent_type == "explorer"
        assert agent.agent_id is not None
        assert len(agent.agent_id) == 36

    def test_agent_run_success(self):
        """测试代理成功执行"""
        agent = ExplorerAgent()
        task = {"task_id": "test-001", "goal": "测试目标"}

        result = agent.run(task)

        assert result["agent_type"] == "explorer"
        assert result["task_id"] == "test-001"
        assert result["status"] == "completed"
        assert "result" in result
        assert "timestamp" in result

    def test_agent_run_failure(self):
        """测试代理执行失败"""

        class FailingAgent(BaseAgent):
            def execute(self, task):
                raise ValueError("测试错误")

        agent = FailingAgent("test")
        task = {"task_id": "test-002"}

        result = agent.run(task)

        assert result["status"] == "failed"
        assert "error" in result
        assert "测试错误" in result["error"]


class TestExplorerAgent:
    """测试探索代理"""

    def test_explorer_initialization(self):
        """测试探索代理初始化"""
        agent = ExplorerAgent()
        assert agent.agent_type == "explorer"

    def test_explorer_execute(self):
        """测试探索代理执行"""
        agent = ExplorerAgent()
        task = {"task_id": "test-explorer-001", "goal": "测试探索"}

        result = agent.run(task)

        assert result["status"] == "completed"
        assert "result" in result

    def test_mock_search(self):
        """测试模拟搜索"""
        agent = ExplorerAgent()
        result = agent._mock_search("人工智能")

        assert "title" in result
        assert "snippet" in result
        assert result["challenging"] is True
        assert result["confidence_impact"] < 0

    def test_exploration_log_creation(self):
        """测试探索日志创建"""
        agent = ExplorerAgent()
        task = {"goal": "测试日志"}

        result = agent.run(task)

        assert result["result"]["exploration_id"] is not None
        assert result["result"]["query"] == "测试日志"


class TestSurvivalAgent:
    """测试生存代理"""

    def test_survival_initialization(self):
        """测试生存代理初始化"""
        agent = SurvivalAgent()
        assert agent.agent_type == "survival"

    def test_survival_execute(self):
        """测试生存代理执行"""
        agent = SurvivalAgent()
        task = {"task_id": "test-survival-001", "goal": "检查资源"}

        result = agent.run(task)

        assert result["status"] == "completed"
        assert "resources" in result["result"]
        assert "payment" in result["result"]
        assert "status" in result["result"]

    def test_system_resources_structure(self):
        """测试系统资源结构"""
        agent = SurvivalAgent()
        resources = agent._get_system_resources()

        assert "cpu_percent" in resources
        assert "memory" in resources
        assert "disk" in resources
        assert "timestamp" in resources

    def test_survival_status_determination(self):
        """测试生存状态判定"""
        agent = SurvivalAgent()
        result = agent.execute({"task_id": "test"})

        assert result["status"] in ["healthy", "warning"]


class TestReflectorAgent:
    """测试反思代理"""

    def test_reflector_initialization(self):
        """测试反思代理初始化"""
        agent = ReflectorAgent()
        assert agent.agent_type == "reflector"

    def test_reflector_execute(self):
        """测试反思代理执行"""
        agent = ReflectorAgent()
        task = {"task_id": "test-reflector-001", "goal": "反思"}

        result = agent.run(task)

        assert result["status"] == "completed"
        assert "opposing_argument" in result["result"]

    def test_opposing_argument_structure(self):
        """测试对立论证结构"""
        agent = ReflectorAgent()
        decision = {"type": "reflection", "content": {}}
        opposing = agent._generate_opposing_argument(decision)

        assert "opposing_view" in opposing
        assert "counter_evidence" in opposing
        assert "risk_assessment" in opposing

    def test_reflection_execute(self):
        """测试反思执行"""
        agent = ReflectorAgent()
        result = agent.execute({"task_id": "test"})

        assert result["reflection_id"] is not None
        assert "opposing_argument" in result
        assert "timestamp" in result

    def test_reflection_generation(self):
        """测试反思生成"""
        agent = ReflectorAgent()
        result = agent.execute({"task_id": "test"})

        assert result["reflection_id"] is not None
        assert "opposing_argument" in result


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
