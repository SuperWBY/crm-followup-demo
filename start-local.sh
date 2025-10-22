#!/bin/bash

# CRM FollowUp Demo - 本地启动脚本
echo "🚀 启动 CRM 客户跟进系统..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查Node.js版本
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js 16+"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"
echo "✅ Node.js 版本: $(node --version)"

# 启动后端
echo "📡 启动后端服务..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 未找到 requirements.txt"
    exit 1
fi

# 安装后端依赖
echo "📦 安装后端依赖..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1

# 启动后端服务器
echo "🔄 启动 FastAPI 后端服务器..."
python3 main.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if curl -s http://localhost:8001/ > /dev/null; then
    echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"
else
    echo "❌ 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 回到项目根目录
cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
if [ ! -f "package.json" ]; then
    echo "❌ 错误: 未找到 package.json"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 安装前端依赖
echo "📦 安装前端依赖..."
npm install > /dev/null 2>&1

# 启动前端开发服务器
echo "🔄 启动 Vite 前端开发服务器..."
npm run dev &
FRONTEND_PID=$!

# 等待前端启动
sleep 5

# 检查前端是否启动成功
if curl -s http://localhost:5173/ > /dev/null; then
    echo "✅ 前端服务启动成功 (PID: $FRONTEND_PID)"
else
    echo "❌ 前端服务启动失败"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

# 回到项目根目录
cd ..

echo ""
echo "🎉 所有服务启动成功！"
echo ""
echo "📱 前端地址: http://localhost:5173"
echo "🔧 后端API: http://localhost:8001"
echo "📚 API文档: http://localhost:8001/docs"
echo ""
echo "💡 提示:"
echo "   - 前端支持热重载，修改代码后会自动刷新"
echo "   - 按 Ctrl+C 可以停止所有服务"
echo ""

# 保存进程ID到文件
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 等待用户中断
trap 'echo ""; echo "🛑 正在停止服务..."; kill $(cat .backend.pid 2>/dev/null) $(cat .frontend.pid 2>/dev/null) 2>/dev/null; rm -f .backend.pid .frontend.pid; echo "✅ 所有服务已停止"; exit 0' INT

echo "⏳ 服务运行中... (按 Ctrl+C 停止)"
wait
