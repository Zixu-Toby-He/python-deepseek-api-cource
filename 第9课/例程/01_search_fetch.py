"""调用 Search，并按需 Fetch 第一条结果。"""
import argparse
import os

import requests


参数解析器 = argparse.ArgumentParser()
参数解析器.add_argument("query")
参数解析器.add_argument("--fetch-first", action="store_true")
参数 = 参数解析器.parse_args()
工具地址 = "https://api.deepseek.com/v1/tools"
请求头 = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"}

# Search 返回排序后的结构化结果，不会自动生成回答。
搜索响应 = requests.post(
	f"{工具地址}/search",
	headers=请求头,
	json={"query": 参数.query, "count": 5, "need_content": False},
	timeout=30,
)
搜索响应.raise_for_status()
搜索结果 = 搜索响应.json()["results"]
for 序号, 结果项 in enumerate(搜索结果, 1):
	print(f"[{序号}] {结果项['title']}\n{结果项['url']}")
	print("score:", 结果项["rerank_score"], "authority:", 结果项["authority"])

# Fetch 只在显式要求且搜索有结果时抓取第一条网页。
if 参数.fetch_first and 搜索结果:
	抓取响应 = requests.post(
		f"{工具地址}/fetch",
		headers=请求头,
		json={"url": 搜索结果[0]["url"]},
		timeout=60,
	)
	抓取响应.raise_for_status()
	页面数据 = 抓取响应.json()
	print("\n#", 页面数据["title"])
	print(页面数据["content"][:3000])
