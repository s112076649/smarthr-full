from http.server import BaseHTTPRequestHandler
import json
import os
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode
from datetime import datetime

# 科大讯飞API配置
XFYUN_APP_ID = os.environ.get('XFYUN_APP_ID', '')
XFYUN_API_KEY = os.environ.get('XFYUN_API_KEY', '')
XFYUN_API_SECRET = os.environ.get('XFYUN_API_SECRET', '')

# TTS配置
TTS_URL = "https://tts-api.xfyun.cn/v2/tts"

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
    
    # 进行hmac-sha256签名
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
        print("科大讯飞API配置缺失，使用模拟数据")
        return {"success": False, "error": "科大讯飞API配置缺失"}
    
    try:
        # 获取鉴权参数
        print(f"开始调用科大讯飞TTS服务，文本长度: {len(text)}")
        print(f"科大讯飞配置: APP_ID={XFYUN_APP_ID[:4] if XFYUN_APP_ID else ''}..., API_KEY={XFYUN_API_KEY[:4] if XFYUN_API_KEY else ''}...")
        
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
        print(f"发送TTS请求到: {url}")
        
        response = requests.post(url, json=body)
        print(f"TTS响应状态码: {response.status_code}")
        
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        print(f"TTS响应结果: code={result.get('code')}, message={result.get('message', '')}")
        
        if result["code"] != 0:
            print(f"TTS调用失败: {result['message']}")
            return {"success": False, "error": result["message"]}
        
        # 提取音频数据
        audio_data = base64.b64decode(result["data"]["audio"])
        return {"success": True, "audio": base64.b64encode(audio_data).decode('utf-8')}
    
    except Exception as e:
        print(f"科大讯飞TTS调用失败: {str(e)}")
        return {"success": False, "error": str(e)}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # 验证请求数据
        if not data or 'text' not in data:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': '缺少必要参数'
            }).encode('utf-8'))
            return
        
        text = data.get('text')
        language = data.get('language', 'zh')
        voice = data.get('voice', 'xiaoyan')  # 默认使用讯飞小燕声音
        
        # 调用科大讯飞TTS服务
        result = text_to_speech(text, voice=voice)
        
        if not result.get('success', False):
            # 如果科大讯飞服务调用失败，返回模拟数据
            dummy_audio = base64.b64encode(b'DUMMY_AUDIO_DATA').decode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'success',
                'data': {
                    'audio': dummy_audio,
                    'format': 'wav',
                    'duration': 2.5,  # 模拟音频长度（秒）
                    'source': 'mock'  # 标记为模拟数据
                }
            }).encode('utf-8'))
            return
        
        # 返回真实的音频数据
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'success',
            'data': {
                'audio': result['audio'],
                'format': 'wav',
                'duration': 0,  # 实际长度未知
                'source': 'xfyun'  # 标记为讯飞数据
            }
        }).encode('utf-8')) 