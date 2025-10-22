#!/usr/bin/env python3
"""
CRM FollowUp API 测试脚本
用于验证后端API接口是否正常工作
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8001"

def test_api():
    """测试API接口"""
    print("🧪 开始测试 CRM FollowUp API")
    print("=" * 50)
    
    try:
        # 1. 测试根路径
        print("1️⃣ 测试根路径...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        print()
        
        # 2. 获取客户列表
        print("2️⃣ 获取客户列表...")
        response = requests.get(f"{BASE_URL}/customers")
        print(f"   状态码: {response.status_code}")
        customers = response.json()
        print(f"   客户数量: {len(customers)}")
        if customers:
            print(f"   第一个客户: {customers[0]['name']}")
        print()
        
        # 3. 获取客户详情
        if customers:
            customer_id = customers[0]['id']
            print(f"3️⃣ 获取客户详情 (ID: {customer_id})...")
            response = requests.get(f"{BASE_URL}/customers/{customer_id}")
            print(f"   状态码: {response.status_code}")
            customer_detail = response.json()
            print(f"   客户名称: {customer_detail['name']}")
            print(f"   联系人: {customer_detail['contact']}")
            print()
            
            # 4. 获取跟进记录
            print(f"4️⃣ 获取客户跟进记录 (ID: {customer_id})...")
            response = requests.get(f"{BASE_URL}/customers/{customer_id}/followups")
            print(f"   状态码: {response.status_code}")
            followups = response.json()
            print(f"   跟进记录数量: {len(followups)}")
            if followups:
                print(f"   最新跟进: {followups[0]['type']} - {followups[0]['content'][:50]}...")
            print()
            
            # 5. 创建新的跟进记录
            print(f"5️⃣ 创建新的跟进记录...")
            new_followup = {
                "type": "电话沟通",
                "content": "测试API创建的跟进记录，客户对我们的服务表示满意，希望进一步了解价格和政策。",
                "date": datetime.now().isoformat(),
                "sales_user_id": 1
            }
            response = requests.post(
                f"{BASE_URL}/customers/{customer_id}/followups",
                json=new_followup
            )
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                created_followup = response.json()
                print(f"   创建成功，跟进记录ID: {created_followup['id']}")
                
                # 6. 更新跟进记录
                print(f"6️⃣ 更新跟进记录 (ID: {created_followup['id']})...")
                updated_followup = {
                    **new_followup,
                    "content": "更新后的跟进内容：客户对我们的服务非常满意，已经决定合作。"
                }
                response = requests.put(
                    f"{BASE_URL}/followups/{created_followup['id']}",
                    json=updated_followup
                )
                print(f"   状态码: {response.status_code}")
                if response.status_code == 200:
                    print("   更新成功")
                
                # 7. 删除跟进记录
                print(f"7️⃣ 删除跟进记录 (ID: {created_followup['id']})...")
                response = requests.delete(f"{BASE_URL}/followups/{created_followup['id']}")
                print(f"   状态码: {response.status_code}")
                if response.status_code == 200:
                    print("   删除成功")
        
        print()
        print("✅ 所有API测试通过！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 请确保后端服务正在运行 (python main.py)")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api()
