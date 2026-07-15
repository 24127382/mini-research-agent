from llm.provider import LLMProvider
from agent.state import State, Action
from agent.planner import Planner
from agent.executor import Executor

executor = Executor()
planner = Planner(LLMProvider("Qwen/Qwen2.5-7B-Instruct")) # Đổi tên model thực tế của bạn

user = input('Please enter your query: ')

# Khởi tạo state ban đầu
state = State(
    messages=[{"role": "user", "content": user}],
    context=[],
    thinking=True,
    action=None,
    observation=None,
    iteration=0
)

print(f"\n[User Query]: {user}\n")

while state.thinking:
    print(f"--- Iteration {state.iteration} ---")
    
    # 1. Gọi LLM lập kế hoạch
    new_action = planner.plan(state)
    state.action = new_action
    
    print(f"Agent Action: Thinking={new_action.thinking}, Tool={new_action.tool}, Args={new_action.arguments}")
    
    # 2. Nếu agent quyết định dừng suy nghĩ (đã có câu trả lời)
    if not new_action.thinking:
        print(f"\n[Final Response]: {new_action.response}")
        break

    # 3. Nếu Agent quyết định dùng tool
    if new_action.tool:
        print(f"Executing tool: {new_action.tool}...")
        observation = executor.execute(new_action)
        state.observation = observation
        print(f"Observation: {observation[:200]}...") # Print log ngắn gọn
    else:
        state.observation = "Không có tool nào được gọi."

    # 4. Lưu lại trí nhớ (context) cho lần chạy sau
    state.context.append({
        "iteration": state.iteration,
        "action": new_action.model_dump(),
        "observation": state.observation
    })
    
    state.iteration += 1