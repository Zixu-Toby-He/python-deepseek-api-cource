"""Anthropic SDK 流式文本；最终消息携带累计用量。"""
import os

import anthropic


客户端 = anthropic.Anthropic(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com/anthropic",
	timeout=300,
)

# SDK 负责解析 SSE；最终消息包含停止原因和累计用量。
with 客户端.messages.stream(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	max_tokens=800,
	messages=[{"role": "user", "content": "用三点解释 Anthropic 流事件。"}],
	thinking={"type": "disabled"},
) as 响应流:
	for 文本增量 in 响应流.text_stream:
		print(文本增量, end="", flush=True)
	最终消息 = 响应流.get_final_message()

print("\nstop_reason:", 最终消息.stop_reason)
print("usage:", 最终消息.usage)
