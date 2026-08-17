class AgentState:

    def __init__(self, text):

        self.text = text

        self.history = []

        self.result = []


    def add_step(
        self,
        thought,
        action,
        observation
    ):

        self.history.append({

            "thought": thought,

            "action": action,

            "observation": observation

        })