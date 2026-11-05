"""用同一 Key 冒烟测试 Chat、Responses、Anthropic 三种协议。"""
import os

import anthropic
import openai


密钥 = os.environ["DEEPSEEK_API_KEY"]
模型名称 = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
开放接口客户端 = openai.OpenAI(
	api_key=密钥,
	base_url="https://api.deepseek.com",
	timeout=60,
)

# 依次发送极短请求，快速确认两种 OpenAI 兼容协议。
对话响应 = 开放接口客户端.chat.completions.create(
	model=模型名称,
	messages=[{"role": "user", "content": "只回答 chat-ok"}],
	max_tokens=20,
	extra_body={"thinking": {"type": "disabled"}},
)
print("chat:", 对话响应.choices[0].message.content)
项目响应 = 开放接口客户端.responses.create(
	model=模型名称,
	input="只回答 responses-ok",
	reasoning={"effort": "none"},
	max_output_tokens=20,
)
print("responses:", 项目响应.output_text)

# Anthropic 兼容协议使用独立基础地址和内容块响应。
消息客户端 = anthropic.Anthropic(
	api_key=密钥,
	base_url="https://api.deepseek.com/anthropic",
	timeout=60,
)
消息响应 = 消息客户端.messages.create(
	model=模型名称,
	max_tokens=20,
	messages=[{"role": "user", "content": "只回答 anthropic-ok"}],
	thinking={"type": "disabled"},
)
文本块 = [内容块.text for 内容块 in 消息响应.content if 内容块.type == "text"]
print("anthropic:", "".join(文本块))
