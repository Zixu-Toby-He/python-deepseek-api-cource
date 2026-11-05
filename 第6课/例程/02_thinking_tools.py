"""思考模式下原样回传 assistant 消息（含 reasoning_content）。"""
import datetime
import json
import os

import openai


工具定义 = [{
	"type": "function",
	"function": {
		"name": "get_date",
		"description": "返回今天日期",
		"parameters": {"type": "object", "properties": {}},
	},
}]
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=300,
)
消息历史 = [{"role": "user", "content": "今天日期是什么？一周后是哪天？"}]

# 直接追加完整 assistant 消息，确保 reasoning_content 不会丢失。
for 工具轮次 in range(4):
	响应 = 客户端.chat.completions.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		messages=消息历史,
		tools=工具定义,
		reasoning_effort="high",
		extra_body={"thinking": {"type": "enabled"}},
	)
	助手消息 = 响应.choices[0].message
	消息历史.append(助手消息)
	if not 助手消息.tool_calls:
		print(助手消息.content)
		break
	for 工具调用 in 助手消息.tool_calls:
		if 工具调用.function.name != "get_date":
			raise ValueError("拒绝未知工具")
		json.loads(工具调用.function.arguments)
		消息历史.append({
			"role": "tool",
			"tool_call_id": 工具调用.id,
			"content": datetime.date.today().isoformat(),
		})
else:
	raise RuntimeError("工具调用超过最大步数")
