"""不携带 tools 时，多轮仅需回传最终回答。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)
模型名称 = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
消息历史 = [{"role": "user", "content": "9.11 和 9.8 哪个更大？"}]

# 未携带 tools 时，历史 reasoning_content 无需回传。
for 追问 in (None, "把答案改写为一句适合小学生的话。"):
	if 追问:
		消息历史.append({"role": "user", "content": 追问})
	响应 = 客户端.chat.completions.create(
		model=模型名称,
		messages=消息历史,
		reasoning_effort="high",
		extra_body={"thinking": {"type": "enabled"}},
	)
	助手回答 = 响应.choices[0].message.content or ""
	print(助手回答)
	消息历史.append({"role": "assistant", "content": 助手回答})
