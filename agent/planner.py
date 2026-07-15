from llm.provider import LLMProvider
from agent.state import Action, State

class Planner:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def plan(self, state: State) -> Action: # FIX: Nhận State thay vì Action
        plan = self.llm_provider.generate_plan(state)
        return plan