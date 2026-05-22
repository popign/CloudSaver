import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from config import load_constitution, validate_constitution, compute_constitution_hash


def test_constitution_load():
    """测试宪法加载和验证"""
    constitution = load_constitution()
    assert constitution is not None
    assert "project" in constitution
    assert "soul_questions" in constitution
    assert "meta_rules" in constitution


def test_constitution_validation():
    """测试宪法验证"""
    constitution = load_constitution()
    assert validate_constitution(constitution) is True


def test_constitution_hash():
    """测试宪法哈希"""
    hash1 = compute_constitution_hash()
    hash2 = compute_constitution_hash()
    assert hash1 == hash2


if __name__ == "__main__":
    test_constitution_load()
    print("✅ test_constitution_load passed")
    
    test_constitution_validation()
    print("✅ test_constitution_validation passed")
    
    test_constitution_hash()
    print("✅ test_constitution_hash passed")
    
    print("\n🎉 所有配置测试通过！")

