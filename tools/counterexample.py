from urllib import response
from llm import DeepSeekLLM
import json


class CounterexampleGenerator:

    name = "counterexample_generator"

    description = """
生成能够削弱用户原始陈述的反例。

工具需要：
1. 判断原陈述的结论类型
2. 判断结论强度
3. 生成针对性反例
4. 判断反例是否真正满足原命题的前提
5. 判断反例是否违反原命题结论
6. 评估反例强度
7. 评估反例可信度
"""

    schema = {
        "type": "function",
        "function": {
            "name": "counterexample_generator",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "statement": {
                        "type": "string",
                        "description": "需要分析的原始陈述"
                    }
                },
                "required": ["statement"]
            }
        }
    }

    def __init__(self):
        self.llm = DeepSeekLLM()

    def run(self, text, claim=None):

        prompt = f"""
你是一个严格的逻辑反例分析器。

请分析下面的陈述：

【原始陈述】
{text}

--------------------------------
已经完成的命题分类
--------------------------------

下面是上游 ClaimClassifier 已经完成的分析：

{claim}

重要：

你不需要重新判断 claim_type。

必须以这个分类结果作为本次反例分析的逻辑基础。

尤其不要自行改变：

- claim_type
- subject
- predicate
- direction
- requires_counterexample

你的任务只是基于这些结构生成反例。

--------------------------------
Step 1：理解逻辑结构
--------------------------------

根据上游分类结果理解：

subject
predicate
direction
claim_type

例如：

claim_type = sufficient
subject = 早起
predicate = 成功

则逻辑结构为：

早起 → 成功

有效反例必须满足：

早起 AND NOT 成功

---

如果：

claim_type = necessary
subject = 成功
predicate = 早起

则：

成功 → 早起

有效反例必须满足：

成功 AND NOT 早起

---

如果：

claim_type = universal
subject = 程序员
predicate = 喜欢游戏

则：

程序员 → 喜欢游戏

有效反例：

程序员 AND NOT 喜欢游戏

--------------------------------
Step 2：生成反例
--------------------------------

反例必须：

1. 满足原命题的 subject
2. 满足 subject → predicate 中的前件
3. 违反 predicate
4. 与原命题的逻辑方向一致
5. 不得因为自己重新分类而改变逻辑结构

如果没有可靠的真实人物或事实：

优先使用明确标记的理论构造。

不要编造真实人物。

--------------------------------
Step 3：验证
--------------------------------

检查：

premise_satisfied
conclusion_violated
logically_valid

--------------------------------
Step 4：评估
--------------------------------

strength：

very_strong
strong
moderate
weak
invalid

confidence：

0 到 1

区分：

逻辑有效性

和

现实事实可信度。

--------------------------------
严格输出 JSON
--------------------------------

{{
    "statement": "...",
    "claim_type": "...",
    "claim_strength": "...",
    "counterexample": "...",
    "premise_satisfied": true,
    "conclusion_violated": true,
    "logically_valid": true,
    "strength": "...",
    "confidence": 0.0,
    "evidence_type": "...",
    "reason": "...",
    "limitations": "..."
}}
"""

        response = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": "你是严格的逻辑反例分析器，只输出JSON。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            []
        )

        content = response.content.strip()

        # 防止模型偶尔返回 ```json ... ```
        if content.startswith("```"):
            content = content.strip("`")

            if content.startswith("json"):
                content = content[4:].strip()

        return json.loads(content)