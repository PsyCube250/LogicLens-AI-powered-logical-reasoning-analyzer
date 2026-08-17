import os
import json

from openai import OpenAI
from tools.base import BaseTool


class BiasDetector(BaseTool):

    name = "bias_detector"

    description = (
        "Detect cognitive biases in the user's statement."
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
你是一个认知偏差检测工具。

分析用户给出的陈述，判断其中是否存在认知偏差。

重点检查但不限于：

- 幸存者偏差
- 确认偏误
- 可得性启发
- 锚定效应
- 选择偏差
- 代表性启发
- 基本归因错误
- 结果偏误
- 过度自信
- 聚焦效应

不要因为某个偏差名字看起来相关就强行判断。

只有在陈述本身有足够证据时才判断存在偏差。

必须返回 JSON：

{
    "bias": "偏差名称或 none",
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