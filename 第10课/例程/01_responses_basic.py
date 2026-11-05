"""Responses API 的基础文本请求。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)

# Responses API 用 instructions 与 input 表达规则和输入。
响应 = 客户端.responses.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	instructions="你是 API 教师，回答不超过三点。",
	input="Chat Completions 和 Responses 的抽象有什么不同？",
	reasoning={"effort": "none"},
	max_output_tokens=400,
)
print(响应.output_text)
print("status:", 响应.status)
print("usage:", 响应.usage)
