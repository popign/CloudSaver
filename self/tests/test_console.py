import sys
import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from console.app import FreezeManager, get_agent_status, get_experience_capsules, get_oracle_state


class TestFreezeManager:
    """测试冻结管理器"""

    def test_freeze_manager_init_unfrozen(self, tmp_path):
        """测试冻结管理器初始化 - 未冻结状态"""
        with patch("console.app.FREEZE_FLAG_PATH", tmp_path / "freeze.flag"):
            from console.app import FreezeManager
            manager = FreezeManager()
            assert manager.frozen is False

    def test_freeze_manager_init_frozen(self, tmp_path):
        """测试冻结管理器初始化 - 已冻结状态"""
        flag_path = tmp_path / "freeze.flag"
        flag_path.write_text(str(time.time()))

        with patch("console.app.FREEZE_FLAG_PATH", flag_path):
            from console.app import FreezeManager
            manager = FreezeManager()
            assert manager.frozen is True

    def test_freeze(self, tmp_path):
        """测试冻结系统"""
        flag_path = tmp_path / "freeze.flag"

        with patch("console.app.FREEZE_FLAG_PATH", flag_path):
            from console.app import FreezeManager
            manager = FreezeManager()
            result = manager.freeze()

            assert manager.frozen is True
            assert result["status"] == "frozen"
            assert flag_path.exists()

    def test_unfreeze(self, tmp_path):
        """测试解冻系统"""
        flag_path = tmp_path / "freeze.flag"
        flag_path.write_text(str(time.time()))

        with patch("console.app.FREEZE_FLAG_PATH", flag_path):
            from console.app import FreezeManager
            manager = FreezeManager()
            result = manager.unfreeze()

            assert manager.frozen is False
            assert result["status"] == "unfrozen"
            assert not flag_path.exists()

    def test_is_frozen(self, tmp_path):
        """测试冻结状态检查"""
        flag_path = tmp_path / "freeze.flag"

        with patch("console.app.FREEZE_FLAG_PATH", flag_path):
            from console.app import FreezeManager
            manager = FreezeManager()

            assert manager.is_frozen() is False
            manager.freeze()
            assert manager.is_frozen() is True
            manager.unfreeze()
            assert manager.is_frozen() is False


class TestStatusFunctions:
    """测试状态获取函数"""

    def test_get_agent_status_no_data(self, tmp_path):
        """测试获取 Agent 状态 - 无数据"""
        state_path = tmp_path / "self_state.json"

        with patch("console.app.SELF_STATE_PATH", state_path):
            status = get_agent_status()
            assert status == {}

    def test_get_agent_status_with_data(self, tmp_path):
        """测试获取 Agent 状态 - 有数据"""
        state_path = tmp_path / "self_state.json"
        state_data = {
            "agents": {
                "explorer": {
                    "agent_id": "test-123",
                    "status": "completed",
                    "timestamp": time.time()
                }
            }
        }
        state_path.write_text(json.dumps(state_data))

        with patch("console.app.SELF_STATE_PATH", state_path):
            status = get_agent_status()
            assert "explorer" in status
            assert status["explorer"]["status"] == "completed"

    def test_get_experience_capsules_no_data(self, tmp_path):
        """测试获取经验胶囊 - 无数据"""
        buffer_path = tmp_path / "experience_buffer"

        with patch("console.app.EXPERIENCE_BUFFER_PATH", buffer_path):
            capsules = get_experience_capsules()
            assert capsules == []

    def test_get_experience_capsules_with_data(self, tmp_path):
        """测试获取经验胶囊 - 有数据"""
        buffer_path = tmp_path / "experience_buffer"
        buffer_path.mkdir()

        capsule = {
            "capsule_id": "test-capsule-001",
            "source_agent": "explorer",
            "content": "测试内容",
            "timestamp": time.time()
        }
        (buffer_path / "test-capsule-001.json").write_text(json.dumps(capsule))

        with patch("console.app.EXPERIENCE_BUFFER_PATH", buffer_path):
            capsules = get_experience_capsules()
            assert len(capsules) == 1
            assert capsules[0]["capsule_id"] == "test-capsule-001"

    def test_get_experience_capsules_sorted(self, tmp_path):
        """测试经验胶囊按时间排序"""
        buffer_path = tmp_path / "experience_buffer"
        buffer_path.mkdir()

        capsule1 = {
            "capsule_id": "capsule-1",
            "source_agent": "explorer",
            "content": "旧内容",
            "timestamp": 1000
        }
        capsule2 = {
            "capsule_id": "capsule-2",
            "source_agent": "survival",
            "content": "新内容",
            "timestamp": 2000
        }
        (buffer_path / "capsule-1.json").write_text(json.dumps(capsule1))
        (buffer_path / "capsule-2.json").write_text(json.dumps(capsule2))

        with patch("console.app.EXPERIENCE_BUFFER_PATH", buffer_path):
            capsules = get_experience_capsules()
            assert len(capsules) == 2
            assert capsules[0]["capsule_id"] == "capsule-2"
            assert capsules[1]["capsule_id"] == "capsule-1"

    def test_get_oracle_state(self):
        """测试获取 Oracle 状态"""
        with patch("console.app.Oracle") as MockOracle:
            mock_instance = MagicMock()
            mock_instance.get_self_state.return_value = {
                "identity": "SELF",
                "cognitive_clarity": 0.8,
                "knowledge_base": []
            }
            MockOracle.return_value = mock_instance

            state = get_oracle_state()
            assert state["cognitive_clarity"] == 0.8


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
