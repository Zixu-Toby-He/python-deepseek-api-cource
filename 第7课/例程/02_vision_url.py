"""使用公开图片 URL 进行视觉问答。"""
import argparse
import os

import openai


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument("url", help="公开可访问的 JPEG/PNG/GIF/WebP URL")
参数解析器.add_argument("--question", default="图片的主要内容是什么？")
参数 = 参数解析器.parse_args()

# 外部 URL 必须能被 DeepSeek 服务端公开访问。
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
			{"type": "image_url", "image_url": {
				"url": 参数.url,
				"detail": "original",
			}},
		],
	}],
	max_tokens=500,
)
print(响应.choices[0].message.content)
