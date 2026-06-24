@echo off
chcp 65001 >nul
echo 🚀 启动财务健康看板...

:: 检查虚拟环境是否存在
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

:: 安装依赖
echo 📥 安装依赖...
pip install -r requirements.txt

:: 启动应用
echo 🌐 启动 Streamlit 应用...
streamlit run project2.py

pause