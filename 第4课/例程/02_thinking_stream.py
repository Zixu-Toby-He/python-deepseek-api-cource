"""流式分别累积 reasoning_content 与 content。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)
响应流 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "为什么二分查找是 O(log n)？"}],
	reasoning_effort="low",
	stream=True,
	extra_body={"thinking": {"type": "enabled"}},
)

# 推理与最终答案分别累积，面向用户只实时打印最终答案。
推理片段 = []
回答片段 = []
for 数据块 in 响应流:
	if not 数据块.choices:
		continue
	增量 = 数据块.choices[0].delta
	推理增量 = getattr(增量, "reasoning_content", None)
	if 推理增量:
		推理片段.append(推理增量)
	if 增量.content:
		回答片段.append(增量.content)
		print(增量.content, end="", flush=True)

print("\n推理字符数:", len("".join(推理片段)))
