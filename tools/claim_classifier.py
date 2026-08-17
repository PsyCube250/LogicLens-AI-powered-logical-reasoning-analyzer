import json

from llm import DeepSeekLLM


class ClaimClassifier:

    name = "claim_classifier"

    description = """
判断用户陈述的逻辑类型，并识别其逻辑方向、证据形式和是否需要反例。

重点区分：

1. universal
   全称命题。
   形式：
   所有 A 都是 B
   A 一定导致/对应 B

2. necessary
   必要条件命题。
   形式：
   B 必须满足 A
   想要 B，必须 A
   A 是 B 的必要条件

3. causal
   因果命题。
   形式：
   A 导致 B
   A 会提高 B
   A 造成 B

4. probabilistic
   概率/趋势命题。
   形式：
   A 通常是 B
   A 往往导致 B
   A 更可能 B

6. existential
   存在性命题。
   表示至少存在一个满足条件的对象。

   形式：
   有些 A 是 B
   至少一个 A 是 B
   存在 A 是 B

7. generalization
   从有限样本推断总体。

8. other
   无法归入以上类别。
"""

    schema = {
        "type": "function",
        "function": {
            "name": "claim_classifier",
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

    def run(self, text):

        prompt = f"""
你是一个严格的逻辑命题分类器。

请分析下面的陈述：

【原始陈述】
{text}

你的任务不是判断这个陈述是否正确，
而是判断它属于什么逻辑类型。

--------------------------------
Step 1：识别核心命题
--------------------------------

识别：

subject：
命题讨论的主体或条件。

predicate：
主体被断言具有的属性、结果或状态。

例如：

“早起的人一定会成功”

subject = “早起的人”
predicate = “成功”

例如：

“想成功必须早起”

subject = “成功”
predicate = “早起”

例如：

“有些程序员喜欢游戏”

subject = “程序员”
predicate = “喜欢游戏”

“有些”是数量/存在性限定词，
不是 subject 本身。

注意：

“必须”会改变必要条件的方向。

--------------------------------
Step 2：判断逻辑方向
--------------------------------

统一使用：

subject_implies_predicate

表示：

subject → predicate

例如：

“早起的人一定会成功”

早起 → 成功

---

对于：

“想成功必须早起”

成功 → 早起

此时：

subject = 成功
predicate = 早起

仍然是：

subject → predicate

因此不要因为出现“必须”就机械地把所有句子分类成 necessary。

--------------------------------
Step 3：判断 claim_type
--------------------------------

请严格按照下面的优先级分类。

### 1. generalization

从有限样本、调查对象或实验样本推广到更大的总体。

典型结构：

样本 → 总体

例如：

“调查了100个人，其中63人支持A，因此全国63%的人支持A。”

claim_type = generalization

注意：

如果只是报告样本结果，而没有推广到总体：

“100个人中63个人支持A。”

则是：

statistical

而不是 generalization。

---

### 2. statistical

陈述本身直接报告统计数据、调查结果、比例、样本数量或实验数据。

例如：

“100个人中63个人支持A。”

“根据一项10000人的随机调查，63%的人支持A。”

claim_type = statistical

---

### 3. existential

表示至少存在一个满足条件的对象。

典型表达：

- 有些 A 是 B
- 至少一个 A 是 B
- 存在 A 是 B
- 有一个 A 是 B
- 不是所有 A 都是 B

特别注意：

“不是所有 A 都是 B”

逻辑上等价于：

“至少存在一个 A 不是 B”

因此：

“不是所有程序员都喜欢游戏”

应该分类为：

existential

而不是 universal。

---

### 4. necessary

表示一个条件是另一个结果的必要条件。

核心逻辑：

B → A

也就是说：

想得到 B，必须满足 A。

典型表达：

- 想要 B 必须 A
- B 必须 A
- A 是 B 的必要条件
- 没有 A 就不能 B
- 只有 A 才能 B

例如：

“想成功必须早起”

逻辑：

成功 → 早起

因此：

claim_type = necessary

---

### 5. sufficient

表示一个条件足以推出另一个结果。

核心逻辑：

A → B

典型表达：

- 只要 A 就 B
- A 就一定 B
- A 足以导致 B
- A 是 B 的充分条件
- A 一定会 B

例如：

“只要早起就能成功”

逻辑：

早起 → 成功

因此：

claim_type = sufficient

---

### 6. universal

表示对某个类别中的所有对象作出绝对断言。

典型表达：

- 所有 A 都是 B
- 每个 A 都是 B
- 任何 A 都是 B
- A 都会 B

例如：

“所有程序员都喜欢游戏。”

claim_type = universal

注意：

如果句子明确表达的是：

A → B

并且强调 A 足以推出 B，例如：

“只要 A 就 B”

优先分类为：

sufficient

而不是 universal。

---

### 7. causal

明确表达因果关系。

例如：

“喝咖啡会提高工作效率。”

“运动能够降低压力。”

“早起有助于成功。”

claim_type = causal

注意：

不要因为出现：

“会”

“能够”

“提高”

就机械判断。

必须判断句子的核心是否是在表达：

A 导致 / 促进 / 造成 B。

---

### 8. probabilistic

表达概率、趋势或统计倾向，但没有直接提供统计数据。

典型表达：

- 通常
- 往往
- 大多数
- 更可能
- 倾向于
- 一般来说
- 经常

例如：

“程序员通常喜欢游戏。”

claim_type = probabilistic

“大多数早起的人都成功了。”

claim_type = probabilistic

注意：

“大多数”虽然涉及数量概念，

但如果没有明确数据，

仍然属于 probabilistic。

一个单独的反例不能证伪“大多数”。

---

### 9. other

无法明确归入以上类别。

--------------------------------
Step 4：has_data
--------------------------------

如果陈述明确包含：

- 样本数量
- 百分比
- 比例
- 调查数据
- 实验数据
- 统计数字

则：

has_data = true

否则：

has_data = false

--------------------------------
Step 5：is_absolute
--------------------------------

以下表达通常表示绝对或严格结论：

- 所有
- 每个
- 一定
- 必须
- 从不
- 永远
- 绝不
- 唯一
- 完全

但注意：

“必须”本身主要用于识别 necessary，
不能仅凭“必须”判断所有命题都是 necessary。

--------------------------------
Step 6：requires_counterexample
--------------------------------

判断这个命题是否可以被一个满足前提、
但违反结论的实例直接推翻。

### requires_counterexample = true

通常适用于：

universal
necessary
sufficient

因为这些命题都包含较强的必然关系。

例如：

“所有程序员都喜欢游戏”

寻找：

程序员 AND NOT 喜欢游戏

---

“想成功必须早起”

逻辑：

成功 → 早起

寻找：

成功 AND NOT 早起

---

“只要早起就能成功”

逻辑：

早起 → 成功

寻找：

早起 AND NOT 成功

---

### existential

通常：

requires_counterexample = false

因为：

“至少存在一个 A 是 B”

不是通过寻找一个反例来推翻的。

它需要证明：

不存在 A ∧ B

---

### probabilistic

通常：

requires_counterexample = false

因为一个反例不能直接推翻概率性命题。

例如：

“大多数早起的人都成功了”

一个：

“早起但不成功”

只能说明：

并非所有早起的人都成功，

不能证明：

“大多数”是假的。

因此：

requires_counterexample = false

---

### causal

通常：

requires_counterexample = false

因果命题不能仅靠一个普通反例自动判定为错误。

需要进一步分析：

- 相关性
- 混杂变量
- 反向因果
- 实验设计
- 机制证据

---

### statistical

通常：

requires_counterexample = false

因为这是对数据的直接报告。

---

### generalization

通常：

requires_counterexample = true

但反例不是简单寻找一个个体。

应该寻找：

样本具有代表性不足
或
总体分布与样本不同

的情况。

--------------------------------
Step 7：严格输出 JSON
--------------------------------

只能输出 JSON。

格式：

{{
    "claim_type": "...",
    "subject": "...",
    "predicate": "...",
    "direction": "subject_implies_predicate",
    "has_data": true,
    "is_absolute": false,
    "requires_counterexample": false,
    "reason": "..."
}}

--------------------------------
重要规则
--------------------------------

不要根据单个关键词机械分类。

尤其注意：

“一定”
“必须”
“会”
“通常”

这些词在不同句子中的逻辑作用不同。

必须理解整个句子的方向。

现在分析：

{text}
"""

        response = self.llm.chat(
            [
                {
                    "role": "system",
                    "content": "你是严格的逻辑命题分类器，只输出JSON。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            []
        )

        content = response.content

        # 防止模型偶尔返回 ```json ... ```
        if content.startswith("```"):
            content = content.strip("`")

            if content.startswith("json"):
                content = content[4:].strip()

        print("\n========== RAW LLM OUTPUT ==========")
        print(content)
        print("====================================\n")

        return json.loads(content)