"""流式打印正文，并在最终块读取累计用量。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)
响应流 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "分四步解释 SSE。"}],
	max_tokens=400,
	stream=True,
	stream_options={"include_usage": True},
	extra_body={"thinking": {"type": "disabled"}},
)

# 正文和累计用量可能出现在不同的流式块中。
用量 = None
停止原因 = None
for 数据块 in 响应流:
	if 数据块.choices:
		增量 = 数据块.choices[0].delta
		print(增量.content or "", end="", flush=True)
		停止原因 = 数据块.choices[0].finish_reason or 停止原因
	if 数据块.usage:
		用量 = 数据块.usage

print("\nfinish_reason:", 停止原因)
print("usage:", 用量)
