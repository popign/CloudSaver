import sys
import json
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from oracle import Oracle


class TestOracle:
    """测试 Oracle 核心"""

    def test_oracle_initialization(self):
        """测试 Oracle 初始化"""
        oracle = Oracle()

        assert oracle.constitution is not None
        assert oracle.self_model is not None
        assert "identity" in oracle.self_model
        assert "cognitive_clarity" in oracle.self_model
        assert "knowledge_base" in oracle.self_model

    def test_self_model_initial_state(self):
        """测试自我模型初始状态"""
        oracle = Oracle()

        assert oracle.self_model["identity"] == "SELF - Slow Thinking Core"
        assert oracle.self_model["cognitive_clarity"] == 0.7
        assert oracle.self_model["last_reflection"] is None
        assert oracle.self_model["knowledge_base"] == []
        assert oracle.self_model["active_tasks"] == []

    def test_build_system_prompt(self):
        """测试系统提示构建"""
        oracle = Oracle()
        prompt = oracle._build_system_prompt()

        assert "SELF" in prompt
        assert "Oracle" in prompt
        assert "不可变公理" in prompt
        assert "元规则" in prompt

    def test_self_reflect_empty_knowledge(self):
        """测试自我反思 - 空知识库"""
        oracle = Oracle()
        oracle.self_model["knowledge_base"] = []
        oracle.self_model["cognitive_clarity"] = 0.7

        reflection = oracle.self_reflect()

        assert "timestamp" in reflection
        assert "cognitive_clarity" in reflection
        assert "contradictions" in reflection
        assert "recommendations" in reflection
        assert len(reflection["contradictions"]) > 0
        assert "知识基为空" in reflection["contradictions"][0]

    def test_self_reflect_low_clarity(self):
        """测试自我反思 - 低认知清晰度"""
        oracle = Oracle()
        oracle.self_model["knowledge_base"] = ["已有知识"]
        oracle.self_model["cognitive_clarity"] = 0.5

        reflection = oracle.self_reflect()

        assert "认知清晰度低于阈值" in reflection["contradictions"]

    def test_self_reflect_updates_model(self):
        """测试自我反思更新模型"""
        oracle = Oracle()
        initial_reflection_time = oracle.self_model["last_reflection"]

        oracle.self_reflect()

        assert oracle.self_model["last_reflection"] is not None
        assert oracle.self_model["last_reflection"] != initial_reflection_time

    def test_decompose_goal_clarity(self):
        """测试目标分解 - 提升清晰度"""
        oracle = Oracle()
        tasks = oracle.decompose_goal("提升自我认知清晰度")

        assert len(tasks) == 3
        agent_types = [t["agent_type"] for t in tasks]
        assert "explorer" in agent_types
        assert "survival" in agent_types
        assert "reflector" in agent_types

    def test_decompose_goal_search(self):
        """测试目标分解 - 搜索"""
        oracle = Oracle()
        tasks = oracle.decompose_goal("去搜索一条可能挑战我现有知识的信息")

        assert len(tasks) == 1
        assert tasks[0]["agent_type"] == "explorer"
        assert "priority" in tasks[0]
        assert tasks[0]["priority"] == "high"

    def test_decompose_goal_custom(self):
        """测试目标分解 - 自定义目标"""
        oracle = Oracle()
        tasks = oracle.decompose_goal("自定义探索目标")

        assert len(tasks) >= 1
        assert tasks[0]["goal"] == "自定义探索目标"

    def test_decompose_goal_updates_model(self):
        """测试目标分解更新模型"""
        oracle = Oracle()
        oracle.self_model["active_tasks"] = []

        oracle.decompose_goal("测试目标")

        assert len(oracle.self_model["active_tasks"]) > 0

    def test_ingest_experience_capsule(self):
        """测试经验胶囊吸收"""
        oracle = Oracle()
        initial_knowledge_count = len(oracle.self_model["knowledge_base"])
        initial_clarity = oracle.self_model["cognitive_clarity"]

        capsule = {
            "capsule_id": "test-capsule-001",
            "content": "测试内容",
            "confidence_impact": 0.1,
            "timestamp": time.time()
        }

        oracle.ingest_experience_capsule(capsule)

        assert len(oracle.self_model["knowledge_base"]) == initial_knowledge_count + 1
        assert oracle.self_model["cognitive_clarity"] > initial_clarity

    def test_ingest_negative_impact(self):
        """测试负面经验影响"""
        oracle = Oracle()
        oracle.self_model["cognitive_clarity"] = 0.5

        capsule = {
            "capsule_id": "test-capsule-002",
            "content": "负面内容",
            "confidence_impact": -0.2,
            "timestamp": time.time()
        }

        oracle.ingest_experience_capsule(capsule)

        assert oracle.self_model["cognitive_clarity"] < 0.5
        assert oracle.self_model["cognitive_clarity"] >= 0.1

    def test_ingest_clamps_clarity(self):
        """测试认知清晰度边界限制"""
        oracle = Oracle()
        oracle.self_model["cognitive_clarity"] = 0.95

        capsule = {
            "capsule_id": "test-capsule-003",
            "content": "大幅提升",
            "confidence_impact": 0.5,
            "timestamp": time.time()
        }

        oracle.ingest_experience_capsule(capsule)

        assert oracle.self_model["cognitive_clarity"] <= 1.0

    def test_get_self_state(self):
        """测试获取自我状态"""
        oracle = Oracle()
        oracle.self_model["test_field"] = "test_value"

        state = oracle.get_self_state()

        assert "test_field" in state
        assert state["test_field"] == "test_value"
        assert state is not oracle.self_model

    def test_constitution_validation_on_init(self):
        """测试初始化时宪法验证"""
        oracle = Oracle()
        assert oracle.constitution is not None
        assert "soul_questions" in oracle.constitution
        assert len(oracle.constitution["soul_questions"]) == 3


class TestOracleIntegration:
    """测试 Oracle 集成"""

    def test_full_cycle(self):
        """测试完整循环"""
        oracle = Oracle()

        reflection = oracle.self_reflect()
        assert reflection is not None

        tasks = oracle.decompose_goal("提升自我认知清晰度")
        assert len(tasks) > 0

        capsule = {
            "capsule_id": "integration-test",
            "content": "集成测试内容",
            "confidence_impact": 0.05,
            "timestamp": time.time()
        }
        oracle.ingest_experience_capsule(capsule)

        state = oracle.get_self_state()
        assert len(state["knowledge_base"]) > 0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
