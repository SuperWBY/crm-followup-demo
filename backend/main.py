from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import SessionLocal, engine, Base
from models import Customer, FollowUp, SalesUser
from schemas import (
    CustomerCreate, CustomerResponse, CustomerWithFollowups,
    FollowUpCreate, FollowUpResponse,
    SalesUserResponse
)

# 创建数据库表
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CRM FollowUp API",
    description="CRM客户事件跟进模块API",
    version="1.0.0"
)

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "message": "CRM API is running"}

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue开发服务器端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"app": "CRM FollowUp", "version": "1.0.0", "status": "running"}

# 客户相关接口
@app.get("/customers", response_model=List[CustomerResponse])
async def get_customers(db: Session = Depends(get_db)):
    """获取客户列表"""
    customers = db.query(Customer).all()
    return customers

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """获取客户详情"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# 跟进记录相关接口
@app.get("/customers/{customer_id}/followups", response_model=List[FollowUpResponse])
async def get_followups(customer_id: int, db: Session = Depends(get_db)):
    """获取客户跟进记录"""
    followups = db.query(FollowUp).filter(
        FollowUp.customer_id == customer_id
    ).order_by(FollowUp.date.desc()).all()
    
    # 为每个跟进记录添加销售人员姓名
    result = []
    for followup in followups:
        sales_user = db.query(SalesUser).filter(SalesUser.id == followup.sales_user_id).first()
        # 创建FollowUpResponse对象
        followup_response = FollowUpResponse(
            id=followup.id,
            customer_id=followup.customer_id,
            sales_user_id=followup.sales_user_id,
            title=followup.title,
            type=followup.type,
            content=followup.content,
            date=followup.date,
            duration=followup.duration,
            result=followup.result,
            next_action=followup.next_action,
            created_at=followup.created_at,
            sales_user_name=sales_user.name if sales_user else "未知"
        )
        result.append(followup_response)
    
    return result

@app.post("/customers/{customer_id}/followups", response_model=FollowUpResponse)
async def create_followup(customer_id: int, followup: FollowUpCreate, db: Session = Depends(get_db)):
    """新增跟进记录"""
    try:
        # 检查客户是否存在
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # 创建跟进记录
        db_followup = FollowUp(
            customer_id=customer_id,
            title=followup.title,
            type=followup.type,
            content=followup.content,
            date=followup.date,
            sales_user_id=followup.sales_user_id,
            duration=followup.duration,
            result=followup.result,
            next_action=followup.next_action
        )
        db.add(db_followup)
        db.commit()
        db.refresh(db_followup)
        
        # 获取销售人员姓名
        sales_user = db.query(SalesUser).filter(SalesUser.id == db_followup.sales_user_id).first()
        result = FollowUpResponse(
            id=db_followup.id,
            customer_id=db_followup.customer_id,
            sales_user_id=db_followup.sales_user_id,
            title=db_followup.title,
            type=db_followup.type,
            content=db_followup.content,
            date=db_followup.date,
            duration=db_followup.duration,
            result=db_followup.result,
            next_action=db_followup.next_action,
            created_at=db_followup.created_at,
            sales_user_name=sales_user.name if sales_user else "未知"
        )
        return result
    except Exception as e:
        print(f"Error creating followup: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/followups/{followup_id}", response_model=FollowUpResponse)
async def update_followup(followup_id: int, followup: FollowUpCreate, db: Session = Depends(get_db)):
    """修改跟进记录"""
    db_followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not db_followup:
        raise HTTPException(status_code=404, detail="FollowUp not found")
    
    db_followup.title = followup.title
    db_followup.type = followup.type
    db_followup.content = followup.content
    db_followup.date = followup.date
    db_followup.sales_user_id = followup.sales_user_id
    db_followup.duration = followup.duration
    db_followup.result = followup.result
    db_followup.next_action = followup.next_action
    
    db.commit()
    db.refresh(db_followup)
    
    # 获取销售人员姓名
    sales_user = db.query(SalesUser).filter(SalesUser.id == db_followup.sales_user_id).first()
    result = FollowUpResponse(
        id=db_followup.id,
        customer_id=db_followup.customer_id,
        sales_user_id=db_followup.sales_user_id,
        title=db_followup.title,
        type=db_followup.type,
        content=db_followup.content,
        date=db_followup.date,
        duration=db_followup.duration,
        result=db_followup.result,
        next_action=db_followup.next_action,
        created_at=db_followup.created_at,
        sales_user_name=sales_user.name if sales_user else "未知"
    )
    return result

@app.delete("/followups/{followup_id}")
async def delete_followup(followup_id: int, db: Session = Depends(get_db)):
    """删除跟进记录"""
    db_followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not db_followup:
        raise HTTPException(status_code=404, detail="FollowUp not found")
    
    db.delete(db_followup)
    db.commit()
    return {"message": "FollowUp deleted successfully"}

# 销售人员相关接口
@app.get("/sales-users", response_model=List[SalesUserResponse])
async def get_sales_users(db: Session = Depends(get_db)):
    """获取销售人员列表"""
    sales_users = db.query(SalesUser).filter(SalesUser.is_active == 1).all()
    return sales_users




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
