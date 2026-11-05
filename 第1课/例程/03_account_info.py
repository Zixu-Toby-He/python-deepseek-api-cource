"""查询可用模型和账户余额，不发起生成。"""
import os

import requests


基础地址 = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
请求头 = {"Authorization": f"Bearer {os.environ['DEEPSEEK_API_KEY']}"}

# 模型列表适合启动检查，不应在每次生成前重复查询。
模型响应 = requests.get(f"{基础地址}/models", headers=请求头, timeout=30)
模型响应.raise_for_status()
for 模型 in 模型响应.json()["data"]:
	print("model:", 模型["id"])

# 余额接口只读取账户状态，不会产生模型生成费用。
余额响应 = requests.get(f"{基础地址}/user/balance", headers=请求头, timeout=30)
余额响应.raise_for_status()
余额数据 = 余额响应.json()
print("is_available:", 余额数据.get("is_available"))
for 余额项 in 余额数据.get("balance_infos", []):
	print(余额项)
