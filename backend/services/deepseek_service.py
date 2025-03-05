#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DeepSeek API服务 - 集成DeepSeek API进行面试问题生成和答案评估
"""

import os
import json
import requests
from flask import current_app

# DeepSeek API配置
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '2a7e2647-866e-4eb5-9c43-fc288ebc2222')
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def deepseek_chat_completion(messages, temperature=0.7, max_tokens=2000):
    """
    调用DeepSeek API进行聊天补全
    
    Args:
        messages: 消息列表，格式为[{"role": "user", "content": "你好"}]
        temperature: 温度参数，控制随机性
        max_tokens: 最大生成token数
        
    Returns:
        API响应的JSON对象
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        current_app.logger.error(f"DeepSeek API调用失败: {str(e)}")
        return {"error": str(e)}

def generate_interview_question(interview_type, company, language, previous_questions=None, previous_answers=None, difficulty=None):
    """
    生成面试问题
    
    Args:
        interview_type: 面试类型（如"软件工程师"）
        company: 公司名称
        language: 语言（"zh"或"en"）
        previous_questions: 之前的问题列表
        previous_answers: 之前的回答列表
        difficulty: 难度级别（1-5）
        
    Returns:
        生成的问题
    """
    # 构建提示
    if language == "zh":
        prompt = f"你是{company}公司的面试官，正在面试一位{interview_type}职位的候选人。"
        if previous_questions and previous_answers:
            prompt += "基于候选人之前的回答，请生成下一个面试问题。\n\n"
            for i, (q, a) in enumerate(zip(previous_questions, previous_answers)):
                prompt += f"问题{i+1}: {q}\n回答{i+1}: {a}\n\n"
        else:
            prompt += "请生成一个合适的面试问题。"
            
        if difficulty:
            prompt += f"\n请生成难度级别为{difficulty}（1-5）的问题。"
    else:
        prompt = f"You are an interviewer from {company}, interviewing a candidate for the {interview_type} position."
        if previous_questions and previous_answers:
            prompt += "Based on the candidate's previous answers, please generate the next interview question.\n\n"
            for i, (q, a) in enumerate(zip(previous_questions, previous_answers)):
                prompt += f"Question {i+1}: {q}\nAnswer {i+1}: {a}\n\n"
        else:
            prompt += "Please generate an appropriate interview question."
            
        if difficulty:
            prompt += f"\nPlease generate a question with difficulty level {difficulty} (1-5)."
    
    # 调用DeepSeek API
    messages = [{"role": "user", "content": prompt}]
    response = deepseek_chat_completion(messages)
    
    if "error" in response:
        return {"error": response["error"]}
    
    try:
        question = response["choices"][0]["message"]["content"]
        return {"question": question}
    except (KeyError, IndexError) as e:
        return {"error": f"解析API响应失败: {str(e)}"}

def evaluate_answer(question, answer, interview_type, language="zh"):
    """
    评估面试回答
    
    Args:
        question: 面试问题
        answer: 候选人回答
        interview_type: 面试类型
        language: 语言（"zh"或"en"）
        
    Returns:
        评估结果
    """
    # 构建提示
    if language == "zh":
        prompt = f"""你是一位经验丰富的{interview_type}面试官。请评估以下面试问答：
        
问题：{question}

候选人回答：{answer}

请提供以下评估：
1. 回答质量（0-100分）
2. 优点
3. 不足
4. 改进建议
5. 是否建议继续面试（是/否）

请以JSON格式返回结果，格式如下：
{{
  "score": 分数,
  "strengths": ["优点1", "优点2", ...],
  "weaknesses": ["不足1", "不足2", ...],
  "suggestions": "改进建议",
  "continue": true/false
}}
"""
    else:
        prompt = f"""You are an experienced {interview_type} interviewer. Please evaluate the following interview Q&A:
        
Question: {question}

Candidate's Answer: {answer}

Please provide the following assessment:
1. Answer quality (0-100 points)
2. Strengths
3. Weaknesses
4. Improvement suggestions
5. Whether to continue the interview (yes/no)

Please return the result in JSON format as follows:
{{
  "score": score,
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "suggestions": "improvement suggestions",
  "continue": true/false
}}
"""
    
    # 调用DeepSeek API
    messages = [{"role": "user", "content": prompt}]
    response = deepseek_chat_completion(messages)
    
    if "error" in response:
        return {"error": response["error"]}
    
    try:
        content = response["choices"][0]["message"]["content"]
        # 尝试解析JSON
        try:
            # 查找JSON内容
            import re
            json_match = re.search(r'({[\s\S]*})', content)
            if json_match:
                json_str = json_match.group(1)
                evaluation = json.loads(json_str)
                return evaluation
            else:
                return {"error": "无法从响应中提取JSON"}
        except json.JSONDecodeError:
            return {"error": "无法解析评估结果JSON"}
    except (KeyError, IndexError) as e:
        return {"error": f"解析API响应失败: {str(e)}"} 