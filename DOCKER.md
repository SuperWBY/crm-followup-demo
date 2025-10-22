# CRM系统Docker部署指南

## 📋 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少2GB可用内存
- 至少1GB可用磁盘空间

## 🚀 快速部署

### 1. 生产环境部署

```bash
# 启动服务
./docker-start.sh

# 或者手动启动
docker-compose up --build -d
```

### 2. 开发环境部署

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up --build -d
```

## 📊 服务访问

- **前端应用**: http://localhost
- **后端API**: http://localhost:8001
- **API文档**: http://localhost:8001/docs

## 🛠️ 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 数据管理

```bash
# 备份数据
docker cp crm-backend:/app/crm_followup.db ./backup/

# 恢复数据
docker cp ./backup/crm_followup.db crm-backend:/app/

# 进入容器
docker exec -it crm-backend bash
docker exec -it crm-frontend sh
```

### 镜像管理

```bash
# 重新构建镜像
docker-compose build

# 清理未使用的镜像
docker image prune

# 清理所有未使用的资源
docker system prune -a
```

## 🔧 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| PYTHONPATH | /app | Python路径 |
| PYTHONUNBUFFERED | 1 | Python输出缓冲 |

### 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 80 | Web界面 |
| 后端 | 8001 | API服务 |

### 数据持久化

- 数据库文件: `./backend/crm_followup.db`
- 数据目录: `./backend/data/`

## 🏥 健康检查

系统包含健康检查机制：

```bash
# 检查后端健康状态
curl http://localhost:8001/health

# 检查前端健康状态
curl http://localhost/health
```

## 🐛 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :80
   netstat -tulpn | grep :8001
   ```

2. **容器启动失败**
   ```bash
   # 查看详细日志
   docker-compose logs backend
   docker-compose logs frontend
   ```

3. **数据库连接问题**
   ```bash
   # 检查数据库文件权限
   ls -la backend/crm_followup.db
   ```

### 重置系统

```bash
# 完全重置
./docker-stop.sh
# 选择删除数据卷和镜像
./docker-start.sh
```

## 📈 性能优化

### 资源限制

在 `docker-compose.yml` 中添加资源限制：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### 缓存优化

- 前端静态资源已配置长期缓存
- 后端使用Python缓存机制
- 数据库查询优化

## 🔒 安全建议

1. **生产环境部署**
   - 修改默认端口
   - 配置防火墙规则
   - 使用HTTPS
   - 定期更新镜像

2. **数据安全**
   - 定期备份数据库
   - 使用数据卷加密
   - 限制容器权限

## 📞 支持

如遇到问题，请检查：
1. Docker和Docker Compose版本
2. 系统资源使用情况
3. 网络连接状态
4. 日志文件内容
