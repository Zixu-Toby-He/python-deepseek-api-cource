"""Anthropic 的 tool_use / tool_result 闭环。"""
import json
import os

import anthropic


客户端 = anthropic.Anthropic(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com/anthropic",
	timeout=120,
)
工具定义 = [{
	"name": "lookup_stock",
	"description": "查询示例库存，不连接真实数据库",
	"input_schema": {
		"type": "object",
		"properties": {"sku": {"type": "string"}},
		"required": ["sku"],
	},
}]
消息历史 = [{"role": "user", "content": "SKU A-100 还有库存吗？"}]

# tool_result 必须紧跟在 user 消息中，并匹配 tool_use_id。
for 工具轮次 in range(3):
	消息 = 客户端.messages.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		max_tokens=500,
		messages=消息历史,
		tools=工具定义,
		thinking={"type": "disabled"},
	)
	消息历史.append({"role": "assistant", "content": 消息.content})
	工具调用列表 = [内容块 for 内容块 in 消息.content if 内容块.type == "tool_use"]
	if not 工具调用列表:
		for 内容块 in 消息.content:
			if 内容块.type == "text":
				print(内容块.text)
		break
	工具结果列表 = []
	for 工具调用 in 工具调用列表:
		if 工具调用.name != "lookup_stock":
			raise ValueError("拒绝未知工具")
		工具结果 = {"sku": 工具调用.input["sku"], "quantity": 12}
		工具结果列表.append({
			"type": "tool_result",
			"tool_use_id": 工具调用.id,
			"content": json.dumps(工具结果, ensure_ascii=False),
		})
	消息历史.append({"role": "user", "content": 工具结果列表})
else:
	raise RuntimeError("工具循环超过上限")
