# 故障排除指南

## 常见问题及解决方案

### 1. 502 Bad Gateway 错误

#### 问题描述
```
GET http://localhost/api/customers?_t=xxx 502 (Bad Gateway)
Error fetching customers: AxiosError
```

#### 解决方案

##### 方案1: 重新启动服务
```bash
# 停止服务
docker-compose down

# 重新启动
docker-compose up -d

# 等待服务启动
sleep 30
```

##### 方案2: 检查服务状态
```bash
# 检查容器状态
docker-compose ps

# 检查服务日志
docker-compose logs backend
docker-compose logs frontend
```

##### 方案3: 清理并重新构建
```bash
# 停止并清理
docker-compose down -v

# 清理数据目录
rm -rf backend/data
mkdir -p backend/data

# 重新构建并启动
docker-compose up --build -d
```

### 2. 数据库初始化问题

#### 问题描述
- 后端服务不断重启
- 数据库文件无法打开
- 没有客户数据

#### 解决方案
```bash
# 确保数据目录存在
mkdir -p backend/data

# 重新启动服务（会自动初始化数据库）
docker-compose up --build -d
```

### 3. 端口占用问题

#### 问题描述
- 端口80或8001被占用
- 服务启动失败

#### 解决方案
```bash
# 检查端口占用
lsof -i :80
lsof -i :8001

# 停止占用端口的进程
sudo kill -9 <PID>

# 或修改docker-compose.yml中的端口映射
```

### 4. 网络连接问题

#### 问题描述
- 前端无法连接后端
- 容器间通信失败

#### 解决方案
```bash
# 检查Docker网络
docker network ls

# 重新创建网络
docker-compose down
docker-compose up -d
```

### 5. 浏览器缓存问题

#### 问题描述
- 页面显示旧内容
- API请求失败

#### 解决方案
1. 清除浏览器缓存
2. 硬刷新页面 (Ctrl+F5 或 Cmd+Shift+R)
3. 使用无痕模式访问

## 诊断命令

### 检查服务状态
```bash
# 查看所有容器状态
docker-compose ps

# 查看服务日志
docker-compose logs backend --tail=20
docker-compose logs frontend --tail=20
docker-compose logs db_init --tail=20
```

### 测试API连接
```bash
# 测试后端健康检查
curl http://localhost:8001/health

# 测试客户API
curl http://localhost:8001/customers

# 测试前端代理
curl http://localhost/api/customers
```

### 检查数据库
```bash
# 检查数据目录
ls -la backend/data/

# 检查数据库文件
file backend/data/crm_followup.db
```

## 完整重置流程

如果以上方案都无法解决问题，可以尝试完整重置：

```bash
# 1. 停止所有服务
docker-compose down -v

# 2. 清理Docker资源
docker system prune -f

# 3. 清理数据目录
rm -rf backend/data
mkdir -p backend/data

# 4. 重新构建并启动
docker-compose up --build -d

# 5. 等待服务启动
sleep 30

# 6. 测试服务
curl http://localhost:8001/health
curl http://localhost/api/customers
```

## 联系支持

如果问题仍然存在，请提供以下信息：

1. 操作系统版本
2. Docker版本
3. 错误日志
4. 服务状态输出

```bash
# 收集诊断信息
echo "=== 系统信息 ==="
uname -a
docker --version
docker-compose --version

echo "=== 服务状态 ==="
docker-compose ps

echo "=== 服务日志 ==="
docker-compose logs backend --tail=50
docker-compose logs frontend --tail=50
```
