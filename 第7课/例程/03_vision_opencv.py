"""将 OpenCV 图像编码为图片字节，再通过 Base64 或 Files API 发送。"""
import argparse
import base64
import io
import os
import pathlib

import cv2
import openai


def 编码图片(图片, 图片格式: str) -> tuple[bytes, str, str]:
	"""把 BGR 像素矩阵编码成受支持的图片文件格式。"""
	扩展名 = ".jpg" if 图片格式 == "jpg" else ".png"
	媒体类型 = "image/jpeg" if 图片格式 == "jpg" else "image/png"
	编码参数 = [cv2.IMWRITE_JPEG_QUALITY, 85] if 图片格式 == "jpg" else []
	编码成功, 编码缓冲区 = cv2.imencode(扩展名, 图片, 编码参数)
	if not 编码成功:
		raise RuntimeError("OpenCV 图片编码失败")
	return 编码缓冲区.tobytes(), 媒体类型, f"opencv-image{扩展名}"


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument(
	"image",
	type=pathlib.Path,
	nargs="?",
	default=pathlib.Path(__file__).parents[1] / "素材" / "示例图.png",
)
参数解析器.add_argument("--format", choices=["jpg", "png"], default="jpg")
参数解析器.add_argument("--transport", choices=["base64", "files"], default="base64")
参数解析器.add_argument("--detail", choices=["low", "original"], default="low")
参数 = 参数解析器.parse_args()

# cv2.imread 返回 BGR ndarray；imencode 可直接正确编码，无需转换 RGB。
图片 = cv2.imread(str(参数.image), cv2.IMREAD_UNCHANGED)
if 图片 is None:
	raise FileNotFoundError(f"OpenCV 无法读取图片：{参数.image}")
图片字节, 媒体类型, 文件名 = 编码图片(图片, 参数.format)
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=600,
)

# JSON 请求使用 Base64；需要复用时则上传内存文件并引用 file_id。
if 参数.transport == "base64":
	Base64文本 = base64.b64encode(图片字节).decode("ascii")
	图片块 = {
		"type": "image_url",
		"image_url": {
			"url": f"data:{媒体类型};base64,{Base64文本}",
			"detail": 参数.detail,
		},
	}
else:
	内存文件 = io.BytesIO(图片字节)
	内存文件.name = 文件名
	上传结果 = 客户端.files.create(file=内存文件, purpose="user_data")
	图片块 = {"type": "file", "file_id": 上传结果.id}
	print("已上传 file_id：", 上传结果.id)

响应 = 客户端.chat.completions.create(
	model="deepseek-flash",
	messages=[{
		"role": "user",
		"content": [
			{"type": "text", "text": "描述图片；不确定的细节请明确说明。"},
			图片块,
		],
	}],
	max_tokens=500,
)
print(响应.choices[0].message.content)
print("编码字节数：", len(图片字节), "usage：", 响应.usage)
