import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from filter import ExperienceFilter, create_experience_capsule


class TestExperienceFilter:
    """测试经验过滤器"""

    def test_filter_initialization(self):
        """测试过滤器初始化"""
        filter = ExperienceFilter()
        assert filter.constitution is not None
        assert "project" in filter.constitution

    def test_format_check_valid(self):
        """测试格式检查 - 有效数据"""
        filter = ExperienceFilter()
        valid_output = {
            "agent_type": "explorer",
            "task_id": "test-001",
            "status": "completed",
            "result": {},
            "timestamp": time.time()
        }

        is_valid, error = filter._check_format(valid_output)
        assert is_valid is True
        assert error is None

    def test_format_check_missing_field(self):
        """测试格式检查 - 缺少字段"""
        filter = ExperienceFilter()
        invalid_output = {
            "agent_type": "explorer",
            "task_id": "test-001",
            "status": "completed"
        }

        is_valid, error = filter._check_format(invalid_output)
        assert is_valid is False
        assert "缺少必需字段" in error

    def test_format_check_invalid_status(self):
        """测试格式检查 - 无效状态"""
        filter = ExperienceFilter()
        invalid_output = {
            "agent_type": "explorer",
            "task_id": "test-001",
            "status": "invalid_status",
            "result": {},
            "timestamp": time.time()
        }

        is_valid, error = filter._check_format(invalid_output)
        assert is_valid is False
        assert "无效的状态" in error

    def test_anomaly_check_valid_length(self):
        """测试异常检测 - 有效长度"""
        filter = ExperienceFilter()
        valid_content = "这是一个有效的测试内容" * 10

        is_valid, error = filter._check_anomaly(valid_content)
        assert is_valid is True
        assert error is None

    def test_anomaly_check_too_short(self):
        """测试异常检测 - 内容过短"""
        filter = ExperienceFilter()
        short_content = "太短"

        is_valid, error = filter._check_anomaly(short_content)
        assert is_valid is False
        assert "过短" in error

    def test_anomaly_check_too_long(self):
        """测试异常检测 - 内容过长"""
        filter = ExperienceFilter()
        long_content = "测试" * 30000

        is_valid, error = filter._check_anomaly(long_content)
        assert is_valid is False
        assert "过长" in error

    def test_values_check_explorer(self):
        """测试价值观检查 - 探索者"""
        filter = ExperienceFilter()
        capsule = {
            "source_agent": "explorer",
            "content": "这是一个具有挑战性的观点"
        }

        is_valid, error = filter._check_values(capsule)
        assert is_valid is True

    def test_values_check_survival_warning(self):
        """测试价值观检查 - 生存警告"""
        filter = ExperienceFilter()
        capsule = {
            "source_agent": "survival",
            "content": "系统资源不足"
        }

        is_valid, error = filter._check_values(capsule)
        assert is_valid is True

    def test_extract_content_explorer(self):
        """测试内容提取 - 探索者"""
        filter = ExperienceFilter()
        agent_output = {
            "agent_type": "explorer",
            "task_id": "test-001",
            "status": "completed",
            "result": {
                "result": {
                    "title": "测试标题",
                    "snippet": "测试摘要"
                }
            },
            "timestamp": time.time()
        }

        content = filter._extract_content(agent_output)
        assert "测试标题" in content
        assert "测试摘要" in content

    def test_extract_confidence_impact_explorer(self):
        """测试置信度影响提取 - 探索者"""
        filter = ExperienceFilter()
        agent_output = {
            "agent_type": "explorer",
            "task_id": "test-001",
            "status": "completed",
            "result": {
                "result": {
                    "confidence_impact": -0.15
                }
            },
            "timestamp": time.time()
        }

        impact = filter._extract_confidence_impact(agent_output)
        assert impact == -0.15

    def test_experience_filter_full_flow(self):
        """测试完整过滤流程"""
        filter = ExperienceFilter()
        agent_output = {
            "agent_type": "explorer",
            "task_id": "test-full-flow",
            "status": "completed",
            "result": {
                "result": {
                    "title": "完整流程测试",
                    "snippet": "这是一个完整的测试摘要",
                    "confidence_impact": -0.1
                }
            },
            "timestamp": time.time()
        }

        capsule = filter.experience_filter(agent_output)
        assert capsule is not None
        assert capsule["capsule_id"] is not None
        assert capsule["source_agent"] == "explorer"
        assert capsule["task_id"] == "test-full-flow"

    def test_experience_filter_failed_task(self):
        """测试失败任务不生成胶囊"""
        filter = ExperienceFilter()
        failed_output = {
            "agent_type": "explorer",
            "task_id": "test-failed",
            "status": "failed",
            "result": {"error": "测试错误"},
            "timestamp": time.time()
        }

        capsule = filter.experience_filter(failed_output)
        assert capsule is None

    def test_create_experience_capsule(self):
        """测试经验胶囊创建"""
        capsule = create_experience_capsule(
            source_agent="test",
            task_id="test-001",
            content="测试内容",
            confidence_impact=0.5
        )

        assert capsule["capsule_id"] is not None
        assert capsule["source_agent"] == "test"
        assert capsule["task_id"] == "test-001"
        assert capsule["content"] == "测试内容"
        assert capsule["confidence_impact"] == 0.5
        assert "content_hash" in capsule
        assert "timestamp" in capsule


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
