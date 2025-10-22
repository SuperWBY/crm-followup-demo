from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class SalesUser(Base):
    __tablename__ = "sales_users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    department = Column(String(100))
    position = Column(String(100))
    hire_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1: 在职, 0: 离职
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联跟进记录
    followups = relationship("FollowUp", back_populates="sales_user")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    company = Column(String(200), nullable=False)
    country = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联跟进记录
    followups = relationship("FollowUp", back_populates="customer", cascade="all, delete-orphan")

class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    sales_user_id = Column(Integer, ForeignKey("sales_users.id"), nullable=False)
    title = Column(String(200), nullable=False)  # 跟进记录标题
    type = Column(String(50), nullable=False)  # 跟进类型：电话/会议/拜访
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer)  # 跟进时长（分钟）
    result = Column(String(50))  # 跟进结果：成功/待跟进/失败
    next_action = Column(Text)  # 下一步行动计划
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联客户和销售员
    customer = relationship("Customer", back_populates="followups")
    sales_user = relationship("SalesUser", back_populates="followups")


