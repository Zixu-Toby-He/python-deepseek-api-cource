"""Beta：从指定 assistant 前缀继续生成。"""
import os

import openai


# Beta 功能必须使用带 /beta 的基础地址。
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com/beta",
	timeout=120,
)
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[
		{"role": "user", "content": "写一个带类型注解的二分查找函数。"},
		{"role": "assistant", "content": "```python\n", "prefix": True},
	],
	max_tokens=400,
	stop=["```"],
	extra_body={"thinking": {"type": "disabled"}},
)
print(响应.choices[0].message.content)
