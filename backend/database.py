from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite数据库文件路径
SQLALCHEMY_DATABASE_URL = "sqlite:///./crm_followup.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},  # SQLite特有配置
    pool_pre_ping=True,  # 验证连接
    pool_recycle=3600  # 每小时回收连接
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base = declarative_base()

