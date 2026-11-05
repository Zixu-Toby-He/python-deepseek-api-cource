"""非流式读取推理内容和最终回答。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)

# reasoning_content 和 content 是相互独立的输出通道。
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "比较 9.11 和 9.8，说明结论。"}],
	max_tokens=1024,
	reasoning_effort="high",
	extra_body={"thinking": {"type": "enabled"}},
)
助手消息 = 响应.choices[0].message
print("[推理]\n", 助手消息.reasoning_content or "")
print("[回答]\n", 助手消息.content or "")
print("usage:", 响应.usage)
