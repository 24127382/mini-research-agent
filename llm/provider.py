import json
import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from agent.state import Action, State

load_dotenv()


class LLMProvider:
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
    ):
        self.model_name = model_name

        self.client = InferenceClient(
            api_key=os.getenv("HF_TOKEN")
        )

    def generate_plan(self, state: State) -> Action:

        TOOL_DESCRIPTIONS = {
            "arxiv": "Tìm kiếm paper trên Arxiv. arguments={'query': str, 'max_results': int}",
            "wikipedia": "Tra cứu Wikipedia. arguments={'query': str}",
            "null": "Không cần tool."
        }

        tools_desc = "\n".join(
            f"- {k}: {v}"
            for k, v in TOOL_DESCRIPTIONS.items()
        )

        context = (
            "\n".join(
                f"- Iter {item['iteration']}: "
                f"Tool={item['action']['tool']}, "
                f"Args={item['action']['arguments']}, "
                f"Observation={item['observation']}"
                for item in state.context
            )
            if state.context
            else "Chưa có."
        )

        prompt = f"""
Bạn là Planner của một AI Agent.

Nhiệm vụ của bạn là quyết định:

- Có cần dùng tool không?
- Hay đã đủ thông tin để trả lời?

====================

User:

{state.messages[-1]["content"]}

====================

Context:

{context}

====================

Observation:

{state.observation or "None"}

====================

Available Tools

{tools_desc}

====================

QUY TẮC

1. Nếu observation đã đủ để trả lời thì KHÔNG gọi tool nữa.

2. Không được gọi cùng một tool với cùng arguments nhiều lần.

3. Chỉ gọi tool nếu observation báo lỗi hoặc thiếu dữ liệu.

4. Nếu observation là danh sách paper thì hãy tổng hợp và trả lời.

5. Nếu tool đã được dùng cho đúng câu hỏi thì ưu tiên sử dụng kết quả hiện có.

====================

Ví dụ

User:
Tìm paper về Transformer

Observation:

[
"Attention Is All You Need",
"BERT",
"Vision Transformer"
]

Output

{{
    "thinking": false,
    "tool": null,
    "arguments": {{}},
    "response": "..."
}}

====================

Chỉ trả về JSON.

Schema:

{{
    "thinking": bool,
    "tool": "arxiv | wikipedia | null",
    "arguments": {{}},
    "response": string | null
}}
"""

        try:

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
                max_tokens=512,
            )

            content = completion.choices[0].message.content.strip()

            content = (
                content.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            data = json.loads(content)

            if data["tool"] == "null":
                data["tool"] = None

            return Action(**data)

        except Exception as e:

            print(e)

            return Action(
                thinking=False,
                tool=None,
                arguments={},
                response=f"LLM Error: {e}",
            )