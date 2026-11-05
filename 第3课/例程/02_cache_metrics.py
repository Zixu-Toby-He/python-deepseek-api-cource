"""重复稳定长前缀，比较自动上下文缓存指标。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=120,
)
固定资料 = "Python 强调可读性。列表可变，元组不可变。" * 300

# 两次请求复用相同长前缀，第二次通常能观察到更多缓存命中。
for 用户问题 in ("概括核心观点。", "比较列表与元组。"):
	响应 = 客户端.chat.completions.create(
		model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
		messages=[
			{"role": "system", "content": "仅依据给定资料回答。"},
			{"role": "user", "content": f"资料：\n{固定资料}\n\n问题：{用户问题}"},
		],
		max_tokens=128,
		temperature=0,
		extra_body={"thinking": {"type": "disabled"}},
	)
	用量 = 响应.usage
	print(用户问题, 响应.choices[0].message.content)
	print(
		"hit:", getattr(用量, "prompt_cache_hit_tokens", None),
		"miss:", getattr(用量, "prompt_cache_miss_tokens", None),
	)
