"""使用 strict JSON Schema 约束工具参数。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)
工具定义 = [{
	"type": "function",
	"function": {
		"name": "create_ticket",
		"description": "创建支持工单；仅生成参数，不真正写入系统",
		"strict": True,
		"parameters": {
			"type": "object",
			"properties": {
				"title": {"type": "string"},
				"priority": {"type": "string", "enum": ["low", "medium", "high"]},
			},
			"required": ["title", "priority"],
			"additionalProperties": False,
		},
	},
}]

# 示例仅检查模型生成的参数，不执行真实工单写入。
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "登录完全不可用，请建立工单。"}],
	tools=工具定义,
	tool_choice={"type": "function", "function": {"name": "create_ticket"}},
	extra_body={"thinking": {"type": "disabled"}},
)
for 工具调用 in 响应.choices[0].message.tool_calls or []:
	print(工具调用.function.name, 工具调用.function.arguments)
