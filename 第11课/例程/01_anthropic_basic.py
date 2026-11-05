"""使用 Anthropic SDK 调用 DeepSeek Messages API。"""
import os

import anthropic


客户端 = anthropic.Anthropic(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com/anthropic",
	timeout=120,
)
消息 = 客户端.messages.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	max_tokens=500,
	system="你是 API 教师，回答简洁。",
	messages=[{"role": "user", "content": "Messages API 的内容块是什么？"}],
	thinking={"type": "disabled"},
)

# Anthropic 响应由内容块组成，此处只打印 text 块。
for 内容块 in 消息.content:
	if 内容块.type == "text":
		print(内容块.text)
print("stop_reason:", 消息.stop_reason)
print("usage:", 消息.usage)
