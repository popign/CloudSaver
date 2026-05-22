import json
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from config import load_constitution, validate_constitution
from oracle import Oracle
from agents import SurvivalAgent, ExplorerAgent, ReflectorAgent
from filter import ExperienceFilter


def main():
    print("=" * 60)
    print("SELF - 双核异步自举系统 v0.1-mvp")
    print("=" * 60)
    
    constitution = load_constitution()
    validate_constitution(constitution)
    print("✅ 宪法加载并验证成功")
    
    oracle = Oracle()
    print("✅ Oracle 初始化成功")
    
    filter = ExperienceFilter()
    print("✅ 经验过滤器初始化成功")
    
    print("\n" + "=" * 60)
    print("Milestone 0: 完成首次完整循环")
    print("=" * 60)
    
    print("\n1️⃣  Oracle 自我反思...")
    reflection = oracle.self_reflect()
    print(f"   认知清晰度: {reflection['cognitive_clarity']:.2%}")
    print(f"   矛盾点: {len(reflection['contradictions'])}")
    
    print("\n2️⃣  Oracle 分解目标...")
    tasks = oracle.decompose_goal("去搜索一条可能挑战我现有知识的信息")
    print(f"   生成任务数: {len(tasks)}")
    for task in tasks:
        print(f"   - [{task['agent_type']}] {task['goal']}")
    
    print("\n3️⃣  执行 Agent 任务...")
    agent_outputs = []
    for task in tasks:
        print(f"   执行 {task['agent_type']} Agent...")
        
        if task["agent_type"] == "survival":
            agent = SurvivalAgent()
        elif task["agent_type"] == "explorer":
            agent = ExplorerAgent()
        elif task["agent_type"] == "reflector":
            agent = ReflectorAgent()
        else:
            continue
        
        output = agent.run(task)
        agent_outputs.append(output)
        print(f"   状态: {output['status']}")
    
    print("\n4️⃣  经验防火墙过滤...")
    capsules = []
    for output in agent_outputs:
        capsule = filter.experience_filter(output)
        if capsule:
            capsules.append(capsule)
            print(f"   ✅ 生成经验胶囊: {capsule['capsule_id']} (来自 {capsule['source_agent']})")
    
    print("\n5️⃣  Oracle 吸收经验胶囊...")
    for capsule in capsules:
        oracle.ingest_experience_capsule(capsule)
        print(f"   ✅ 吸收胶囊: {capsule['capsule_id']}")
    
    oracle_state = oracle.get_self_state()
    print(f"\n   更新后认知清晰度: {oracle_state['cognitive_clarity']:.2%}")
    print(f"   知识条目数: {len(oracle_state['knowledge_base'])}")
    
    print("\n" + "=" * 60)
    print("🎉 Milestone 0 完成！")
    print("=" * 60)
    print("\n📊 系统状态:")
    print(f"   Oracle 认知清晰度: {oracle_state['cognitive_clarity']:.2%}")
    print(f"   知识条目: {len(oracle_state['knowledge_base'])}")
    print(f"   经验胶囊: {len(capsules)}")
    print("\n🌐 运维终端: http://localhost:8000")
    print("\n提示: 运行 `python -m src.console.app` 启动运维终端")


if __name__ == "__main__":
    main()

