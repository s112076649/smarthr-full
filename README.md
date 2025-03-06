# AI面试模拟系统 - Web应用版

AI面试模拟系统是一个基于人工智能的面试练习平台，帮助求职者提升面试技巧和表现。Web应用版支持在任何设备上使用，无需安装任何软件。

## 功能特点

- **多行业面试场景**：支持软件工程师、产品经理、数据科学家等多种职位的面试模拟
- **机器学习优化**：根据用户回答自动调整问题难度和方向，提供个性化面试体验
- **语音交互**：支持语音识别和合成，模拟真实面试场景
- **多语言支持**：支持中英文面试
- **专业评估反馈**：每次面试后获得详细的评估报告，包括优势、不足和改进建议
- **响应式设计**：适配手机、平板和电脑等各种设备

## 技术架构

### 前端
- React.js
- Material UI
- Axios
- RecordRTC (语音录制)

### 后端
- Flask
- DeepSeek API (面试问题生成和答案评估)
- 科大讯飞API (语音识别和合成)

## 开发环境设置

### 后端设置

1. 安装Python依赖：

```bash
cd ai_interview_web/backend
pip install -r requirements.txt
```

2. 设置环境变量：

```bash
# DeepSeek API密钥
export DEEPSEEK_API_KEY=your_deepseek_api_key

# 科大讯飞API配置（可选）
export XFYUN_APP_ID=your_xfyun_app_id
export XFYUN_API_KEY=your_xfyun_api_key
export XFYUN_API_SECRET=your_xfyun_api_secret
```

3. 启动后端服务：

```bash
python app.py
```

### 前端设置

1. 安装Node.js依赖：

```bash
cd ai_interview_web/frontend
npm install
```

2. 启动开发服务器：

```bash
npm start
```

## 部署指南

### 后端部署

1. 使用Gunicorn作为WSGI服务器：

```bash
pip install gunicorn
cd ai_interview_web/backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. 配置Nginx反向代理（推荐）

### 前端部署

1. 构建生产版本：

```bash
cd ai_interview_web/frontend
npm run build
```

2. 将构建文件部署到Web服务器或CDN

## API文档

### 面试API

- `GET /api/interview/types` - 获取可用的面试类型
- `POST /api/interview/start` - 开始新面试
- `GET /api/interview/question` - 获取面试问题
- `POST /api/interview/answer` - 提交面试答案
- `GET /api/interview/evaluate` - 获取面试总体评估

### 语音API

- `POST /api/speech/tts` - 文本转语音
- `POST /api/speech/asr` - 语音识别
- `GET /api/speech/asr/websocket` - 获取WebSocket语音识别服务信息

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件

## 联系方式

如有任何问题或建议，请通过以下方式联系我们：

- 项目主页：https://github.com/s112076649/smarthr-interview.git
- 电子邮件：Kevinhuang98321@gmail.com

## 更新日志

- 2024-03-06: 修复了构建问题，移除了 SpeedInsights 组件 