"""非思考模式的客户端函数调用闭环。"""
import json
import os

import openai


def 查询天气(城市: str) -> dict:
	"""返回本地模拟天气，不访问外部系统。"""
	天气样本 = {"北京": "晴，12°C", "上海": "多云，18°C"}
	return {"city": 城市, "weather": 天气样本.get(城市, "暂无数据")}


工具定义 = [{
	"type": "function",
	"function": {
		"name": "get_weather",
		"description": "查询城市的示例天气",
		"parameters": {
			"type": "object",
			"properties": {"city": {"type": "string"}},
			"required": ["city"],
			"additionalProperties": False,
		},
	},
}]
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)
消息历史 = [{"role": "user", "content": "北京和上海天气如何？"}]

# 每一轮先让模型决定是否调用工具，再把可信执行结果回传。
for 工具轮次 in range(4):
	响应 = 客户端.chat.completions.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		messages=消息历史,
		tools=工具定义,
		max_tokens=512,
		extra_body={"thinking": {"type": "disabled"}},
	)
	助手消息 = 响应.choices[0].message
	消息历史.append(助手消息)
	if not 助手消息.tool_calls:
		print(助手消息.content)
		break
	for 工具调用 in 助手消息.tool_calls:
		if 工具调用.function.name != "get_weather":
			raise ValueError("拒绝未知工具")
		工具参数 = json.loads(工具调用.function.arguments)
		工具结果 = 查询天气(城市=str(工具参数["city"]))
		消息历史.append({
			"role": "tool",
			"tool_call_id": 工具调用.id,
			"content": json.dumps(工具结果, ensure_ascii=False),
		})
else:
	raise RuntimeError("工具调用超过最大步数")
