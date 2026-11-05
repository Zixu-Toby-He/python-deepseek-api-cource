"""首次使用 OpenAI SDK 调用 DeepSeek。"""
import os

import openai


# 客户端只从环境变量读取密钥，避免把凭据写入源码。
客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
	timeout=60.0,
)

# 显式关闭思考模式，得到延迟较低的入门响应。
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "用一句话解释什么是 API。"}],
	max_tokens=128,
	temperature=0,
	extra_body={"thinking": {"type": "disabled"}},
)

候选结果 = 响应.choices[0]
print(候选结果.message.content)
print("finish_reason:", 候选结果.finish_reason)
print("usage:", 响应.usage)
