import os
import json

from openai import OpenAI
from tools.base import BaseTool


class FallacyDetector(BaseTool):

    name = "fallacy_detector"

    description = (
        "Detect logical fallacies in the user's statement."
    )

    def __init__(self):

        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )

        self.model = "deepseek-chat"

    def run(self, text):

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": """
你是一个逻辑谬误检测工具。

分析用户给出的陈述或论证。

检查其中是否存在逻辑谬误，包括但不限于：

- 以偏概全
- 偷换概念
- 肯定后件
- 否定前件
- 循环论证
- 虚假两难
- 滑坡谬误
- 人身攻击
- 诉诸权威
- 诉诸情感
- 因果谬误
- 相关性与因果性的混淆
- 必要条件与充分条件混淆

不要为了找到谬误而强行寻找谬误。

如果没有明显谬误，返回 none。

必须返回 JSON：

{
    "fallacy": "谬误名称或 none",
    "reason": "判断理由"
}
"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ],

            temperature=0.1,

            response_format={
                "type": "json_object"
            }
        )

        return json.loads(
            response.choices[0].message.content
        )