# 主应用入口

import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from components.sql_generator import SQLGenerator
from components.flowchart import FlowChart

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 初始化组件
api_key = os.getenv('QWEN_API_KEY')
model_url = os.getenv('QWEN_MODEL_URL')
if not api_key:
    print("警告: 未找到Qwen API密钥，请在.env文件中设置QWEN_API_KEY")
sql_generator = SQLGenerator(api_key=api_key, model_url=model_url)
flowchart = FlowChart()

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/generate_sql', methods=['POST'])
def generate_sql():
    """根据自然语言生成SQL"""
    data = request.json
    natural_language = data.get('natural_language', '')
    schema = data.get('schema', None)

    if not natural_language:
        return jsonify({'error': '请提供自然语言描述'}), 400

    # 生成SQL
    sql = sql_generator.generate_sql(natural_language, schema)

    # 解析SQL为步骤
    steps = sql_generator.parse_sql_to_steps(sql)

    # 创建流程图
    flowchart.from_sql_steps(steps)

    return jsonify({
        'sql': sql,
        'steps': steps,
        'flowchart': flowchart.to_dict()
    })

@app.route('/update_flowchart', methods=['POST'])
def update_flowchart():
    """更新流程图并重新生成SQL"""
    data = request.json
    steps = data.get('steps', [])

    if not steps:
        return jsonify({'error': '请提供流程步骤'}), 400

    # 更新流程图
    flowchart.from_sql_steps(steps)

    # 重新生成SQL
    sql = sql_generator.generate_sql_from_steps(steps)

    return jsonify({
        'sql': sql,
        'flowchart': flowchart.to_dict()
    })

@app.route('/add_step', methods=['POST'])
def add_step():
    """添加新步骤"""
    data = request.json
    step_type = data.get('step_type', 'process')
    description = data.get('description', '')
    after_id = data.get('after_id', None)

    if not description:
        return jsonify({'error': '请提供步骤描述'}), 400

    # 添加步骤
    new_id = flowchart.add_step(step_type, description, after_id)

    # 获取所有步骤
    steps = flowchart.get_steps_for_sql()

    # 重新生成SQL
    sql = sql_generator.generate_sql_from_steps(steps)

    return jsonify({
        'sql': sql,
        'flowchart': flowchart.to_dict(),
        'new_step_id': new_id
    })

@app.route('/update_step', methods=['POST'])
def update_step():
    """更新步骤"""
    data = request.json
    step_id = data.get('step_id', '')
    new_text = data.get('new_text', '')
    new_type = data.get('new_type', None)

    if not step_id or not new_text:
        return jsonify({'error': '请提供步骤ID和新文本'}), 400

    # 更新步骤
    success = flowchart.update_step(step_id, new_text, new_type)

    if not success:
        return jsonify({'error': '未找到指定步骤'}), 404

    # 获取所有步骤
    steps = flowchart.get_steps_for_sql()

    # 重新生成SQL
    sql = sql_generator.generate_sql_from_steps(steps)

    return jsonify({
        'sql': sql,
        'flowchart': flowchart.to_dict()
    })

@app.route('/remove_step', methods=['POST'])
def remove_step():
    """删除步骤"""
    data = request.json
    step_id = data.get('step_id', '')

    if not step_id:
        return jsonify({'error': '请提供步骤ID'}), 400

    # 删除步骤
    success = flowchart.remove_step(step_id)

    if not success:
        return jsonify({'error': '未找到指定步骤'}), 404

    # 获取所有步骤
    steps = flowchart.get_steps_for_sql()

    # 重新生成SQL
    sql = sql_generator.generate_sql_from_steps(steps)

    return jsonify({
        'sql': sql,
        'flowchart': flowchart.to_dict()
    })

if __name__ == '__main__':
    app.run(debug=True)
