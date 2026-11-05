"""请求 JSON Output，并完成最基本的本地校验。"""
import json
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[
		{
			"role": "system",
			"content": "提取成绩并只输出 JSON，例如："
			'{"name":"小明","score":95}。score 必须是 0 到 100 的整数。',
		},
		{"role": "user", "content": "期末考试中，小红获得了 88 分。"},
	],
	response_format={"type": "json_object"},
	max_tokens=128,
	extra_body={"thinking": {"type": "disabled"}},
)

# 先检查截断和空白，再解析 JSON 并执行本地业务校验。
候选结果 = 响应.choices[0]
响应正文 = 候选结果.message.content or ""
if 候选结果.finish_reason == "length" or not 响应正文.strip():
	raise RuntimeError("JSON 被截断或为空")
解析数据 = json.loads(响应正文)
if not isinstance(解析数据.get("name"), str) or not 0 <= 解析数据.get("score", -1) <= 100:
	raise ValueError(f"业务字段不合法：{解析数据}")
else:
	print(解析数据)
