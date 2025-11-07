# 流程图组件

import json
from typing import List, Dict, Any

class FlowChart:
    def __init__(self):
        """
        初始化流程图组件
        """
        self.steps = []
        self.connections = []

    def from_sql_steps(self, steps: List[Dict[str, Any]]):
        """
        从SQL步骤初始化流程图
        :param steps: SQL步骤列表
        """
        self.steps = []
        self.connections = []
        
        # 确保第一个步骤是"开始"，最后一个是"结束"
        if steps and steps[0].get('step_type') != 'start':
            steps.insert(0, {"step_id": 0, "step_type": "start", "description": "开始"})
        if steps and steps[-1].get('step_type') != 'end':
            steps.append({"step_id": len(steps) + 1, "step_type": "end", "description": "结束"})

        for i, step in enumerate(steps):
            # 创建节点
            node_id = f"node_{step.get('step_id', i+1)}"
            node_type = step.get('step_type', 'process')
            node_text = step.get('description', f"步骤 {i+1}")

            self.steps.append({
                "id": node_id,
                "type": node_type,
                "text": node_text,
                "position": {
                    "x": 100,
                    "y": 100 + i * 100
                }
            })

            # 创建连接（除了最后一个节点）
            if i < len(steps) - 1:
                next_node_id = f"node_{steps[i+1].get('step_id', i+2)}"
                self.connections.append({
                    "source": node_id,
                    "target": next_node_id,
                    "type": "arrow"
                })

    def to_dict(self):
        """
        将流程图转换为字典格式，便于序列化
        :return: 流程图字典
        """
        return {
            "nodes": self.steps,
            "connections": self.connections
        }

    def to_json(self):
        """
        将流程图转换为JSON字符串
        :return: 流程图JSON字符串
        """
        return json.dumps(self.to_dict(), indent=2)

    def update_step(self, step_id: str, new_text: str, new_type: str = None):
        """
        更新流程图中的步骤
        :param step_id: 步骤ID
        :param new_text: 新的步骤文本
        :param new_type: 新的步骤类型（可选）
        """
        for step in self.steps:
            if step["id"] == step_id:
                step["text"] = new_text
                if new_type:
                    step["type"] = new_type
                return True
        return False

    def add_step(self, step_type: str, description: str, after_id: str = None):
        """
        添加新步骤
        :param step_type: 步骤类型
        :param description: 步骤描述
        :param after_id: 在哪个步骤后添加（可选）
        :return: 新创建的步骤ID
        """
        # 生成新的ID
        max_id = 0
        for step in self.steps:
            try:
                step_num = int(step["id"].replace("node_", ""))
                if step_num > max_id:
                    max_id = step_num
            except:
                pass

        new_id = f"node_{max_id + 1}"

        # 确定新步骤的位置
        new_y = 100
        if after_id:
            for step in self.steps:
                if step["id"] == after_id:
                    new_y = step["position"]["y"] + 100
                    break

        # 创建新步骤
        new_step = {
            "id": new_id,
            "type": step_type,
            "text": description,
            "position": {
                "x": 100,
                "y": new_y
            }
        }

        self.steps.append(new_step)

        # 如果指定了after_id，添加连接
        if after_id:
            self.connections.append({
                "source": after_id,
                "target": new_id,
                "type": "arrow"
            })

        return new_id

    def remove_step(self, step_id: str):
        """
        删除步骤
        :param step_id: 要删除的步骤ID
        :return: 是否成功删除
        """
        # 删除步骤
        for i, step in enumerate(self.steps):
            if step["id"] == step_id:
                self.steps.pop(i)
                break
        else:
            return False

        # 删除相关连接
        self.connections = [
            conn for conn in self.connections 
            if conn["source"] != step_id and conn["target"] != step_id
        ]

        return True

    def get_steps_for_sql(self):
        """
        获取用于生成SQL的步骤列表
        :return: 步骤列表
        """
        steps = []
        for step in self.steps:
            # 从ID中提取步骤编号
            try:
                step_id = int(step["id"].replace("node_", ""))
            except:
                step_id = len(steps) + 1

            steps.append({
                "step_id": step_id,
                "step_type": step["type"],
                "description": step["text"]
            })

        # 按步骤ID排序
        steps.sort(key=lambda x: x["step_id"])
        return steps
