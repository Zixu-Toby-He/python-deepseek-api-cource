"""不用 SDK，观察 DeepSeek 的原始 HTTP JSON 协议。"""
import os

import requests


# 原始 HTTP 调用需要自行构造鉴权头和 JSON 请求体。
接口地址 = "https://api.deepseek.com/chat/completions"
请求头 = {
	"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}",
	"Content-Type": "application/json",
}
请求体 = {
	"model": os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	"messages": [{"role": "user", "content": "返回三个学习 API 的建议。"}],
	"max_tokens": 160,
	"temperature": 0,
	"thinking": {"type": "disabled"},
}

# raise_for_status 会把认证、余额和限速错误转成异常。
响应 = requests.post(接口地址, headers=请求头, json=请求体, timeout=60)
响应.raise_for_status()
响应数据 = 响应.json()
print(响应数据["choices"][0]["message"]["content"])
print(响应数据["usage"])
