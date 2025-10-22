#!/bin/bash

# CRM FollowUp Demo - 停止本地服务脚本
echo "🛑 停止 CRM 客户跟进系统..."

# 停止后端服务
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill $BACKEND_PID 2>/dev/null; then
        echo "✅ 后端服务已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️  后端服务进程不存在或已停止"
    fi
    rm -f .backend.pid
else
    echo "⚠️  未找到后端进程ID文件"
fi

# 停止前端服务
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill $FRONTEND_PID 2>/dev/null; then
        echo "✅ 前端服务已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️  前端服务进程不存在或已停止"
    fi
    rm -f .frontend.pid
else
    echo "⚠️  未找到前端进程ID文件"
fi

# 清理可能残留的进程
echo "🧹 清理残留进程..."
pkill -f "python3.*main.py" 2>/dev/null && echo "✅ 清理后端进程"
pkill -f "npm.*dev" 2>/dev/null && echo "✅ 清理前端进程"
pkill -f "vite" 2>/dev/null && echo "✅ 清理Vite进程"

echo "🎉 所有服务已停止！"
