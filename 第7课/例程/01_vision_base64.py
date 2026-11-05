"""把本地图片编码成 data URL 后提交。"""
import argparse
import base64
import mimetypes
import os
import pathlib

import openai


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument(
	"image",
	type=pathlib.Path,
	nargs="?",
	default=pathlib.Path(__file__).parents[1] / "素材" / "示例图.png",
)
参数解析器.add_argument("--detail", choices=["low", "original"], default="low")
参数 = 参数解析器.parse_args()
if not 参数.image.is_file():
	raise FileNotFoundError(f"请把图片放到 {参数.image}，或在命令行指定图片路径")

# 根据文件名推断 MIME，并把原始字节编码为 data URL。
媒体类型 = mimetypes.guess_type(参数.image.name)[0] or "image/jpeg"
编码内容 = base64.b64encode(参数.image.read_bytes()).decode("ascii")
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
			{"type": "text", "text": "描述图片；不确定的细节请明确说明。"},
			{"type": "image_url", "image_url": {
				"url": f"data:{媒体类型};base64,{编码内容}",
				"detail": 参数.detail,
			}},
		],
	}],
	max_tokens=500,
)
print(响应.choices[0].message.content)
print("usage:", 响应.usage)
