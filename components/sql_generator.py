# SQL生成组件

import requests
import json
import re

class SQLGenerator:
    def __init__(self, api_key=None, model_url=None):
        """
        初始化SQL生成器
        :param api_key: Qwen API密钥
        :param model_url: Qwen模型API地址
        """
        self.api_key = api_key
        self.model_url = model_url or "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def generate_sql(self, natural_language, schema=None):
        """
        根据自然语言生成SQL语句
        :param natural_language: 自然语言描述
        :param schema: 数据库结构信息（可选）
        :return: 生成的SQL语句
        """
        prompt = self._build_prompt(natural_language, schema)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {"role": "system", "content": "你是一个专业的SQL生成助手，请根据用户的自然语言描述生成准确的SQL查询语句。"},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(self.model_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            sql = result["output"]["text"].strip()
            # 清理SQL，去除可能的markdown标记
            sql = re.sub(r'```sql\n?', '', sql)
            sql = re.sub(r'```', '', sql)

            return sql
        except Exception as e:
            print(f"生成SQL时出错: {e}")
            return "-- 生成SQL时出错，请检查API密钥和网络连接"

    def _build_prompt(self, natural_language, schema=None):
        """
        构建用于生成SQL的提示词
        :param natural_language: 自然语言描述
        :param schema: 数据库结构信息
        :return: 构建的提示词
        """
        prompt = f"请将以下自然语言描述转换为SQL查询语句:\n\n{natural_language}\n\n"

        if schema:
            prompt += f"\n数据库结构信息:\n{schema}\n\n"

        prompt += "请只返回SQL语句，不要包含任何解释。"

        return prompt

    def parse_sql_to_steps(self, sql):
        """
        将SQL语句解析为流程步骤
        :param sql: SQL语句
        :return: 流程步骤列表
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"请将以下SQL语句分解为执行步骤，每个步骤用JSON格式表示，包含step_id, step_type和description:\n\n{sql}\n\n返回JSON数组格式。"
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {"role": "system", "content": "你是一个SQL解析助手，能够将SQL语句分解为执行步骤。"},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(self.model_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()["output"]["text"].strip()
            # 尝试提取JSON部分
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                result = json_match.group()

            steps = json.loads(result)
            return steps
        except Exception as e:
            print(f"解析SQL为步骤时出错: {e}")
            # 返回一个默认的步骤结构
            return [
                {"step_id": 1, "step_type": "query", "description": "执行查询"},
                {"step_id": 2, "step_type": "result", "description": "获取结果"}
            ]

    def generate_sql_from_steps(self, steps):
        """
        根据流程步骤重新生成SQL语句
        :param steps: 流程步骤列表
        :return: 生成的SQL语句
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        steps_str = json.dumps(steps, indent=2)
        prompt = f"请根据以下步骤重新生成完整的SQL查询语句:\n\n{steps_str}\n\n返回SQL语句，不要包含任何解释。"
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {"role": "system", "content": "你是一个SQL生成助手，能够根据执行步骤重新构建SQL语句。"},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
        
        try:
            response = requests.post(self.model_url, headers=headers, json=data)
            response.raise_for_status()
            
            sql = response.json()["output"]["text"].strip()
            # 清理SQL，去除可能的markdown标记
            sql = re.sub(r'```sql\n?', '', sql)
            sql = re.sub(r'```', '', sql)

            return sql
        except Exception as e:
            print(f"从步骤生成SQL时出错: {e}")
            return "-- 从步骤生成SQL时出错"
