#!/bin/bash

echo "🚀 GitHub上传脚本"
echo "================================"
echo ""

# 检查GitHub仓库URL是否已设置
if [ -z "$1" ]; then
    echo "❌ 请提供GitHub仓库URL"
    echo ""
    echo "使用方法:"
    echo "  ./upload-to-github.sh https://github.com/yourusername/crm-followup-demo.git"
    echo ""
    echo "或者:"
    echo "  ./upload-to-github.sh git@github.com:yourusername/crm-followup-demo.git"
    echo ""
    exit 1
fi

GITHUB_URL=$1

echo "📋 准备上传到GitHub..."
echo "仓库URL: $GITHUB_URL"
echo ""

# 检查Git状态
echo "🔍 检查Git状态..."
if [ ! -d ".git" ]; then
    echo "❌ 项目不是Git仓库，请先运行 git init"
    exit 1
fi

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  检测到未提交的更改，正在提交..."
    git add .
    git commit -m "Update: 更新项目文件"
    echo "✅ 更改已提交"
fi

# 添加远程仓库
echo ""
echo "🔗 添加远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin $GITHUB_URL

# 设置主分支
echo "🌿 设置主分支..."
git branch -M main

# 推送到GitHub
echo ""
echo "📤 推送到GitHub..."
echo "这可能需要几分钟时间，请耐心等待..."

if git push -u origin main; then
    echo ""
    echo "🎉 上传成功！"
    echo "================================"
    echo "📱 您的项目已成功上传到GitHub"
    echo "🔗 访问地址: $(echo $GITHUB_URL | sed 's/\.git$//')"
    echo ""
    echo "📋 项目特性:"
    echo "  ✅ 完整的CRM客户跟进系统"
    echo "  ✅ Docker一键部署"
    echo "  ✅ 详细的README文档"
    echo "  ✅ 功能演示GIF"
    echo "  ✅ 完整的项目结构"
    echo ""
    echo "🎯 下一步建议:"
    echo "  1. 在GitHub上设置仓库描述和标签"
    echo "  2. 启用GitHub Pages（如果需要）"
    echo "  3. 设置Issues和Projects"
    echo "  4. 邀请协作者（如果需要）"
else
    echo ""
    echo "❌ 上传失败"
    echo "================================"
    echo "可能的原因:"
    echo "  1. 网络连接问题"
    echo "  2. GitHub认证失败"
    echo "  3. 仓库URL错误"
    echo "  4. 权限不足"
    echo ""
    echo "🔧 解决方案:"
    echo "  1. 检查网络连接"
    echo "  2. 确认GitHub用户名和密码/Token"
    echo "  3. 验证仓库URL是否正确"
    echo "  4. 确认有仓库的写入权限"
    echo ""
    echo "💡 提示: 如果使用HTTPS，建议使用Personal Access Token"
    echo "   生成地址: https://github.com/settings/tokens"
fi
