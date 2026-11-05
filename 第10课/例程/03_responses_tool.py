"""Responses API 的 function_call / function_call_output。"""
import json
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)
工具定义 = [{
	"type": "function",
	"name": "convert_celsius",
	"description": "把摄氏度转换为华氏度",
	"parameters": {
		"type": "object",
		"properties": {"value": {"type": "number"}},
		"required": ["value"],
		"additionalProperties": False,
	},
}]
输入项目 = [{"role": "user", "content": "20 摄氏度等于多少华氏度？"}]

# function_call 与 function_call_output 使用相同 call_id 配对。
for 工具轮次 in range(3):
	响应 = 客户端.responses.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		input=输入项目,
		tools=工具定义,
		reasoning={"effort": "none"},
	)
	工具调用列表 = [项目 for 项目 in 响应.output if 项目.type == "function_call"]
	if not 工具调用列表:
		print(响应.output_text)
		break
	输入项目.extend(项目.model_dump(exclude_none=True) for 项目 in 响应.output)
	for 工具调用 in 工具调用列表:
		if 工具调用.name != "convert_celsius":
			raise ValueError("拒绝未知工具")
		摄氏温度 = float(json.loads(工具调用.arguments)["value"])
		输入项目.append({
			"type": "function_call_output",
			"call_id": 工具调用.call_id,
			"output": json.dumps({"fahrenheit": 摄氏温度 * 9 / 5 + 32}),
		})
else:
	raise RuntimeError("工具循环超过上限")
