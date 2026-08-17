class ToolRegistry:

    def __init__(self):
        self.tools = {}


    def register(self, tool):

        self.tools[tool.name] = tool


    def get_tool(self, name):

        return self.tools.get(name)


    def list_tools(self):

        return [
            {
                "name":tool.name,
                "description":tool.description
            }
            for tool in self.tools.values()
        ]
    def get_schemas(self):

        schemas = []

        for tool in self.tools.values():

            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "需要分析的文本"
                            }
                        },
                        "required": ["text"]
                    }
                }
            })

        return schemas