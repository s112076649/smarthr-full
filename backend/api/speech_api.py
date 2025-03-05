#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
语音服务API模块 - 提供语音识别和合成的REST API接口
"""

from flask import Blueprint, request, jsonify, Response
import json
import base64
import time
from services.xfyun_service import text_to_speech, speech_to_text

# 创建Blueprint
speech_api = Blueprint('speech_api', __name__)

@speech_api.route('/tts', methods=['POST'])
def text_to_speech_api():
    """文本转语音API"""
    data = request.json
    
    # 验证请求数据
    if not data or 'text' not in data:
        return jsonify({
            'status': 'error',
            'message': '缺少必要参数'
        }), 400
    
    text = data.get('text')
    language = data.get('language', 'zh')
    voice = data.get('voice', 'xiaoyan')  # 默认使用讯飞小燕声音
    
    # 调用科大讯飞TTS服务
    result = text_to_speech(text, voice=voice)
    
    if not result.get('success', False):
        # 如果科大讯飞服务调用失败，返回模拟数据
        dummy_audio = base64.b64encode(b'DUMMY_AUDIO_DATA').decode('utf-8')
        return jsonify({
            'status': 'success',
            'data': {
                'audio': dummy_audio,
                'format': 'wav',
                'duration': 2.5,  # 模拟音频长度（秒）
                'source': 'mock'  # 标记为模拟数据
            }
        })
    
    # 返回真实的音频数据
    return jsonify({
        'status': 'success',
        'data': {
            'audio': result['audio'],
            'format': 'wav',
            'duration': 0,  # 实际长度未知
            'source': 'xfyun'  # 标记为讯飞数据
        }
    })

@speech_api.route('/asr', methods=['POST'])
def speech_to_text_api():
    """语音识别API"""
    # 检查是否有文件上传
    if 'audio' not in request.files:
        return jsonify({
            'status': 'error',
            'message': '未找到音频文件'
        }), 400
    
    audio_file = request.files['audio']
    language = request.form.get('language', 'zh')
    
    # 读取音频数据
    audio_data = audio_file.read()
    
    # 调用科大讯飞ASR服务
    xf_language = 'zh_cn' if language == 'zh' else 'en_us'
    result = speech_to_text(audio_data, language=xf_language)
    
    if not result.get('success', False):
        # 如果科大讯飞服务调用失败，返回模拟数据
        return jsonify({
            'status': 'success',
            'data': {
                'text': "这是一个模拟的语音识别结果",
                'confidence': 0.95,
                'source': 'mock'  # 标记为模拟数据
            }
        })
    
    # 返回真实的识别结果
    return jsonify({
        'status': 'success',
        'data': {
            'text': result['text'],
            'confidence': 0.95,  # 置信度未知，使用默认值
            'source': 'xfyun'  # 标记为讯飞数据
        }
    })

@speech_api.route('/asr/websocket', methods=['GET'])
def asr_websocket_info():
    """获取WebSocket语音识别服务信息"""
    # 提供WebSocket服务端点信息
    # 在实际实现中，前端将通过WebSocket与后端建立连接进行实时语音识别
    return jsonify({
        'status': 'success',
        'data': {
            'websocket_url': 'ws://localhost:5000/api/speech/ws',
            'protocol': 'xf-asr-1.0',
            'supported_formats': ['wav', 'pcm']
        }
    }) 