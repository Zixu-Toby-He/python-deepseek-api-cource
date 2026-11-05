"""客户端保存消息历史，构造无状态多轮对话。"""
import os

import openai


客户端 = openai.OpenAI(
	api_key=os.environ["DEEPSEEK_API_KEY"],
	base_url="https://api.deepseek.com",
	timeout=60,
)
模型名称 = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
消息历史 = [{"role": "system", "content": "回答简洁；不确定时明确说不知道。"}]

print("输入 exit 结束。")
while True:
	用户问题 = input("你> ").strip()
	if not 用户问题 or 用户问题.lower() == "exit":
		break
	else:
		# DeepSeek API 无状态，因此每轮都要发送需要保留的历史。
		消息历史.append({"role": "user", "content": 用户问题})
		响应 = 客户端.chat.completions.create(
			model=模型名称,
			messages=消息历史,
			max_tokens=512,
			extra_body={"thinking": {"type": "disabled"}},
		)
		助手回答 = 响应.choices[0].message.content or ""
		print("助手>", 助手回答)
		消息历史.append({"role": "assistant", "content": 助手回答})

	# 示例只保留最近十条业务消息，生产环境应按 Token 精确裁剪。
	if len(消息历史) > 12:
		消息历史 = 消息历史[:1] + 消息历史[-10:]
