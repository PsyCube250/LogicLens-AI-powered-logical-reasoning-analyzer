import os
from openai import OpenAI


class DeepSeekLLM:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )

        self.model = "deepseek-chat"


    def chat(self, messages, tools):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        return response.choices[0].message