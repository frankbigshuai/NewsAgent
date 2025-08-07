# test_api.py - TechSum API完整测试脚本
import requests
import json
import time
from typing import Dict, Any

# API基础URL
BASE_URL = "http://localhost:8001"

class TechSumAPITester:
    """TechSum API测试器"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.test_user_id = f"test_user_{int(time.time())}"
        self.test_results = []
        
    def test_api_endpoint(self, method: str, endpoint: str, data: Dict[str, Any] = None, description: str = ""):
        """测试API端点"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"\n🧪 测试: {description}")
            print(f"   请求: {method} {endpoint}")
            
            if method.upper() == "GET":
                response = requests.get(url)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            else:
                print(f"   ❌ 不支持的HTTP方法: {method}")
                return False
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"   ✅ 测试通过")
                    print(f"   📊 响应摘要: {result.get('message', 'success')}")
                    
                    # 显示关键数据
                    if "data" in result:
                        data = result["data"]
                        if isinstance(data, dict):
                            key_info = []
                            for key in ["user_id", "total_recommendations", "confidence_score", "primary_interests"]:
                                if key in data:
                                    key_info.append(f"{key}: {data[key]}")
                            if key_info:
                                print(f"   📋 关键信息: {', '.join(key_info)}")
                    
                    self.test_results.append({"endpoint": endpoint, "status": "✅ 通过", "description": description})
                    return True
                else:
                    print(f"   ❌ API返回失败: {result}")
                    self.test_results.append({"endpoint": endpoint, "status": "❌ 失败", "description": description})
                    return False
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                print(f"   📄 响应: {response.text}")
                self.test_results.append({"endpoint": endpoint, "status": f"❌ HTTP {response.status_code}", "description": description})
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ 连接失败: 请确保API服务器正在运行 (python survey_api.py)")
            self.test_results.append({"endpoint": endpoint, "status": "❌ 连接失败", "description": description})
            return False
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            self.test_results.append({"endpoint": endpoint, "status": f"❌ 异常: {e}", "description": description})
            return False
    
    def run_complete_test_suite(self):
        """运行完整测试套件"""
        print("🚀 开始TechSum API完整测试")
        print(f"🎯 测试用户ID: {self.test_user_id}")
        print("="*60)
        
        # 测试1: 获取问卷结构
        self.test_api_endpoint(
            "GET", 
            "/api/v2/survey/questions",
            description="获取问卷结构"
        )
        
        # 测试2: 提交问卷答案
        survey_answers = {
            "user_id": self.test_user_id,
            "answers": {
                "技术兴趣": ["ai_ml", "programming", "startup_venture"],
                "专业背景": "engineer",
                "阅读习惯": "summary",
                "使用场景": ["morning", "evening"],
                "AI关注程度": 4
            }
        }
        
        self.test_api_endpoint(
            "POST",
            "/api/v2/survey/submit",
            data=survey_answers,
            description="提交问卷答案，创建用户画像"
        )
        
        # 测试3: 获取用户画像
        self.test_api_endpoint(
            "GET",
            f"/api/v2/profile/{self.test_user_id}",
            description="获取用户画像详情"
        )
        
        # 测试4: 追踪用户行为
        behavior_data = {
            "user_id": self.test_user_id,
            "action": "deep_read",
            "news_id": "test_news_001",
            "news_category": "ai_ml",
            "news_title": "OpenAI发布GPT-5模型技术详解",
            "reading_duration": 180,
            "scroll_percentage": 90.0
        }
        
        self.test_api_endpoint(
            "POST",
            "/api/v2/behavior/track",
            data=behavior_data,
            description="追踪用户行为，更新画像"
        )
        
        # 测试5: 获取个性化推荐
        personalized_request = {
            "user_id": self.test_user_id,
            "limit": 10
        }
        
        self.test_api_endpoint(
            "POST",
            "/api/v2/personalized-feed",
            data=personalized_request,
            description="获取个性化新闻推荐（你的喜好）"
        )
        
        # 测试6: 获取推荐解释
        self.test_api_endpoint(
            "GET",
            f"/api/v2/feed/explanation/{self.test_user_id}",
            description="获取推荐解释"
        )
        
        # 测试7: 系统统计
        self.test_api_endpoint(
            "GET",
            "/api/v2/system/stats",
            description="获取系统统计信息"
        )
        
        # 打印测试结果汇总
        self.print_test_summary()
    
    def test_user_journey(self):
        """测试完整用户旅程"""
        print("\n🎭 测试完整用户旅程...")
        print("="*60)
        
        journey_user = f"journey_user_{int(time.time())}"
        
        # 步骤1: 新用户填写问卷
        print("\n👤 步骤1: 新用户填写问卷")
        survey_data = {
            "user_id": journey_user,
            "answers": {
                "技术兴趣": ["ai_ml", "web3_crypto"],
                "专业背景": "investor",
                "阅读习惯": "deep",
                "使用场景": ["morning", "weekend"],
                "AI关注程度": 5
            }
        }
        self.test_api_endpoint("POST", "/api/v2/survey/submit", survey_data, "投资人用户填写问卷")
        
        # 步骤2: 查看个性化推荐
        print("\n📱 步骤2: 查看'你的喜好'页面")
        feed_request = {"user_id": journey_user, "limit": 8}
        self.test_api_endpoint("POST", "/api/v2/personalized-feed", feed_request, "查看个性化新闻流")
        
        # 步骤3: 阅读AI相关新闻
        print("\n📖 步骤3: 深度阅读AI新闻")
        behaviors = [
            {"action": "deep_read", "category": "ai_ml", "duration": 240, "scroll": 95.0},
            {"action": "share", "category": "ai_ml", "duration": 60, "scroll": 80.0},
            {"action": "bookmark", "category": "web3_crypto", "duration": 90, "scroll": 85.0}
        ]
        
        for i, behavior in enumerate(behaviors):
            behavior_data = {
                "user_id": journey_user,
                "action": behavior["action"],
                "news_id": f"news_{i+1}",
                "news_category": behavior["category"],
                "news_title": f"相关新闻标题 {i+1}",
                "reading_duration": behavior["duration"],
                "scroll_percentage": behavior["scroll"]
            }
            self.test_api_endpoint("POST", "/api/v2/behavior/track", behavior_data, f"行为{i+1}: {behavior['action']}")
        
        # 步骤4: 再次查看推荐，验证学习效果
        print("\n🎯 步骤4: 验证行为学习效果")
        self.test_api_endpoint("POST", "/api/v2/personalized-feed", feed_request, "查看学习后的推荐")
        self.test_api_endpoint("GET", f"/api/v2/profile/{journey_user}", description="查看更新后的用户画像")
    
    def print_test_summary(self):
        """打印测试结果汇总"""
        print("\n" + "="*60)
        print("📊 TechSum API测试结果汇总")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "✅" in r["status"]])
        failed_tests = total_tests - passed_tests
        
        print(f"📈 总测试数: {total_tests}")
        print(f"✅ 通过测试: {passed_tests}")
        print(f"❌ 失败测试: {failed_tests}")
        print(f"📊 成功率: {passed_tests/total_tests*100:.1f}%")
        
        print(f"\n📋 详细结果:")
        for result in self.test_results:
            print(f"   {result['status']} {result['endpoint']} - {result['description']}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 所有API测试通过！系统可以投入使用！")
            print(f"💡 下一步建议:")
            print(f"   1. 与Zane协调前端集成")
            print(f"   2. 部署到生产环境")
            print(f"   3. 添加数据持久化")
        else:
            print(f"\n⚠️  部分测试失败，需要修复后再进行前端集成")

def main():
    """主测试函数"""
    print("🔍 检查API服务器状态...")
    
    # 简单健康检查
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API服务器运行正常")
        else:
            print("⚠️  API服务器响应异常")
    except:
        print("❌ 无法连接到API服务器")
        print("💡 请先运行: python survey_api.py")
        return
    
    # 运行测试
    tester = TechSumAPITester()
    
    # 基础API测试
    tester.run_complete_test_suite()
    
    # 用户旅程测试
    tester.test_user_journey()

if __name__ == "__main__":
    main()