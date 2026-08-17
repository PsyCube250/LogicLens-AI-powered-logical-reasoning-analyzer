from agent.router import LogicAgent


def print_result(result):

    print("\n" + "=" * 60)
    print("                 LOGIC ANALYSIS")
    print("=" * 60)

    # ========================================
    # Claim
    # ========================================

    claim = result["claim"]

    print("\n【核心判断】")

    print(f"类型       : {claim['type']}")
    print(f"主体       : {claim['subject']}")
    print(f"结论       : {claim['predicate']}")
    print(f"逻辑方向   : {claim['direction']}")
    print(f"包含数据   : {claim['has_data']}")
    print(f"绝对程度   : {claim['is_absolute']}")
    print(f"需要反例   : {claim['requires_counterexample']}")

    print(f"\n理由：{claim['reason']}")

    # ========================================
    # Counterexample
    # ========================================

    counterexample = result.get("counterexample")

    if counterexample:

        print("\n【反例分析】")

        print(f"反例       : {counterexample.get('counterexample')}")
        print(f"反例成立   : {counterexample.get('logically_valid')}")
        print(f"前提满足   : {counterexample.get('premise_satisfied')}")
        print(f"结论违反   : {counterexample.get('conclusion_violated')}")
        print(f"反例强度   : {counterexample.get('strength')}")
        print(f"可信度     : {counterexample.get('confidence')}")
        print(f"证据类型   : {counterexample.get('evidence_type')}")

        print(f"\n分析：{counterexample.get('reason')}")

        limitations = counterexample.get("limitations")

        if limitations:
            print(f"\n局限：{limitations}")

    # ========================================
    # Fallacy
    # ========================================

    fallacy = result["fallacy"]

    print("\n【逻辑谬误】")

    print(f"判断：{fallacy['name']}")
    print(f"理由：{fallacy['reason']}")

    # ========================================
    # Bias
    # ========================================

    bias = result["bias"]

    print("\n【认知偏差】")

    print(f"判断：{bias['name']}")
    print(f"理由：{bias['reason']}")

    print("\n" + "=" * 60)


def main():

    agent = LogicAgent()

    print("=" * 60)
    print("             Logic Agent")
    print("=" * 60)
    print("输入一句陈述进行分析。")
    print("输入 q / quit / exit 退出。\n")

    while True:

        text = input("陈述: ").strip()

        if text.lower() in {"q", "quit", "exit"}:
            break

        if not text:
            continue

        try:

            result = agent.run(text)

            print_result(result)

        except Exception as e:

            print("\n[ERROR]")
            print(type(e).__name__)
            print(e)


if __name__ == "__main__":
    main()