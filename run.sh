#!/bin/bash
# 财务健康看板 - Linux/Mac 一键启动脚本

echo "🚀 启动财务健康看板..."

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 启动应用
echo "🌐 启动 Streamlit 应用..."
streamlit run project2.py