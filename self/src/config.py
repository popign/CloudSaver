import yaml
import hashlib
import os
from pathlib import Path


CONSTITUTION_PATH = Path(__file__).parent.parent / "config" / "constitution.yaml"
CONSTITUTION_HASH_PATH = Path(__file__).parent.parent / "config" / ".constitution_hash"


def compute_constitution_hash() -> str:
    with open(CONSTITUTION_PATH, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_constitution() -> dict:
    if not CONSTITUTION_PATH.exists():
        raise FileNotFoundError(f"Constitution file not found at {CONSTITUTION_PATH}")

    current_hash = compute_constitution_hash()

    if CONSTITUTION_HASH_PATH.exists():
        with open(CONSTITUTION_HASH_PATH, "r") as f:
            saved_hash = f.read().strip()
        if current_hash != saved_hash:
            raise ValueError("Constitution file has been tampered with!")
    else:
        with open(CONSTITUTION_HASH_PATH, "w") as f:
            f.write(current_hash)

    with open(CONSTITUTION_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_constitution(constitution: dict) -> bool:
    required_keys = ["project", "soul_questions", "meta_rules", "immutable_claims", "safety"]
    for key in required_keys:
        if key not in constitution:
            raise ValueError(f"Constitution missing required key: {key}")

    if len(constitution["soul_questions"]) != 3:
        raise ValueError("Constitution must have exactly 3 soul questions")

    if len(constitution["meta_rules"]) != 3:
        raise ValueError("Constitution must have exactly 3 meta rules")

    return True


if __name__ == "__main__":
    constitution = load_constitution()
    validate_constitution(constitution)
    print("Constitution loaded and validated successfully!")
    print(f"Project: {constitution['project']['name']} v{constitution['project']['version']}")

