"""按语义事件消费 Responses 流。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)
响应流 = 客户端.responses.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	input="用四句话解释事件流。",
	reasoning={"effort": "low"},
	max_output_tokens=600,
	stream=True,
)

# Responses 流以语义终止事件结束，不使用 data: [DONE]。
终止事件 = None
for 事件 in 响应流:
	if 事件.type == "response.output_text.delta":
		print(事件.delta, end="", flush=True)
	if 事件.type in {"response.completed", "response.incomplete", "response.failed"}:
		终止事件 = 事件.type
		print("\n终止事件:", 终止事件)
		print("usage:", 事件.response.usage)

if 终止事件 != "response.completed":
	raise RuntimeError(f"响应未正常完成：{终止事件}")
