# CRM 客户事件跟进模块 Demo

## 项目背景

WallTech 是一家专注于跨境物流的 SaaS 平台服务商，为全球电商企业提供一站式物流解决方案。随着业务规模的扩大和客户数量的增长，传统的客户关系管理方式已无法满足精细化运营的需求。

### 业务痛点
- **跟进记录分散**：销售人员的客户沟通记录缺乏统一管理
- **数据孤岛**：客户信息、跟进历史、销售数据无法有效整合
- **效率低下**：缺乏系统化的跟进流程和数据分析工具
- **决策困难**：管理层无法及时了解销售进展和客户状态

### 解决方案
本项目为 WallTech CRM 系统新增 **客户事件跟进功能模块**，旨在：
- 建立标准化的客户跟进流程
- 实现跟进数据的集中管理和分析
- 提供直观的数据可视化界面
- 支持销售团队的协作和效率提升

## 功能演示

### 🎬 Demo 展示

<div align="center">
  <img src="demo.gif" alt="CRM Demo" width="800" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
</div>

> **💡 提示**: 如果GIF显示较小，请点击图片查看完整尺寸

> **演示内容**：
> - 客户列表浏览和搜索
> - 客户详情页面的跟进记录管理
> - 新增/编辑跟进记录流程
> - 数据统计和可视化展示
> - 响应式设计适配

#### 📹 视频演示（高清版）

如果您觉得GIF显示不够清晰，我们还提供了高清视频演示：

<div align="center">
  <a href="demo.mp4">
    <img src="https://img.shields.io/badge/📹-观看高清视频演示-blue?style=for-the-badge&logo=video" alt="观看视频演示">
  </a>
</div>

> **视频特点**：
> - 🎥 高清画质，细节清晰可见
> - 🔊 包含操作说明和功能介绍
> - 📱 展示完整的用户交互流程
> - ⏱️ 时长约2-3分钟，内容精炼

### 核心功能

销售人员可以在客户详情页中：
- 📝 **录入跟进记录**（电话沟通 / 线上会议 / 上门拜访等）
- 📊 **查看历史跟进记录**（时间线展示，支持分页和搜索）
- 📈 **数据统计分析**（KPI指标、销售漏斗、跟进统计）
- 🔍 **快速索引导航**（基于标题的快速跳转）
- 👥 **多销售人员协作**（支持13个销售人员的权限管理）

## 技术栈

### 后端
- **FastAPI** - 现代、快速的Web框架
- **SQLAlchemy** - Python SQL工具包和对象关系映射
- **SQLite** - 轻量级数据库
- **Pydantic** - 数据验证和序列化

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Element Plus** - Vue 3组件库
- **Pinia** - Vue状态管理
- **Vue Router** - Vue官方路由管理器
- **Axios** - HTTP客户端

## 项目结构

```
crm-followup-demo/
├── backend/                 # 后端项目
│   ├── main.py             # FastAPI应用入口
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── schemas.py          # Pydantic模式
│   ├── init_data.py        # 初始化数据脚本
│   ├── requirements.txt    # Python依赖
│   ├── Dockerfile          # 后端Docker镜像
│   ├── .dockerignore       # Docker忽略文件
│   └── README.md          # 后端说明文档
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── stores/        # Pinia状态管理
│   │   ├── router/        # 路由配置
│   │   └── api/           # API接口
│   ├── package.json       # Node.js依赖
│   ├── vite.config.js     # Vite配置
│   ├── Dockerfile          # 前端生产环境Docker镜像
│   ├── Dockerfile.dev      # 前端开发环境Docker镜像
│   ├── nginx.conf          # Nginx配置文件
│   └── .dockerignore       # Docker忽略文件
├── docker-compose.yml      # Docker Compose生产环境配置
├── docker-compose.dev.yml  # Docker Compose开发环境配置
├── docker-start.sh         # Docker启动脚本
├── docker-stop.sh          # Docker停止脚本
├── start-local.sh          # 本地启动脚本
├── stop-local.sh           # 本地停止脚本
├── DOCKER.md               # Docker部署文档
├── demo.gif                # 功能演示动图
└── README.md               # 项目说明文档
```

## 快速开始

### 🚀 Docker 部署（推荐）

**最简单的方式，一键启动所有服务！**

#### 环境要求
- **Docker** 20.10+
- **Docker Compose** 2.0+

#### 一键启动
```bash
# 克隆项目
git clone <repository-url>
cd crm-followup-demo

# 使用Docker启动脚本（推荐）
chmod +x docker-start.sh
./docker-start.sh

# 或直接使用docker-compose
docker-compose up --build -d
```

#### 访问地址
- **前端应用**: http://localhost
- **后端API**: http://localhost:8001
- **API文档**: http://localhost:8001/docs

#### 停止服务
```bash
# 使用停止脚本
chmod +x docker-stop.sh
./docker-stop.sh

# 或直接使用docker-compose
docker-compose down
```

#### Docker 开发模式
```bash
# 启动开发环境（支持热重载）
docker-compose -f docker-compose.dev.yml up --build -d

# 访问地址
# 前端: http://localhost:5173
# 后端: http://localhost:8001
```

### 💻 本地开发部署

#### 环境要求
- **Python 3.8+**
- **Node.js 16+**
- **npm** 或 **yarn**

#### 一键启动（推荐）
```bash
# 克隆项目
git clone <repository-url>
cd crm-followup-demo

# 一键启动所有服务
chmod +x start-local.sh
./start-local.sh
```

#### 手动启动

##### 1. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
python main.py
```

##### 2. 启动前端服务
```bash
cd frontend
npm install
npm run dev
```

#### 访问地址
- **前端页面**: http://localhost:5173
- **后端API**: http://localhost:8001
- **API文档**: http://localhost:8001/docs

#### 停止服务
```bash
# 使用停止脚本
chmod +x stop-local.sh
./stop-local.sh

# 或手动停止
# 按 Ctrl+C 停止运行的服务
```

### 🎯 快速开始总结

| 部署方式 | 命令 | 访问地址 | 适用场景 |
|---------|------|----------|----------|
| **Docker（推荐）** | `./docker-start.sh` | http://localhost | 生产环境、快速体验 |
| **Docker开发** | `docker-compose -f docker-compose.dev.yml up -d` | http://localhost:5173 | 开发调试 |
| **本地开发** | `./start-local.sh` | http://localhost:5173 | 本地开发 |

> **💡 提示**：首次使用建议选择 Docker 部署，一键启动，无需配置环境！

## 开发特性

### 前端热重载
- 修改代码后自动刷新浏览器
- 支持Vue组件的热更新
- 实时查看样式和功能更改

### 后端自动重启
- 修改Python代码后自动重启服务
- 支持API接口的实时调试

## 功能特性

### 客户管理
- 客户列表展示（网格视图/列表视图）
- 客户信息查看
- 客户搜索功能

### 跟进记录
- 新增跟进记录
- 跟进记录编辑
- 跟进记录删除
- 跟进记录时间线展示

### 跟进类型
- 电话沟通
- 线上会议
- 上门拜访
- 邮件联系

## API 接口

### 客户接口
- `GET /customers` - 获取客户列表
- `GET /customers/{id}` - 获取客户详情

### 跟进记录接口
- `GET /customers/{customer_id}/followups` - 获取客户跟进记录
- `POST /customers/{customer_id}/followups` - 创建跟进记录
- `PUT /followups/{id}` - 更新跟进记录
- `DELETE /followups/{id}` - 删除跟进记录

### 销售人员接口
- `GET /sales-users` - 获取销售人员列表

## 开发说明

### 数据库
项目使用SQLite数据库，数据库文件位于 `backend/crm_followup.db`。

### 数据初始化
项目启动时会自动初始化示例数据，包括：
- 5个示例客户
- 每个客户的跟进记录

### 样式定制
项目使用极简设计风格，配色方案：
- 主色调: #3B82F6 (蓝色)
- 辅助色: #F5F5F5 (灰色)
- 成功色: #10B981 (绿色)
- 警告色: #F59E0B (橙色)
- 错误色: #EF4444 (红色)

## 部署说明

### 🐳 Docker 部署优势

- **环境一致性**：开发、测试、生产环境完全一致
- **快速部署**：一键启动，无需配置复杂环境
- **资源隔离**：容器化部署，避免环境冲突
- **易于扩展**：支持水平扩展和负载均衡
- **版本管理**：支持镜像版本管理和回滚

### 📋 部署检查清单

#### Docker 部署前检查
- [ ] Docker 服务正常运行
- [ ] Docker Compose 已安装
- [ ] 端口 80 和 8001 未被占用
- [ ] 磁盘空间充足（至少 2GB）

#### 本地部署前检查
- [ ] Python 3.8+ 已安装
- [ ] Node.js 16+ 已安装
- [ ] 端口 5173 和 8001 未被占用
- [ ] 网络连接正常

## 故障排除

### Docker 部署问题

1. **Docker 服务未启动**
   ```bash
   # macOS/Windows
   # 启动 Docker Desktop
   
   # Linux
   sudo systemctl start docker
   ```

2. **端口被占用**
   ```bash
   # 检查端口占用
   lsof -i :80
   lsof -i :8001
   
   # 停止占用端口的进程
   sudo kill -9 <PID>
   ```

3. **容器启动失败**
   ```bash
   # 查看容器日志
   docker-compose logs backend
   docker-compose logs frontend
   
   # 重新构建镜像
   docker-compose build --no-cache
   ```

4. **数据库初始化失败**
   ```bash
   # 清理数据卷重新初始化
   docker-compose down -v
   docker-compose up --build -d
   ```

### 本地部署问题

1. **端口被占用**
   - 后端默认端口: 8001
   - 前端默认端口: 5173
   - 如有冲突，请修改相应配置文件

2. **依赖安装失败**
   - 确保Python和Node.js版本符合要求
   - 尝试使用虚拟环境
   - 清除缓存重新安装：`npm cache clean --force`

3. **服务启动失败**
   - 检查端口是否被占用
   - 查看错误日志信息
   - 确保数据库文件权限正确

### 常见错误解决

#### 1. "录入人没有数据" 问题
**原因**：API URL配置错误
**解决**：确保使用相对路径 `/api/sales-users`

#### 2. 前端页面空白
**原因**：API连接失败
**解决**：检查后端服务是否正常运行

#### 3. 数据库连接失败
**原因**：数据库文件权限或路径问题
**解决**：检查 `backend/data/` 目录权限

### 性能优化建议

1. **生产环境优化**
   - 使用 Nginx 反向代理
   - 启用 Gzip 压缩
   - 配置静态资源缓存

2. **数据库优化**
   - 定期备份数据库
   - 监控数据库性能
   - 考虑升级到 PostgreSQL

3. **监控和日志**
   - 配置应用监控
   - 设置日志轮转
   - 监控系统资源使用

## 许可证

MIT License