#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
科大讯飞语音服务 - 集成科大讯飞API进行语音合成和识别
"""

import os
import time
import base64
import hashlib
import hmac
import json
import requests
from urllib.parse import urlencode
from datetime import datetime
from flask import current_app

# 科大讯飞API配置
XFYUN_APP_ID = os.environ.get('XFYUN_APP_ID', '')
XFYUN_API_KEY = os.environ.get('XFYUN_API_KEY', '')
XFYUN_API_SECRET = os.environ.get('XFYUN_API_SECRET', '')

# TTS配置
TTS_URL = "https://tts-api.xfyun.cn/v2/tts"

# ASR配置
ASR_URL = "https://iat-api.xfyun.cn/v2/iat"

def generate_tts_auth_params():
    """
    生成科大讯飞TTS接口鉴权参数
    """
    # 当前时间戳
    now = int(time.time())
    # 有效期2小时
    expires = now + 7200
    
    # 拼接字符串
    host = "tts-api.xfyun.cn"
    date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = f"host: {host}\ndate: {date}\nGET /v2/tts HTTP/1.1"
    
    # 使用hmac-sha256算法结合apiSecret对上面的signature_origin签名
    signature_sha = hmac.new(
        XFYUN_API_SECRET.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    # 将签名结果进行base64编码
    signature = base64.b64encode(signature_sha).decode('utf-8')
    
    # 拼接authorization
    authorization_origin = f'api_key="{XFYUN_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
    
    # 返回鉴权参数
    return {
        "authorization": authorization,
        "date": date,
        "host": host
    }

def text_to_speech(text, voice="xiaoyan", speed=50, volume=50, pitch=50):
    """
    调用科大讯飞TTS接口将文本转换为语音
    
    Args:
        text: 要转换的文本
        voice: 发音人，默认为"xiaoyan"
        speed: 语速，范围：[0,100]，默认为50
        volume: 音量，范围：[0,100]，默认为50
        pitch: 音高，范围：[0,100]，默认为50
        
    Returns:
        音频数据的base64编码
    """
    if not XFYUN_APP_ID or not XFYUN_API_KEY or not XFYUN_API_SECRET:
        current_app.logger.warning("科大讯飞API配置缺失，使用模拟数据")
        return {"success": False, "error": "科大讯飞API配置缺失"}
    
    try:
        # 获取鉴权参数
        auth_params = generate_tts_auth_params()
        
        # 构建请求URL
        url = f"{TTS_URL}?{urlencode(auth_params)}"
        
        # 构建请求体
        body = {
            "common": {
                "app_id": XFYUN_APP_ID
            },
            "business": {
                "aue": "raw",  # 音频编码，raw：未压缩的pcm
                "sfl": 1,      # 是否开启流式返回
                "auf": "audio/L16;rate=16000",  # 音频采样率
                "vcn": voice,  # 发音人
                "speed": speed,  # 语速
                "volume": volume,  # 音量
                "pitch": pitch,  # 音高
                "tte": "UTF8"  # 文本编码
            },
            "data": {
                "text": base64.b64encode(text.encode('utf-8')).decode('utf-8'),
                "status": 2  # 2表示完整的text
            }
        }
        
        # 发送请求
        response = requests.post(url, json=body)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        if result["code"] != 0:
            return {"success": False, "error": result["message"]}
        
        # 提取音频数据
        audio_data = base64.b64decode(result["data"]["audio"])
        return {"success": True, "audio": base64.b64encode(audio_data).decode('utf-8')}
    
    except Exception as e:
        current_app.logger.error(f"科大讯飞TTS调用失败: {str(e)}")
        return {"success": False, "error": str(e)}

def generate_asr_auth_params():
    """
    生成科大讯飞ASR接口鉴权参数
    """
    # 当前时间戳
    now = int(time.time())
    # 有效期2小时
    expires = now + 7200
    
    # 拼接字符串
    host = "iat-api.xfyun.cn"
    date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature_origin = f"host: {host}\ndate: {date}\nPOST /v2/iat HTTP/1.1"
    
    # 使用hmac-sha256算法结合apiSecret对上面的signature_origin签名
    signature_sha = hmac.new(
        XFYUN_API_SECRET.encode('utf-8'),
        signature_origin.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    # 将签名结果进行base64编码
    signature = base64.b64encode(signature_sha).decode('utf-8')
    
    # 拼接authorization
    authorization_origin = f'api_key="{XFYUN_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
    
    # 返回鉴权参数
    return {
        "authorization": authorization,
        "date": date,
        "host": host
    }

def speech_to_text(audio_data, language="zh_cn"):
    """
    调用科大讯飞ASR接口将语音转换为文本
    
    Args:
        audio_data: 音频数据（二进制）
        language: 语言，默认为"zh_cn"
        
    Returns:
        识别结果
    """
    if not XFYUN_APP_ID or not XFYUN_API_KEY or not XFYUN_API_SECRET:
        current_app.logger.warning("科大讯飞API配置缺失，使用模拟数据")
        return {"success": False, "error": "科大讯飞API配置缺失"}
    
    try:
        # 获取鉴权参数
        auth_params = generate_asr_auth_params()
        
        # 构建请求URL
        url = f"{ASR_URL}?{urlencode(auth_params)}"
        
        # 构建请求体
        body = {
            "common": {
                "app_id": XFYUN_APP_ID
            },
            "business": {
                "language": language,  # 语种
                "domain": "iat",       # 领域
                "accent": "mandarin",  # 方言，普通话
                "vad_eos": 3000        # 静默检测（毫秒）
            },
            "data": {
                "status": 2,           # 2表示最后一帧
                "format": "audio/L16;rate=16000",
                "encoding": "raw",
                "audio": base64.b64encode(audio_data).decode('utf-8')
            }
        }
        
        # 发送请求
        response = requests.post(url, json=body)
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        if result["code"] != 0:
            return {"success": False, "error": result["message"]}
        
        # 提取识别结果
        text = ""
        for item in result["data"]["result"]["ws"]:
            for word in item["cw"]:
                text += word["w"]
        
        return {"success": True, "text": text}
    
    except Exception as e:
        current_app.logger.error(f"科大讯飞ASR调用失败: {str(e)}")
        return {"success": False, "error": str(e)} 