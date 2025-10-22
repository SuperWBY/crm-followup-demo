# CRM FollowUp Backend

## 项目介绍
CRM客户事件跟进模块后端API，使用FastAPI + SQLAlchemy + SQLite构建。

## 功能特性
- 客户管理（增删查改）
- 跟进记录管理（增删查改）
- RESTful API设计
- 自动生成API文档（Swagger UI）

## 快速开始

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据
```bash
python init_data.py
```

### 3. 启动服务
```bash
python main.py
```

服务将在 http://localhost:8000 启动

### 4. 查看API文档
访问 http://localhost:8000/docs 查看Swagger UI文档

## API接口

### 客户相关
- `GET /customers` - 获取客户列表
- `GET /customers/{id}` - 获取客户详情

### 跟进记录相关
- `GET /customers/{id}/followups` - 获取客户跟进记录
- `POST /customers/{id}/followups` - 新增跟进记录
- `PUT /followups/{id}` - 修改跟进记录
- `DELETE /followups/{id}` - 删除跟进记录

## 数据库设计

### Customer（客户表）
- id: 主键
- name: 客户名称
- contact: 联系人
- phone: 联系电话
- company: 所属公司
- country: 国家
- created_at: 创建时间

### FollowUp（跟进记录表）
- id: 主键
- customer_id: 客户ID（外键）
- type: 跟进类型
- content: 跟进内容
- date: 跟进时间
- sales_user: 录入人
- created_at: 创建时间

