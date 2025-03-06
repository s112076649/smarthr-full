#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
面试API模块 - 提供面试流程的REST API接口
"""

from flask import Blueprint, request, jsonify
import json
import time
from services.deepseek_service import generate_interview_question, evaluate_answer

# 创建Blueprint
interview_api = Blueprint('interview_api', __name__)

# 模拟面试数据（后期将从数据库获取）
INTERVIEW_TYPES = {
    'software_engineer': '软件工程师',
    'product_manager': '产品经理',
    'data_scientist': '数据科学家',
    'frontend_developer': '前端开发工程师',
    'backend_developer': '后端开发工程师'
}

# API端点
@interview_api.route('/types', methods=['GET'])
def get_interview_types():
    """获取可用的面试类型"""
    return jsonify({
        'status': 'success',
        'data': INTERVIEW_TYPES
    })

@interview_api.route('/start', methods=['POST'])
def start_interview():
    """开始新面试"""
    data = request.json
    
    # 验证请求数据
    if not data or 'type' not in data:
        return jsonify({
            'status': 'error',
            'message': '缺少必要参数'
        }), 400
    
    interview_type = data.get('type')
    company_name = data.get('company', '')
    language = data.get('language', 'zh')
    use_ml = data.get('use_ml', True)
    
    # 创建面试会话（后期将使用数据库存储）
    interview_id = f"interview_{int(time.time())}"
    
    # 返回面试会话信息
    return jsonify({
        'status': 'success',
        'data': {
            'interview_id': interview_id,
            'type': interview_type,
            'company': company_name,
            'language': language,
            'use_ml': use_ml,
            'start_time': time.time()
        }
    })

@interview_api.route('/question', methods=['GET'])
def get_question():
    """获取面试问题"""
    interview_id = request.args.get('interview_id')
    
    if not interview_id:
        return jsonify({
            'status': 'error',
            'message': '缺少面试ID'
        }), 400
    
    try:
        # 从URL参数中获取面试类型和公司名称
        interview_type = request.args.get('type', 'software_engineer')
        company = request.args.get('company', '某科技公司')
        language = request.args.get('language', 'zh')
        
        # 调用DeepSeek API生成问题
        result = generate_interview_question(interview_type, company, language)
        
        if result and 'question' in result:
            question = {
                'id': f'q_{int(time.time())}',
                'content': result['question'],
                'type': result.get('type', 'technical'),
                'difficulty': result.get('difficulty', 3)
            }
        else:
            # 如果API调用失败，使用备用问题
            question = {
                'id': f'q_{int(time.time())}',
                'content': '请简单介绍一下你自己以及你的技术背景。',
                'type': 'open',
                'difficulty': 1
            }
        
        return jsonify({
            'status': 'success',
            'data': question
        })
    except Exception as e:
        print(f"生成问题时出错: {str(e)}")
        # 出错时使用备用问题
        question = {
            'id': f'q_{int(time.time())}',
            'content': '请简单介绍一下你自己以及你的技术背景。',
            'type': 'open',
            'difficulty': 1
        }
        
        return jsonify({
            'status': 'success',
            'data': question
        })

@interview_api.route('/answer', methods=['POST'])
def submit_answer():
    """提交面试答案"""
    data = request.json
    
    # 验证请求数据
    if not data or 'interview_id' not in data or 'question_id' not in data or 'answer' not in data:
        return jsonify({
            'status': 'error',
            'message': '缺少必要参数'
        }), 400
    
    # 提取数据
    interview_id = data.get('interview_id')
    question_id = data.get('question_id')
    answer = data.get('answer')
    question = data.get('question', '')
    interview_type = data.get('type', 'software_engineer')
    language = data.get('language', 'zh')
    
    try:
        # 调用DeepSeek API评估答案
        result = evaluate_answer(question, answer, interview_type, language)
        
        if result and not 'error' in result:
            analysis = {
                'quality': result.get('score', 80) / 100,  # 转换为0-1范围
                'feedback': result.get('suggestions', ''),
                'strengths': result.get('strengths', []),
                'weaknesses': result.get('weaknesses', []),
                'next_question': result.get('continue', True)
            }
        else:
            # 如果API调用失败，使用备用评估
            analysis = {
                'quality': 0.8,
                'feedback': '回答完整，展示了相关经验，但可以更具体地列举项目案例。',
                'strengths': ['表达清晰', '基础知识扎实'],
                'weaknesses': ['缺少具体例子', '回答不够深入'],
                'next_question': True
            }
        
        return jsonify({
            'status': 'success',
            'data': analysis
        })
    except Exception as e:
        print(f"评估答案时出错: {str(e)}")
        # 出错时使用备用评估
        analysis = {
            'quality': 0.8,
            'feedback': '回答完整，展示了相关经验，但可以更具体地列举项目案例。',
            'strengths': ['表达清晰', '基础知识扎实'],
            'weaknesses': ['缺少具体例子', '回答不够深入'],
            'next_question': True
        }
        
        return jsonify({
            'status': 'success',
            'data': analysis
        })

@interview_api.route('/evaluate', methods=['GET'])
def get_evaluation():
    """获取面试总体评估"""
    interview_id = request.args.get('interview_id')
    
    if not interview_id:
        return jsonify({
            'status': 'error',
            'message': '缺少面试ID'
        }), 400
    
    # 模拟评估生成（后期将集成现有的评估生成逻辑）
    evaluation = {
        'score': 85,
        'summary': '面试表现良好，技术基础扎实，沟通流畅。可以更好地展示项目经验和解决问题的能力。',
        'strengths': ['技术知识全面', '表达清晰', '逻辑思维好'],
        'weaknesses': ['项目经验描述不够具体', '对某些技术细节掌握不够深入'],
        'suggestions': '建议在回答中加入更多具体的项目案例和数据，展示解决复杂问题的能力。'
    }
    
    return jsonify({
        'status': 'success',
        'data': evaluation
    }) 