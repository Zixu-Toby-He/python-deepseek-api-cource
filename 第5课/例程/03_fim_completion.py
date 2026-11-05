"""Beta：根据函数前缀和后缀补全中间代码。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com/beta",
	timeout=120,
)

# prompt 与 suffix 之间的空白位置由模型补全。
响应 = 客户端.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	prompt="def fib(n: int) -> int:\n\t",
	suffix="\n\treturn fib(n - 1) + fib(n - 2)\n",
	max_tokens=128,
	temperature=0,
	stop=["\ndef "],
)
print(响应.choices[0].text)
