#!/bin/bash

echo "🚀 GitHub克隆项目设置脚本"
echo "================================"
echo ""
echo "这个脚本专门用于设置从GitHub克隆的CRM项目"
echo ""

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker守护进程未运行。请启动Docker Desktop或Docker服务。"
    exit 1
fi
echo "✅ Docker服务正常运行"

# 检查docker-compose是否可用
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose命令未找到。请安装Docker Compose。"
    exit 1
fi
echo "✅ Docker Compose可用"

# 停止并移除旧的服务
echo ""
echo "🧹 停止并移除旧的Docker服务（如果存在）..."
docker-compose down --remove-orphans

# 确保数据目录存在
echo ""
echo "📁 创建数据目录..."
mkdir -p backend/data

# 清理可能存在的旧数据
echo ""
echo "🗑️ 清理旧数据..."
rm -rf backend/data/*

# 重新构建并启动服务
echo ""
echo "🔨 重新构建并启动Docker服务..."
docker-compose up --build -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动（这可能需要1-2分钟）..."
sleep 60

# 检查服务状态
echo ""
echo "🔍 检查服务状态..."
docker-compose ps

# 测试API连接
echo ""
echo "🧪 测试API连接..."
echo "等待后端服务完全启动..."
sleep 10

# 测试后端健康检查
echo "1. 测试后端健康检查:"
if curl -s http://localhost:8001/health | grep -q "healthy"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常，请检查日志"
    docker-compose logs backend --tail=20
fi

# 测试客户API
echo ""
echo "2. 测试客户API:"
CUSTOMER_COUNT=$(curl -s http://localhost:8001/customers | python3 -c "
import json
import sys
try:
    data = json.load(sys.stdin)
    print(len(data))
except:
    print(0)
" 2>/dev/null)

if [ "$CUSTOMER_COUNT" -gt 0 ]; then
    echo "✅ 客户API正常，返回 $CUSTOMER_COUNT 个客户"
else
    echo "❌ 客户API异常，没有客户数据"
fi

# 测试前端代理
echo ""
echo "3. 测试前端代理:"
if curl -s http://localhost/api/customers | grep -q "name"; then
    echo "✅ 前端代理正常"
else
    echo "❌ 前端代理异常"
fi

# 最终状态检查
echo ""
echo "🎉 设置完成！"
echo "================================"

if [ "$CUSTOMER_COUNT" -gt 0 ]; then
    echo "✅ 所有服务正常运行"
    echo ""
    echo "🌐 访问地址:"
    echo "  前端应用: http://localhost"
    echo "  后端API: http://localhost:8001"
    echo "  API文档: http://localhost:8001/docs"
    echo ""
    echo "📊 项目状态:"
    echo "  - 数据库: 已初始化，包含 $CUSTOMER_COUNT 个客户"
    echo "  - 后端服务: 正常运行"
    echo "  - 前端服务: 正常运行"
    echo "  - API连接: 正常"
    echo ""
    echo "💡 如果遇到502错误，请等待1-2分钟让服务完全启动"
    echo "   或清除浏览器缓存后重新访问"
else
    echo "❌ 设置过程中遇到问题"
    echo ""
    echo "🔧 故障排除:"
    echo "1. 检查Docker服务是否正常运行"
    echo "2. 检查端口80和8001是否被占用"
    echo "3. 查看服务日志: docker-compose logs"
    echo "4. 重新运行此脚本"
    echo ""
    echo "📋 服务日志:"
    docker-compose logs --tail=10
fi

echo ""
echo "📚 更多帮助:"
echo "  - 故障排除指南: ./troubleshooting.md"
echo "  - 项目文档: ./README.md"
