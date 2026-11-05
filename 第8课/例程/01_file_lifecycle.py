"""上传、查询、列表文件；仅显式 --delete 时删除。"""
import argparse
import os
import pathlib

import openai


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument("image", type=pathlib.Path)
参数解析器.add_argument("--delete", action="store_true")
参数 = 参数解析器.parse_args()
if not 参数.image.is_file():
	raise FileNotFoundError(参数.image)

客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=600,
)

# 上传成功后立即查询元数据并列出最近文件。
with 参数.image.open("rb") as 文件句柄:
	已上传文件 = 客户端.files.create(file=文件句柄, purpose="user_data")
print("uploaded:", 已上传文件.id, 已上传文件.filename, 已上传文件.bytes)
文件信息 = 客户端.files.retrieve(已上传文件.id)
print("retrieved:", 文件信息.id, 文件信息.filename)
文件页 = 客户端.files.list(limit=10, order="desc", purpose="user_data")
print("recent:", [(文件.id, 文件.filename) for 文件 in 文件页.data])

# 删除具有副作用，只在调用者显式传入 --delete 时执行。
if 参数.delete:
	删除结果 = 客户端.files.delete(已上传文件.id)
	print("deleted:", 删除结果.deleted)
else:
	print("保留文件；稍后可用 file_id：", 已上传文件.id)
