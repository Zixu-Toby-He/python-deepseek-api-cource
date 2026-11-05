"""输出不含提示正文和密钥的结构化请求指标。"""
import json
import os
import time
import uuid

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=90,
)
追踪标识 = uuid.uuid4().hex
开始时间 = time.perf_counter()
响应 = 客户端.chat.completions.create(
	model=os.getenv("DEEPSEEK_MODEL", "deepseek-flash"),
	messages=[{"role": "user", "content": "一句话定义可观测性。"}],
	max_tokens=80,
	extra_body={"thinking": {"type": "disabled"}},
)

# 指标只保留运行元数据，不记录提示正文、密钥或推理内容。
耗时毫秒 = round((time.perf_counter() - 开始时间) * 1000)
候选结果 = 响应.choices[0]
用量 = 响应.usage
指标 = {
	"trace_id": 追踪标识,
	"request_id": 响应.id,
	"model": 响应.model,
	"latency_ms": 耗时毫秒,
	"finish_reason": 候选结果.finish_reason,
	"prompt_tokens": 用量.prompt_tokens,
	"completion_tokens": 用量.completion_tokens,
	"cache_hit_tokens": getattr(用量, "prompt_cache_hit_tokens", None),
}
print(候选结果.message.content)
print(json.dumps(指标, ensure_ascii=False))
