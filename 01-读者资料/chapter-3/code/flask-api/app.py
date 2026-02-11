"""
Flask AI API 示例

来源：《动手做 AI Agent：零基础玩转智能体》
章节：第3章 API 开发相关
行号：第 6000-6200 行
页码：第 XX 页

用途：创建一个简单的 AI API 服务

安装：
    pip install Flask openai python-dotenv

运行：
    python app.py
"""

from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
)


@app.route("/health", methods=["GET"])
def health_check():
    """健康检查"""
    return jsonify({"status": "healthy", "service": "AI Agent API"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    聊天对话接口

    请求体示例：
    {
        "message": "你好",
        "model": "gpt-4",
        "temperature": 0.7
    }
    """
    data = request.json

    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    try:
        response = client.chat.completions.create(
            model=data.get("model", "gpt-4"),
            messages=[
                {"role": "system", "content": "你是一个有帮助的AI助手。"},
                {"role": "user", "content": data["message"]}
            ],
            temperature=data.get("temperature", 0.7),
            max_tokens=1000
        )

        return jsonify({
            "response": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stream", methods=["POST"])
def stream_chat():
    """
    流式输出接口

    使用 Server-Sent Events (SSE) 返回流式响应
    """
    from flask import Response
    import json

    data = request.json

    def generate():
        stream = client.chat.completions.create(
            model=data.get("model", "gpt-4"),
            messages=[{"role": "user", "content": data["message"]}],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True
    )
