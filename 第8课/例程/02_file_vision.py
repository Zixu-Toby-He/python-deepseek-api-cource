"""引用已经上传的 file_id 进行视觉问答。"""
import argparse
import os

import openai


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument("file_id", help="形如 file-api-...")
参数解析器.add_argument("--question", default="描述这张图片的主要信息。")
参数 = 参数解析器.parse_args()
if not 参数.file_id.startswith("file-api-"):
	raise ValueError("file_id 格式不正确")

# file_id 引用已上传图片，避免在每次请求中重复编码文件。
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=180,
)
响应 = 客户端.chat.completions.create(
	model="deepseek-flash",
	messages=[{
		"role": "user",
		"content": [
			{"type": "text", "text": 参数.question},
			{"type": "file", "file_id": 参数.file_id},
		],
	}],
	max_tokens=500,
)
print(响应.choices[0].message.content)
