#!/bin/bash

# CRM系统Docker部署脚本
echo "🚀 启动CRM系统Docker部署..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 清理旧镜像（可选）
read -p "是否清理旧镜像？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 清理旧镜像..."
    docker-compose down --rmi all
fi

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 检查健康状态
echo "🏥 检查服务健康状态..."
echo "后端健康检查:"
curl -f http://localhost:8001/health && echo "✅ 后端服务正常" || echo "❌ 后端服务异常"

echo "前端健康检查:"
curl -f http://localhost/health && echo "✅ 前端服务正常" || echo "❌ 前端服务异常"

echo ""
echo "🎉 CRM系统部署完成！"
echo "📱 前端访问地址: http://localhost"
echo "🔧 后端API地址: http://localhost:8001"
echo "📊 查看日志: docker-compose logs -f"
echo "🛑 停止服务: docker-compose down"
