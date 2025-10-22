#!/bin/bash

# CRM系统Docker停止脚本
echo "🛑 停止CRM系统Docker服务..."

# 停止并删除容器
docker-compose down

# 询问是否删除数据卷
read -p "是否删除数据卷？这将删除所有数据！(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ 删除数据卷..."
    docker-compose down -v
fi

# 询问是否删除镜像
read -p "是否删除Docker镜像？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 删除Docker镜像..."
    docker-compose down --rmi all
fi

echo "✅ CRM系统Docker服务已停止"
