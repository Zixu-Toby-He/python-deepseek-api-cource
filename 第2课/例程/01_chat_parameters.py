"""演示 Chat Completions 的常用非流式参数。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=60,
)

# system 消息负责长期规则，user 消息负责本轮任务。
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[
		{"role": "system", "content": "你是 Python 教师，回答不超过三点。"},
		{"role": "user", "content": "列表和生成器有什么区别？"},
	],
	max_tokens=256,
	temperature=0.2,
	stop=["第四点"],
	extra_body={
		"thinking": {"type": "disabled"},
		"user_id": "course_demo_user",
	},
)

# 截断结果不是完整答案，不能静默展示给用户。
候选结果 = 响应.choices[0]
if 候选结果.finish_reason == "length":
	raise RuntimeError("输出被截断，请扩大 max_tokens 或缩短输入")
else:
	print(候选结果.message.content)
	print("finish_reason:", 候选结果.finish_reason)
