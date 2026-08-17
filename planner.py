class Planner:

    def __init__(self, llm):

        self.llm = llm


    def decide_next(self, text, state, tools):

        return self.llm.decide_next(
            text,
            state.history,
            tools
        )