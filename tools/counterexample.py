from unittest import result

from llm import DeepSeekLLM
from tools.search import SearchTool
import json


class CounterexampleGenerator:

    name = "counterexample_generator"

    description = """
生成能够削弱用户原始陈述的反例。

工具需要：
1. 判断原陈述的结论类型
2. 判断结论强度
3. 判断是否需要检索权威数据支撑反例
4. （需要时）检索权威信源，生成基于事实的反例；否则生成理论构造反例
5. 判断反例是否真正满足原命题的前提
6. 判断反例是否违反原命题结论
7. 评估反例强度
8. 评估反例可信度
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
        self.search_tool = SearchTool()

    # ----------------------------------------------------------------
    # 第一步：判断这次反例是否需要检索权威数据支撑
    # ----------------------------------------------------------------
    def _judge_need_search(self, text, claim):
        prompt = f"""
你是一个判断助手。判断下面这个陈述的反例，是否需要检索权威统计数据/新闻/研究来增强说服力，
还是纯逻辑结构反例就足够（比如反驳一个抽象的全称命题，不涉及具体现实数据）。

【原始陈述】
{text}

【命题分类】
{claim}

判断标准：
- 如果陈述涉及具体的社会现象、群体行为、统计规律（比如"程序员都喜欢游戏"这种可以用调查数据验证/反驳的陈述），
  needs_search = true，并给出 1 个适合搜索引擎检索的中文关键词短语（query）。
- 如果陈述是抽象的价值判断或纯逻辑命题，检索现实数据意义不大，needs_search = false，query 留空。

严格输出 JSON，不要任何多余文字：

{{
    "needs_search": true or false,
    "query": "..."
}}
"""
        response = self.llm.chat(
            [
                {"role": "system", "content": "你是判断助手，只输出JSON。"},
                {"role": "user", "content": prompt},
            ],
            [],
        )

        content = response.content.strip()
        if content.startswith("```"):
            content = content.strip("`")
            if content.startswith("json"):
                content = content[4:].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"needs_search": False, "query": ""}

    # ----------------------------------------------------------------
    # 第二步：生成反例（可选带检索到的权威资料作为上下文）
    # ----------------------------------------------------------------
    def run(self, text, claim=None):

        judge = self._judge_need_search(text, claim)
        evidence_block = "（本次反例不涉及具体现实数据，采用逻辑结构反例）"

        if judge.get("needs_search") and judge.get("query"):
            results = self.search_tool.search(judge["query"])
            evidence_block = self.search_tool.format_for_prompt(results)

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
检索到的权威信源资料（可能为空）
--------------------------------

{evidence_block}

如果上面有真实检索结果，优先基于这些资料构造反例，并在 evidence_type 里标注 "empirical_data"，
在 reason 中注明引用的来源编号（如 [1]）。

如果没有检索结果或检索结果与本命题无关，则使用逻辑构造反例，
evidence_type 标注 "theoretical_construct"，不要编造不存在的统计数据或来源。

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

不要编造真实人物，不要编造不存在的统计数据或引用来源。

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
    "evidence_sources": ["..."],
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

#-----------------------------------------------------------------------

        result = json.loads(content)
        print("DEBUG evidence_sources:", result.get("evidence_sources"))
        return result

#-----------------------------------------------------------------------
        return json.loads(content)
