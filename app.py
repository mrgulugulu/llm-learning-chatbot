
from flask import Flask, request, jsonify, render_template
from main import learning_llm_chatbot_server
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/learning_llm_chatbot', methods=['POST'])
def process():
    data = request.json  # 获取 JSON 数据
    user_input = data.get('input', '')  # 提取输入内容
    prompt_input = data.get('prompt', '')
    result = learning_llm_chatbot_server(user_input, prompt_input)  # 调用处理方法
    return jsonify({'output': result})  # 返回 JSON 响应


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)  # 在所有可用的 IP 地址上运行