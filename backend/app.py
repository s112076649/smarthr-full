#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI面试模拟系统 - Web应用后端
Flask API服务入口文件
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# 导入API蓝图
from api.interview_api import interview_api
from api.speech_api import speech_api

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)  # 启用跨域请求支持

# 注册API蓝图
app.register_blueprint(interview_api, url_prefix='/api/interview')
app.register_blueprint(speech_api, url_prefix='/api/speech')

# 添加CORS响应头，确保跨域请求正常工作
@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

# API路由
@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查API"""
    return jsonify({
        'status': 'success',
        'message': 'AI面试模拟系统API服务正常运行'
    })

# 前端应用路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """提供前端React应用"""
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# 启动应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 