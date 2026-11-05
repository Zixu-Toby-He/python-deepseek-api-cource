"""以本地线程池限制并发，避免瞬间压垮服务或自身。"""
import concurrent.futures
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=90,
)


def 提问(序号: int) -> tuple[int, str]:
	"""发送一个短请求，并返回原序号和模型答案。"""
	响应 = 客户端.chat.completions.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		messages=[{"role": "user", "content": f"只返回数字 {序号} 的平方。"}],
		max_tokens=20,
		extra_body={
			"thinking": {"type": "disabled"},
			"user_id": f"course_user_{序号 % 2}",
		},
	)
	return 序号, 响应.choices[0].message.content or ""


# max_workers 是客户端自己的并发上限，应低于账户和本机容量。
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as 线程池:
	待完成任务 = [线程池.submit(提问, 序号) for 序号 in range(1, 9)]
	for 已完成任务 in concurrent.futures.as_completed(待完成任务):
		序号, 助手回答 = 已完成任务.result()
		print(序号, 助手回答)
