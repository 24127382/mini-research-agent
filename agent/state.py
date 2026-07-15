from pydantic import BaseModel

class Action(BaseModel): 
    tool: str | None
    arguments: dict 
    thinking: bool 
    response: str | None 
    
class State(BaseModel): 
    messages: list[dict] 
    context: list[dict] 
    thinking: bool
    action: Action | None
    observation: str | None 
    iteration: int = 0