from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Customer, FollowUp, SalesUser, Base
from datetime import datetime, timedelta
import random

# 创建所有表
Base.metadata.create_all(bind=engine)

def init_data():
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(Customer).count() > 0:
            print("数据已存在，跳过初始化")
            return
        
        # 创建销售人员数据
        sales_users_data = [
            # 销售管理层
            {
                "name": "王小明",
                "email": "wangxiaoming@company.com",
                "phone": "+86-138-0001-0001",
                "department": "销售部",
                "position": "高级销售经理"
            },
            {
                "name": "李小红",
                "email": "lixiaohong@company.com",
                "phone": "+86-138-0002-0002",
                "department": "销售部",
                "position": "销售经理"
            },
            {
                "name": "刘大伟",
                "email": "liudawei@company.com",
                "phone": "+86-138-0003-0003",
                "department": "销售部",
                "position": "区域销售总监"
            },
            
            # 资深销售
            {
                "name": "张小华",
                "email": "zhangxiaohua@company.com",
                "phone": "+86-138-0004-0004",
                "department": "销售部",
                "position": "资深销售专员"
            },
            {
                "name": "陈小强",
                "email": "chenxiaoqiang@company.com",
                "phone": "+86-138-0005-0005",
                "department": "销售部",
                "position": "资深销售专员"
            },
            {
                "name": "赵美丽",
                "email": "zhaomeili@company.com",
                "phone": "+86-138-0006-0006",
                "department": "销售部",
                "position": "资深销售专员"
            },
            
            # 销售专员
            {
                "name": "孙志强",
                "email": "sunzhiqiang@company.com",
                "phone": "+86-138-0007-0007",
                "department": "销售部",
                "position": "销售专员"
            },
            {
                "name": "周雨婷",
                "email": "zhouyuting@company.com",
                "phone": "+86-138-0008-0008",
                "department": "销售部",
                "position": "销售专员"
            },
            {
                "name": "吴建国",
                "email": "wujianguo@company.com",
                "phone": "+86-138-0009-0009",
                "department": "销售部",
                "position": "销售专员"
            },
            
            # 国际销售
            {
                "name": "Alice Johnson",
                "email": "alice.johnson@company.com",
                "phone": "+1-555-0101",
                "department": "国际销售部",
                "position": "International Sales Manager"
            },
            {
                "name": "David Chen",
                "email": "david.chen@company.com",
                "phone": "+1-555-0102",
                "department": "国际销售部",
                "position": "Senior International Sales"
            },
            
            # 客户成功
            {
                "name": "林晓敏",
                "email": "linxiaomin@company.com",
                "phone": "+86-138-0010-0010",
                "department": "客户成功部",
                "position": "客户成功经理"
            },
            {
                "name": "黄志明",
                "email": "huangzhiming@company.com",
                "phone": "+86-138-0011-0011",
                "department": "客户成功部",
                "position": "客户成功专员"
            }
        ]
        
        sales_users = []
        for user_data in sales_users_data:
            sales_user = SalesUser(**user_data)
            db.add(sales_user)
            sales_users.append(sales_user)
        
        db.commit()
        print(f"创建了 {len(sales_users)} 个销售人员")
        
        # 创建客户数据 - 保留10个代表性客户
        customers_data = [
            # 中国客户 (6个)
            {
                "name": "阿里巴巴集团",
                "contact": "张总",
                "phone": "+86-138-0013-8888",
                "company": "阿里巴巴集团控股有限公司",
                "country": "中国"
            },
            {
                "name": "腾讯科技",
                "contact": "李经理",
                "phone": "+86-138-0013-8889",
                "company": "腾讯科技（深圳）有限公司",
                "country": "中国"
            },
            {
                "name": "京东集团",
                "contact": "王总",
                "phone": "+86-138-0013-8890",
                "company": "京东集团股份有限公司",
                "country": "中国"
            },
            {
                "name": "字节跳动",
                "contact": "陈经理",
                "phone": "+86-138-0013-8891",
                "company": "字节跳动科技有限公司",
                "country": "中国"
            },
            {
                "name": "华为技术",
                "contact": "刘总监",
                "phone": "+86-138-0013-8892",
                "company": "华为技术有限公司",
                "country": "中国"
            },
            {
                "name": "小米科技",
                "contact": "雷总",
                "phone": "+86-138-0013-8893",
                "company": "小米科技有限责任公司",
                "country": "中国"
            },
            
            # 美国客户 (2个)
            {
                "name": "Amazon",
                "contact": "John Smith",
                "phone": "+1-555-0123",
                "company": "Amazon.com Inc.",
                "country": "美国"
            },
            {
                "name": "Apple",
                "contact": "David Brown",
                "phone": "+1-408-555-0127",
                "company": "Apple Inc.",
                "country": "美国"
            },
            
            # 加拿大客户 (1个)
            {
                "name": "Shopify",
                "contact": "Sarah Johnson",
                "phone": "+1-416-555-0124",
                "company": "Shopify Inc.",
                "country": "加拿大"
            },
            
            # 日本客户 (1个)
            {
                "name": "楽天市場",
                "contact": "田中先生",
                "phone": "+81-3-5555-0129",
                "company": "楽天株式会社",
                "country": "日本"
            }
        ]
        
        customers = []
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        
        # 为每个客户创建跟进记录
        followup_types = ["电话沟通", "线上会议", "上门拜访", "邮件联系"]
        followup_results = ["成功", "待跟进", "失败"]
        
        # 定义更丰富的跟进内容模板
        followup_contents = {
            "电话沟通": [
                "与{customer_contact}进行了电话沟通，详细介绍了我们的跨境物流服务优势。客户对我们的时效性和价格体系很感兴趣，希望了解更多细节。",
                "电话回访{customer_contact}，了解客户对上次提供的物流方案的反馈。客户表示需要内部讨论，预计下周给出回复。",
                "与{customer_contact}电话沟通了最新的物流政策变化，客户对我们的专业服务表示认可，有意向进行深度合作。",
                "电话联系{customer_contact}跟进合同签署事宜，客户对条款基本满意，正在走内部审批流程。",
                "电话沟通了紧急物流需求，客户对我们的快速响应能力表示赞赏，已安排技术团队对接。"
            ],
            "线上会议": [
                "与{customer_contact}进行线上产品演示会议，展示了我们的智能物流管理系统。客户对系统的实时追踪功能很感兴趣。",
                "线上会议讨论合作框架，客户对我们的服务范围和价格策略表示认可，希望进一步细化合作条款。",
                "与客户团队进行线上技术对接会议，详细介绍了API集成方案和数据安全措施。",
                "线上会议回顾了合作进展，客户对我们的服务质量和响应速度给予高度评价。",
                "与{customer_contact}进行线上培训会议，介绍了新功能的操作方法，客户反馈积极。"
            ],
            "上门拜访": [
                "前往{customer_company}进行上门拜访，实地了解了客户的物流需求和仓库情况，为定制化方案提供了重要参考。",
                "上门拜访{customer_contact}，详细介绍了我们的仓储配送网络，客户对覆盖范围表示满意。",
                "实地考察了客户的物流流程，与操作团队进行了深入交流，提出了优化建议。",
                "上门拜访讨论了长期合作协议，客户对我们的专业能力和服务态度表示认可。",
                "实地拜访了客户新设立的海外仓，就合作模式进行了深入探讨。"
            ],
            "邮件联系": [
                "发送了详细的物流服务报价单给{customer_contact}，包含不同方案的价格对比和服务说明。",
                "邮件发送了最新的物流政策更新和行业动态，客户回复表示感谢并希望保持沟通。",
                "通过邮件发送了合作合同草稿，等待客户法务部门审核。",
                "邮件跟进上次会议讨论的效果，客户回复表示正在内部评估。",
                "发送了客户关心的技术文档和操作手册，客户反馈文档很详细实用。"
            ]
        }
        
        # 定义下一步行动模板
        next_actions = [
            "准备详细的技术方案和报价单",
            "安排技术团队进行系统对接",
            "等待客户内部决策结果",
            "跟进合同签署进度",
            "安排产品演示会议",
            "准备合作框架协议",
            "跟进客户反馈意见",
            "安排实地考察访问",
            "提供定制化解决方案",
            "跟进付款和结算事宜"
        ]
        
        for customer in customers:
            # 为每个客户创建5-12条跟进记录
            num_followups = random.randint(5, 12)
            
            # 按时间顺序创建跟进记录
            for i in range(num_followups):
                # 创建过去90天内的随机日期，让时间分布更自然
                days_ago = random.randint(1, 90)
                followup_date = datetime.utcnow() - timedelta(days=days_ago)
                followup_type = random.choice(followup_types)
                sales_user = random.choice(sales_users)
                
                # 根据跟进类型选择合适的跟进内容
                content_template = random.choice(followup_contents[followup_type])
                content = content_template.format(
                    customer_contact=customer.contact,
                    customer_company=customer.company
                )
                
                # 根据跟进类型调整时长范围
                duration_ranges = {
                    "电话沟通": (10, 45),
                    "线上会议": (30, 90),
                    "上门拜访": (60, 180),
                    "邮件联系": (5, 20)
                }
                duration = random.randint(*duration_ranges[followup_type])
                
                # 根据跟进次数调整结果概率
                if i < 2:  # 前两次跟进，成功的概率较低
                    result_weights = [0.3, 0.5, 0.2]  # 成功, 待跟进, 失败
                elif i < num_followups - 2:  # 中间跟进，待跟进较多
                    result_weights = [0.4, 0.5, 0.1]
                else:  # 最后几次跟进，成功概率较高
                    result_weights = [0.6, 0.3, 0.1]
                
                result = random.choices(followup_results, weights=result_weights)[0]
                
                # 生成跟进记录标题
                title = f"{followup_type} - {customer.name}"
                
                followup = FollowUp(
                    customer_id=customer.id,
                    sales_user_id=sales_user.id,
                    title=title,
                    type=followup_type,
                    content=content,
                    date=followup_date,
                    duration=duration,
                    result=result,
                    next_action=random.choice(next_actions)
                )
                db.add(followup)
        
        db.commit()
        print("初始化数据创建成功！")
        
    except Exception as e:
        print(f"初始化数据失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_data()

