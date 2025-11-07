# 文字转SQL与纵向流程框图系统

本项目是一个基于Qwen大模型的文字转SQL与纵向流程框图系统，能够根据输入的自然语言生成SQL语言和与之对应的纵向流程框图，并支持双向联动编辑。

## 功能特点

- 根据自然语言生成SQL语句
- 生成对应的纵向流程框图，支持不同节点类型的可视化（开始、结束、决策、处理、数据）
- 支持流程框图编辑，并实时更新SQL语句
- 基于Flask和Qwen API构建
- 美观的Web界面，支持响应式设计
- 支持SQL语句复制功能

## 技术栈

- **后端**：Python, Flask
- **前端**：HTML5, CSS3, JavaScript, Bootstrap
- **大模型**：Qwen（通义千问）
- **API**：阿里云DashScope API

## 安装与运行

### 环境要求

- Python 3.7+
- 阿里云DashScope API密钥

### 安装步骤

1. 克隆项目：
```bash
git clone [项目仓库地址]
cd flowchat
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入您的Qwen API密钥
QWEN_API_KEY=your_qwen_api_key_here
QWEN_MODEL_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

4. 运行应用：
```bash
python app.py
```

5. 访问应用：
打开浏览器访问 `http://127.0.0.1:5000`

## 项目结构

```
flowchat/
├── app.py                 # 主应用入口
├── requirements.txt       # 项目依赖
├── .env.example          # 环境变量示例
├── components/            # 组件目录
│   ├── __init__.py
│   ├── sql_generator.py   # SQL生成组件
│   └── flowchart.py       # 流程图组件
└── templates/             # HTML模板
    └── index.html         # 主页面
```

## 使用说明

1. 在"输入区域"输入自然语言描述，例如："查询所有年龄大于30岁的用户信息，包括姓名、年龄和邮箱，并按年龄降序排列"
2. 可选：提供数据库结构信息，以便更准确地生成SQL
3. 点击"生成SQL与流程图"按钮
4. 查看生成的SQL语句和对应的纵向流程框图
5. 可以编辑流程框图中的步骤，SQL语句会随之更新
6. 点击"复制"按钮可以复制SQL语句

## 流程框图节点类型

- **开始**：绿色圆角矩形，表示流程开始
- **结束**：红色圆角矩形，表示流程结束
- **处理**：白色矩形，表示常规处理步骤
- **决策**：黄色菱形，表示判断或分支点
- **数据**：蓝色倾斜矩形，表示数据操作

## 注意事项

- 需要有效的阿里云DashScope API密钥才能使用本系统
- 生成的SQL语句可能需要根据实际数据库结构进行调整
- 流程框图是SQL执行过程的可视化表示，仅供参考

## 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

## 许可证

本项目采用MIT许可证。
