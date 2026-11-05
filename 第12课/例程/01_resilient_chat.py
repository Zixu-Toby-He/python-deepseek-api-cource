"""仅对临时 API 错误做有界指数退避。"""
import os
import random
import time

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=90,
)


def 聊天(提示词: str, 最大尝试次数: int = 4) -> str:
	"""请求模型，并且只重试网络错误和临时服务错误。"""
	for 尝试序号 in range(最大尝试次数):
		try:
			响应 = 客户端.chat.completions.create(
				model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
				messages=[{"role": "user", "content": 提示词}],
				max_tokens=300,
				extra_body={"thinking": {"type": "disabled"}},
			)
			候选结果 = 响应.choices[0]
			if 候选结果.finish_reason == "length":
				raise RuntimeError("输出被截断，不自动重试")
			return 候选结果.message.content or ""
		except openai.APIStatusError as 错误:
			if 错误.status_code not in {408, 429, 500, 502, 503, 504}:
				raise
		except (openai.APITimeoutError, openai.APIConnectionError):
			pass

		# 最后一次失败后不再等待，直接离开重试循环。
		if 尝试序号 == 最大尝试次数 - 1:
			break
		等待秒数 = min(8.0, 0.5 * 2**尝试序号) + random.random() * 0.25
		time.sleep(等待秒数)
	raise RuntimeError("临时错误重试耗尽")


print(聊天("用两句话解释指数退避。"))
