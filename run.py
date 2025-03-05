#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI面试模拟系统 - Web应用版启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import signal
import platform

# 进程列表
processes = []

def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    
    # 检查是否存在requirements.txt
    req_file = os.path.join(backend_dir, 'requirements.txt')
    if os.path.exists(req_file):
        print("正在安装后端依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=True)
    
    # 启动Flask应用
    os.chdir(backend_dir)
    if platform.system() == 'Windows':
        process = subprocess.Popen([sys.executable, "app.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        process = subprocess.Popen([sys.executable, "app.py"])
    
    processes.append(process)
    print("✓ 后端服务已启动")
    return process

def start_frontend_dev():
    """启动前端开发服务器"""
    print("正在启动前端开发服务器...")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    
    # 检查是否已安装依赖
    node_modules = os.path.join(frontend_dir, 'node_modules')
    if not os.path.exists(node_modules):
        print("正在安装前端依赖（这可能需要几分钟时间）...")
        os.chdir(frontend_dir)
        if platform.system() == 'Windows':
            subprocess.run(["npm", "install"], shell=True, check=True)
        else:
            subprocess.run(["npm", "install"], check=True)
    
    # 启动开发服务器
    os.chdir(frontend_dir)
    if platform.system() == 'Windows':
        process = subprocess.Popen(["npm", "start"], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        process = subprocess.Popen(["npm", "start"])
    
    processes.append(process)
    print("✓ 前端开发服务器已启动")
    return process

def open_browser():
    """打开浏览器访问应用"""
    print("正在打开浏览器...")
    time.sleep(5)  # 等待服务器启动
    webbrowser.open('http://localhost:3000')

def signal_handler(sig, frame):
    """处理终止信号"""
    print("\n正在关闭所有服务...")
    for process in processes:
        if platform.system() == 'Windows':
            process.kill()
        else:
            process.terminate()
    sys.exit(0)

def main():
    """主函数"""
    print("="*50)
    print("AI面试模拟系统 - Web应用版")
    print("="*50)
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # 启动后端
        backend_process = start_backend()
        
        # 启动前端
        frontend_process = start_frontend_dev()
        
        # 打开浏览器
        threading.Thread(target=open_browser).start()
        
        print("\n应用已启动！")
        print("- 前端地址: http://localhost:3000")
        print("- 后端API: http://localhost:5000")
        print("\n按Ctrl+C停止服务\n")
        
        # 等待进程结束
        backend_process.wait()
        
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"启动失败: {str(e)}")
        signal_handler(None, None)

if __name__ == "__main__":
    main() 