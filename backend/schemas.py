from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Customer相关Schema
class CustomerBase(BaseModel):
    name: str
    contact: str
    phone: str
    company: str
    country: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# SalesUser相关Schema
class SalesUserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None


class SalesUserResponse(SalesUserBase):
    id: int
    hire_date: datetime
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True

# FollowUp相关Schema
class FollowUpBase(BaseModel):
    title: str
    type: str
    content: str
    date: datetime
    sales_user_id: int
    duration: Optional[int] = None
    result: Optional[str] = None
    next_action: Optional[str] = None

class FollowUpCreate(FollowUpBase):
    pass

class FollowUpResponse(FollowUpBase):
    id: int
    customer_id: int
    created_at: datetime
    sales_user_name: Optional[str] = None

    class Config:
        from_attributes = True


# 包含跟进记录的客户详情
class CustomerWithFollowups(CustomerResponse):
    followups: List[FollowUpResponse] = []

