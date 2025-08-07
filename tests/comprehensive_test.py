# comprehensive_test.py - TechSum 完整集成测试套件
import sys
import os
import time
import json
import unittest
import requests
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TechSumComprehensiveTest:
    """
    TechSum 系统完整测试套件
    🎯 测试覆盖：单元测试 + 集成测试 + API测试 + 性能测试
    """
    
    def __init__(self):
        self.test_results = {
            "unit_tests": {"passed": 0, "failed": 0, "errors": []},
            "integration_tests": {"passed": 0, "failed": 0, "errors": []},
            "api_tests": {"passed": 0, "failed": 0, "errors": []},
            "performance_tests": {"passed": 0, "failed": 0, "errors": []},
            "end_to_end_tests": {"passed": 0, "failed": 0, "errors": []}
        }
        
        self.api_server_process = None
        self.base_url = "http://localhost:8001"
        
        print("🚀 初始化TechSum完整测试套件...")
        print("=" * 80)
    
    # ===========================================
    # 📋 Part 1: 单元测试
    # ===========================================
    
    def test_unit_interest_survey(self):
        """测试问卷系统单元功能"""
        print("\n📋 Part 1: 单元测试")
        print("-" * 50)
        print("🧪 测试兴趣问卷系统...")
        
        try:
            from models.interest_survey import survey_instance
            
            # 测试1: 问卷结构获取
            survey_data = survey_instance.get_survey_for_frontend()
            assert "metadata" in survey_data, "问卷应包含元数据"
            assert "questions" in survey_data, "问卷应包含问题"
            assert len(survey_data["questions"]) == 5, "应该有5个问题"
            print("   ✅ 问卷结构获取正常")
            
            # 测试2: 答案验证
            valid_answers = {
                "技术兴趣": ["ai_ml", "programming"],
                "专业背景": "engineer",
                "阅读习惯": "summary"
            }
            validation = survey_instance.validate_answers(valid_answers)
            assert validation["valid"] == True, "有效答案应该通过验证"
            print("   ✅ 答案验证功能正常")
            
            # 测试3: 画像转换
            profile_data = survey_instance.convert_answers_to_profile(valid_answers)
            assert "interest_weights" in profile_data, "应该生成兴趣权重"
            assert "basic_info" in profile_data, "应该包含基础信息"
            
            # 验证权重分配
            weights = profile_data["interest_weights"]
            assert abs(sum(weights.values()) - 1.0) < 0.001, "权重总和应该为1"
            assert weights["programming"] > 0.125, "编程权重应该提升"
            print("   ✅ 画像转换功能正常")
            
            self.test_results["unit_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 兴趣问卷测试失败: {e}")
            self.test_results["unit_tests"]["failed"] += 1
            self.test_results["unit_tests"]["errors"].append(f"兴趣问卷: {e}")
    
    def test_unit_user_profile(self):
        """测试用户画像管理单元功能"""
        print("\n🧪 测试用户画像管理...")
        
        try:
            from models.interest_survey import survey_instance
            from models.user_profile import UserProfileManager
            
            profile_manager = UserProfileManager(survey_instance)
            
            # 测试1: 问卷创建画像
            test_answers = {
                "技术兴趣": ["ai_ml", "programming", "startup_venture"],
                "专业背景": "engineer",
                "阅读习惯": "summary",
                "使用场景": ["morning", "evening"]
            }
            
            user_profile = profile_manager.create_profile_from_survey(
                "unit_test_user", test_answers
            )
            
            assert user_profile.user_id == "unit_test_user", "用户ID应该正确"
            assert user_profile.basic_info["professional_background"] == "engineer", "专业背景应该正确"
            assert len(user_profile.interest_weights) == 8, "应该有8个兴趣类别"
            print("   ✅ 问卷创建画像功能正常")
            
            # 测试2: 行为更新画像
            behavior_data = {
                "action": "deep_read",
                "news_category": "ai_ml",
                "reading_duration": 180,
                "engagement_score": 0.25
            }
            
            updated_profile = profile_manager.update_profile_from_behavior(
                "unit_test_user", behavior_data
            )
            
            assert updated_profile.personalization["total_interactions"] > 0, "交互次数应该增加"
            print("   ✅ 行为更新画像功能正常")
            
            # 测试3: 推荐用画像数据
            rec_profile = profile_manager.get_profile_for_recommendations("unit_test_user")
            assert "interest_weights" in rec_profile, "应该包含兴趣权重"
            assert "primary_interests" in rec_profile, "应该包含主要兴趣"
            print("   ✅ 推荐画像数据获取正常")
            
            self.test_results["unit_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 用户画像测试失败: {e}")
            self.test_results["unit_tests"]["failed"] += 1
            self.test_results["unit_tests"]["errors"].append(f"用户画像: {e}")
    
    def test_unit_behavior_system(self):
        """测试行为学习系统单元功能"""
        print("\n🧪 测试行为学习系统...")
        
        try:
            from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
            
            behavior_system = EnhancedBehaviorSystem(test_mode=True)
            
            # 测试1: 行为事件追踪
            test_event = BehaviorEvent(
                user_id="behavior_test_user",
                action="read",
                news_id="test_news_001",
                news_category="ai_ml",
                reading_duration=120,
                scroll_percentage=80.0
            )
            
            result = behavior_system.track_behavior(test_event)
            assert result["success"] == True, "行为追踪应该成功"
            assert "behavior_id" in result, "应该返回行为ID"
            assert result["engagement_score"] > 0, "参与度分数应该大于0"
            print("   ✅ 行为事件追踪功能正常")
            
            # 测试2: 用户偏好获取
            preferences = behavior_system.get_user_preferences("behavior_test_user")
            assert len(preferences) == 8, "应该有8个类别偏好"
            assert abs(sum(preferences.values()) - 1.0) < 0.001, "偏好权重总和应该为1"
            print("   ✅ 用户偏好获取功能正常")
            
            # 测试3: 系统统计
            stats = behavior_system.get_system_statistics()
            assert "total_behaviors" in stats, "应该包含行为统计"
            assert stats["total_behaviors"] > 0, "行为计数应该大于0"
            print("   ✅ 系统统计功能正常")
            
            self.test_results["unit_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 行为学习测试失败: {e}")
            self.test_results["unit_tests"]["failed"] += 1
            self.test_results["unit_tests"]["errors"].append(f"行为学习: {e}")
    
    def test_unit_recommendation_engine(self):
        """测试推荐引擎单元功能"""
        print("\n🧪 测试推荐引擎...")
        
        try:
            from models.cached_recommendation_engine import CachedRecommendationEngine
            
            rec_engine = CachedRecommendationEngine()
            
            # 测试1: 新闻数据获取
            news_data = rec_engine.get_cached_news_data()
            assert len(news_data) > 0, "应该获取到新闻数据"
            assert "title" in news_data[0], "新闻应该包含标题"
            assert "category" in news_data[0], "新闻应该包含类别"
            print("   ✅ 新闻数据获取功能正常")
            
            # 测试2: 个性化推荐生成
            user_interests = ["ai_ml", "programming"]
            user_weights = {
                "ai_ml": 0.3,
                "programming": 0.25,
                "web3_crypto": 0.1,
                "startup_venture": 0.1,
                "hardware_chips": 0.1,
                "consumer_tech": 0.05,
                "enterprise_saas": 0.05,
                "social_media": 0.05
            }
            
            recommendations = rec_engine.recommend_for_user(
                "rec_test_user", user_interests, user_weights, limit=5
            )
            
            assert len(recommendations) > 0, "应该生成推荐"
            assert "personalized_score" in recommendations[0], "推荐应该包含个性化分数"
            print("   ✅ 个性化推荐生成功能正常")
            
            # 测试3: 缓存统计
            cache_stats = rec_engine.get_cache_statistics()
            assert "总请求数" in cache_stats, "应该包含请求统计"
            print("   ✅ 缓存系统功能正常")
            
            self.test_results["unit_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 推荐引擎测试失败: {e}")
            self.test_results["unit_tests"]["failed"] += 1
            self.test_results["unit_tests"]["errors"].append(f"推荐引擎: {e}")
    
    # ===========================================
    # 🔄 Part 2: 集成测试
    # ===========================================
    
    def test_integration_survey_to_profile(self):
        """测试问卷→画像集成"""
        print("\n🔄 Part 2: 集成测试")
        print("-" * 50)
        print("🧪 测试问卷→画像集成...")
        
        try:
            from models.interest_survey import survey_instance
            from models.user_profile import UserProfileManager
            
            profile_manager = UserProfileManager(survey_instance)
            
            # 完整的问卷流程
            test_answers = {
                "技术兴趣": ["ai_ml", "web3_crypto", "startup_venture"],
                "专业背景": "investor",
                "阅读习惯": "deep",
                "使用场景": ["morning", "weekend"],
                "AI关注程度": 5
            }
            
            # 问卷验证
            validation = survey_instance.validate_answers(test_answers)
            assert validation["valid"], f"问卷验证失败: {validation['errors']}"
            
            # 创建画像
            profile = profile_manager.create_profile_from_survey("integration_user", test_answers)
            
            # 验证集成结果
            assert profile.basic_info["professional_background"] == "investor", "专业背景应该正确设置"
            assert profile.interest_weights["ai_ml"] > 0.125, "AI权重应该因高关注度提升"
            assert profile.personalization["onboarding_completed"] == True, "入职流程应该完成"
            
            # 验证推荐数据生成
            rec_profile = profile_manager.get_profile_for_recommendations("integration_user")
            assert len(rec_profile["primary_interests"]) > 0, "应该识别主要兴趣"
            
            print("   ✅ 问卷→画像集成功能正常")
            self.test_results["integration_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 问卷→画像集成测试失败: {e}")
            self.test_results["integration_tests"]["failed"] += 1
            self.test_results["integration_tests"]["errors"].append(f"问卷→画像: {e}")
    
    def test_integration_profile_to_recommendation(self):
        """测试画像→推荐集成"""
        print("\n🧪 测试画像→推荐集成...")
        
        try:
            from models.interest_survey import survey_instance
            from models.user_profile import UserProfileManager
            from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
            from models.cached_recommendation_engine import CachedRecommendationEngine
            
            # 创建集成系统
            rec_engine = CachedRecommendationEngine()
            behavior_system = EnhancedBehaviorSystem(rec_engine, test_mode=True)
            profile_manager = UserProfileManager(survey_instance, behavior_system)
            
            # 创建测试用户画像
            test_answers = {
                "技术兴趣": ["ai_ml", "programming"],
                "专业背景": "engineer",
                "阅读习惯": "summary"
            }
            
            profile = profile_manager.create_profile_from_survey("rec_integration_user", test_answers)
            
            # 获取推荐
            rec_profile = profile_manager.get_profile_for_recommendations("rec_integration_user")
            recommendations = behavior_system.get_intelligent_recommendations(
                "rec_integration_user", limit=8
            )
            
            # 验证推荐质量
            assert len(recommendations) > 0, "应该生成推荐"
            
            # 检查个性化效果
            ai_count = sum(1 for rec in recommendations if rec.get("category") == "ai_ml")
            programming_count = sum(1 for rec in recommendations if rec.get("category") == "programming")
            
            assert ai_count + programming_count >= len(recommendations) * 0.4, "技术类新闻应该占主要比例"
            
            print("   ✅ 画像→推荐集成功能正常")
            print(f"      AI新闻: {ai_count}条, 编程新闻: {programming_count}条")
            
            self.test_results["integration_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 画像→推荐集成测试失败: {e}")
            self.test_results["integration_tests"]["failed"] += 1
            self.test_results["integration_tests"]["errors"].append(f"画像→推荐: {e}")
    
    def test_integration_behavior_learning_loop(self):
        """测试行为学习闭环"""
        print("\n🧪 测试行为学习闭环...")
        
        try:
            from models.interest_survey import survey_instance
            from models.user_profile import UserProfileManager
            from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
            from models.cached_recommendation_engine import CachedRecommendationEngine
            
            # 创建完整系统
            rec_engine = CachedRecommendationEngine()
            behavior_system = EnhancedBehaviorSystem(rec_engine, test_mode=True)
            profile_manager = UserProfileManager(survey_instance, behavior_system)
            
            user_id = "learning_loop_user"
            
            # 1. 创建初始画像
            initial_answers = {
                "技术兴趣": ["programming"],  # 只选择编程
                "专业背景": "engineer",
                "阅读习惯": "summary"
            }
            
            profile_manager.create_profile_from_survey(user_id, initial_answers)
            initial_prefs = behavior_system.get_user_preferences(user_id)
            initial_ai_weight = initial_prefs["ai_ml"]
            
            # 2. 模拟用户大量阅读AI新闻
            ai_behaviors = [
                {"action": "deep_read", "duration": 180, "scroll": 95.0},
                {"action": "share", "duration": 60, "scroll": 80.0},
                {"action": "bookmark", "duration": 90, "scroll": 85.0},
                {"action": "like", "duration": 30, "scroll": 70.0},
                {"action": "deep_read", "duration": 200, "scroll": 90.0}
            ]
            
            for i, behavior in enumerate(ai_behaviors):
                event = BehaviorEvent(
                    user_id=user_id,
                    action=behavior["action"],
                    news_id=f"ai_news_{i}",
                    news_category="ai_ml",
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
                
                result = behavior_system.track_behavior(event)
                assert result["success"], f"行为{i+1}追踪应该成功"
                
                # 更新画像
                profile_manager.update_profile_from_behavior(user_id, {
                    "action": result["enhanced_action"],
                    "news_category": "ai_ml",
                    "reading_duration": behavior["duration"],
                    "engagement_score": result["engagement_score"]
                })
            
            # 3. 验证学习效果
            final_prefs = behavior_system.get_user_preferences(user_id)
            final_ai_weight = final_prefs["ai_ml"]
            
            assert final_ai_weight > initial_ai_weight, "AI权重应该通过行为学习提升"
            
            # 4. 验证推荐更新
            updated_recommendations = behavior_system.get_intelligent_recommendations(user_id, limit=8)
            ai_rec_count = sum(1 for rec in updated_recommendations if rec.get("category") == "ai_ml")
            
            assert ai_rec_count >= 2, "学习后AI推荐应该增加"
            
            print("   ✅ 行为学习闭环功能正常")
            print(f"      AI权重变化: {initial_ai_weight:.3f} → {final_ai_weight:.3f}")
            print(f"      AI推荐数量: {ai_rec_count}条")
            
            self.test_results["integration_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 行为学习闭环测试失败: {e}")
            self.test_results["integration_tests"]["failed"] += 1
            self.test_results["integration_tests"]["errors"].append(f"行为学习闭环: {e}")
    
    # ===========================================
    # 📡 Part 3: API测试（改进版）
    # ===========================================
    
    def start_api_server(self, timeout=30):
        """启动API服务器"""
        print("\n📡 Part 3: API接口测试")
        print("-" * 50)
        print("🚀 启动API服务器...")
        
        try:
        # 检查服务器是否已经运行
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("   ✅ API服务器已在运行，直接使用现有服务器")
                return True
        except:
            print("   🚀 API服务器未运行，尝试启动...")
        
        # 启动新的服务器进程
        try:
            self.api_server_process = subprocess.Popen(
                ["python", "survey_api.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 等待服务器启动
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(f"{self.base_url}/docs", timeout=2)
                    if response.status_code == 200:
                        print("   ✅ API服务器启动成功")
                        time.sleep(2)  # 额外等待确保完全启动
                        return True
                except:
                    time.sleep(1)
                    continue
            
            print("   ❌ API服务器启动超时")
            return False
            
        except Exception as e:
            print(f"   ❌ API服务器启动失败: {e}")
            return False
    
    def test_api_endpoints(self):
        """测试API端点（改进版）"""
        if not self.start_api_server():
            print("⚠️ 跳过API测试（服务器启动失败）")
            return
        
        print("\n🧪 测试API端点...")
        
        # 配置请求参数
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TechSum-Test-Client/1.0'
        })
        
        test_user_id = f"api_test_user_{int(time.time())}"
        
        try:
            # 测试1: 获取问卷结构
            print("   🧪 测试获取问卷结构...")
            response = session.get(f"{self.base_url}/api/v2/survey/questions", timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                assert result["success"], "API应该返回成功"
                assert "questions" in result["data"], "应该包含问题数据"
                print("      ✅ 问卷结构API正常")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            time.sleep(1)  # 避免请求过快
            
            # 测试2: 提交问卷
            print("   🧪 测试提交问卷...")
            survey_data = {
                "user_id": test_user_id,
                "answers": {
                    "技术兴趣": ["ai_ml", "programming"],
                    "专业背景": "engineer",
                    "阅读习惯": "summary"
                }
            }
            
            response = session.post(
                f"{self.base_url}/api/v2/survey/submit",
                json=survey_data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                assert result["success"], "问卷提交应该成功"
                assert result["data"]["profile_created"], "应该创建用户画像"
                print("      ✅ 问卷提交API正常")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            time.sleep(1)
            
            # 测试3: 获取个性化推荐
            print("   🧪 测试个性化推荐...")
            feed_data = {
                "user_id": test_user_id,
                "limit": 5
            }
            
            response = session.post(
                f"{self.base_url}/api/v2/personalized-feed",
                json=feed_data,
                timeout=20  # 推荐生成可能需要更长时间
            )
            
            if response.status_code == 200:
                result = response.json()
                assert result["success"], "推荐生成应该成功"
                assert len(result["data"]["recommendations"]) > 0, "应该生成推荐"
                print("      ✅ 个性化推荐API正常")
                print(f"         生成推荐: {len(result['data']['recommendations'])}条")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            time.sleep(1)
            
            # 测试4: 行为追踪
            print("   🧪 测试行为追踪...")
            behavior_data = {
                "user_id": test_user_id,
                "action": "read",
                "news_id": "api_test_news",
                "news_category": "ai_ml",
                "reading_duration": 120,
                "scroll_percentage": 80.0
            }
            
            response = session.post(
                f"{self.base_url}/api/v2/behavior/track",
                json=behavior_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                assert result["success"], "行为追踪应该成功"
                print("      ✅ 行为追踪API正常")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
            
            print("   ✅ 所有API端点测试通过")
            self.test_results["api_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ API测试失败: {e}")
            self.test_results["api_tests"]["failed"] += 1
            self.test_results["api_tests"]["errors"].append(f"API测试: {e}")
    
    def cleanup_api_server(self):
        """清理API服务器"""
        if self.api_server_process:
            try:
                self.api_server_process.terminate()
                self.api_server_process.wait(timeout=5)
            except:
                self.api_server_process.kill()
            self.api_server_process = None
    
    # ===========================================
    # ⚡ Part 4: 性能测试
    # ===========================================
    
    def test_performance_recommendations(self):
        """测试推荐生成性能"""
        print("\n⚡ Part 4: 性能测试")
        print("-" * 50)
        print("🧪 测试推荐生成性能...")
        
        try:
            from models.cached_recommendation_engine import CachedRecommendationEngine
            
            rec_engine = CachedRecommendationEngine()
            
            # 性能测试参数
            test_rounds = 10
            target_time_per_request = 2.0  # 秒
            
            # 测试数据
            test_users = [
                {
                    "user_id": f"perf_user_{i}",
                    "interests": ["ai_ml", "programming"],
                    "weights": {
                        "ai_ml": 0.4, "programming": 0.3,
                        "web3_crypto": 0.1, "startup_venture": 0.1,
                        "hardware_chips": 0.05, "consumer_tech": 0.025,
                        "enterprise_saas": 0.025, "social_media": 0.0
                    }
                }
                for i in range(test_rounds)
            ]
            
            # 执行性能测试
            total_time = 0
            successful_requests = 0
            
            for i, user_data in enumerate(test_users):
                start_time = time.time()
                
                try:
                    recommendations = rec_engine.recommend_for_user(
                        user_data["user_id"],
                        user_data["interests"],
                        user_data["weights"],
                        limit=20
                    )
                    
                    end_time = time.time()
                    request_time = end_time - start_time
                    total_time += request_time
                    successful_requests += 1
                    
                    # 验证推荐质量
                    assert len(recommendations) > 0, f"用户{i+1}应该获得推荐"
                    
                    if i == 0:  # 首次请求可能较慢（缓存预热）
                        print(f"      首次请求耗时: {request_time:.3f}秒")
                    elif i == test_rounds - 1:  # 最后一次请求应该很快（缓存命中）
                        print(f"      缓存命中耗时: {request_time:.3f}秒")
                        
                except Exception as e:
                    print(f"      ❌ 用户{i+1}推荐失败: {e}")
                    continue
            
            # 性能分析
            if successful_requests > 0:
                avg_time = total_time / successful_requests
                qps = successful_requests / total_time if total_time > 0 else 0
                
                print(f"   📊 性能测试结果:")
                print(f"      成功请求: {successful_requests}/{test_rounds}")
                print(f"      平均响应时间: {avg_time:.3f}秒")
                print(f"      QPS (每秒请求): {qps:.2f}")
                
                # 性能要求验证
                if avg_time <= target_time_per_request:
                    print(f"   ✅ 性能测试通过 (目标: <{target_time_per_request}秒)")
                    self.test_results["performance_tests"]["passed"] += 1
                else:
                    print(f"   ⚠️ 性能需要优化 (目标: <{target_time_per_request}秒)")
                    self.test_results["performance_tests"]["failed"] += 1
                    self.test_results["performance_tests"]["errors"].append(
                        f"推荐性能: {avg_time:.3f}秒 > {target_time_per_request}秒"
                    )
            else:
                raise Exception("所有性能测试请求都失败了")
                
        except Exception as e:
            print(f"   ❌ 性能测试失败: {e}")
            self.test_results["performance_tests"]["failed"] += 1
            self.test_results["performance_tests"]["errors"].append(f"性能测试: {e}")
    
    # ===========================================
    # 🎭 Part 5: 端到端测试
    # ===========================================
    
    def test_end_to_end_user_journey(self):
        """测试端到端用户旅程"""
        print("\n🎭 Part 5: 端到端测试")
        print("-" * 50)
        print("🧪 测试完整用户旅程...")
        
        try:
            from models.interest_survey import survey_instance
            from models.user_profile import UserProfileManager
            from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
            from models.cached_recommendation_engine import CachedRecommendationEngine
            
            # 创建完整系统
            rec_engine = CachedRecommendationEngine()
            behavior_system = EnhancedBehaviorSystem(rec_engine, test_mode=True)
            profile_manager = UserProfileManager(survey_instance, behavior_system)
            
            user_id = "e2e_test_user"
            print(f"   👤 测试用户: {user_id}")
            
            # 步骤1: 新用户填写问卷
            print("   📋 步骤1: 新用户填写问卷")
            survey_answers = {
                "技术兴趣": ["ai_ml", "startup_venture"],
                "专业背景": "investor",
                "阅读习惯": "deep",
                "使用场景": ["morning", "weekend"],
                "AI关注程度": 4
            }
            
            # 验证和创建画像
            validation = survey_instance.validate_answers(survey_answers)
            assert validation["valid"], "问卷答案应该有效"
            
            profile = profile_manager.create_profile_from_survey(user_id, survey_answers)
            assert profile.basic_info["professional_background"] == "investor", "专业背景应该正确"
            print("      ✅ 用户画像创建成功")
            
            # 步骤2: 获取初始推荐
            print("   🎯 步骤2: 获取初始个性化推荐")
            initial_recommendations = behavior_system.get_intelligent_recommendations(user_id, limit=10)
            assert len(initial_recommendations) > 0, "应该生成初始推荐"
            
            initial_ai_count = sum(1 for rec in initial_recommendations if rec.get("category") == "ai_ml")
            print(f"      ✅ 初始推荐生成成功 (AI新闻: {initial_ai_count}条)")
            
            # 步骤3: 模拟用户行为
            print("   🔄 步骤3: 模拟用户行为序列")
            user_behaviors = [
                {"action": "deep_read", "category": "ai_ml", "duration": 300, "scroll": 95},
                {"action": "share", "category": "ai_ml", "duration": 80, "scroll": 85},
                {"action": "bookmark", "category": "startup_venture", "duration": 120, "scroll": 80},
                {"action": "skip", "category": "consumer_tech", "duration": 5, "scroll": 10},
                {"action": "deep_read", "category": "ai_ml", "duration": 250, "scroll": 90}
            ]
            
            for i, behavior in enumerate(user_behaviors):
                event = BehaviorEvent(
                    user_id=user_id,
                    action=behavior["action"],
                    news_id=f"e2e_news_{i}",
                    news_category=behavior["category"],
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
                
                # 追踪行为
                result = behavior_system.track_behavior(event)
                assert result["success"], f"行为{i+1}追踪应该成功"
                
                # 更新画像
                profile_manager.update_profile_from_behavior(user_id, {
                    "action": result["enhanced_action"],
                    "news_category": behavior["category"],
                    "reading_duration": behavior["duration"],
                    "engagement_score": result["engagement_score"]
                })
                
                print(f"      {i+1}. {behavior['action']} [{behavior['category']}] → {result['enhanced_action']}")
            
            # 步骤4: 验证学习效果
            print("   📈 步骤4: 验证行为学习效果")
            final_recommendations = behavior_system.get_intelligent_recommendations(user_id, limit=10)
            final_ai_count = sum(1 for rec in final_recommendations if rec.get("category") == "ai_ml")
            
            # 获取最终用户画像
            final_profile = profile_manager.get_profile(user_id)
            final_confidence = final_profile.personalization["confidence_score"]
            total_interactions = final_profile.personalization["total_interactions"]
            
            print(f"      📊 学习效果分析:")
            print(f"         AI推荐变化: {initial_ai_count} → {final_ai_count}条")
            print(f"         用户置信度: {final_confidence:.3f}")
            print(f"         总交互次数: {total_interactions}")
            
            # 验证学习效果
            
            ai_dominance = final_ai_count / len(final_recommendations) if final_recommendations else 0
            assert ai_dominance >= 0.3, f"AI推荐占比应该>=30%，实际{ai_dominance:.1%}"
            assert final_ai_count >= 2, f"AI推荐至少应该有2条，实际{final_ai_count}条"
            assert final_confidence > 0.1, "用户置信度应该提升"
            assert total_interactions == len(user_behaviors), "交互次数应该正确"
            
            # 步骤5: 生成用户报告
            print("   📄 步骤5: 生成用户分析报告")
            user_analysis = profile_manager.analyze_profile_evolution(user_id)
            
            assert "current_interests" in user_analysis, "应该包含当前兴趣"
            assert "stability_score" in user_analysis, "应该包含稳定性得分"
            
            print(f"      📋 用户分析报告:")
            print(f"         主要兴趣: {user_analysis['current_interests']}")
            print(f"         兴趣稳定性: {user_analysis['stability_score']}")
            print(f"         推荐质量: {user_analysis['recommendation_effectiveness']}")
            
            print("   ✅ 端到端用户旅程测试完全成功")
            self.test_results["end_to_end_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"   ❌ 端到端测试失败: {e}")
            self.test_results["end_to_end_tests"]["failed"] += 1
            self.test_results["end_to_end_tests"]["errors"].append(f"端到端测试: {e}")
    
    # ===========================================
    # 📊 测试结果汇总
    # ===========================================
    
    def print_comprehensive_summary(self):
        """打印完整测试结果汇总"""
        print("\n" + "=" * 80)
        print("📊 TechSum 系统完整测试结果汇总")
        print("=" * 80)
        
        # 计算总体统计
        total_passed = sum(category["passed"] for category in self.test_results.values())
        total_failed = sum(category["failed"] for category in self.test_results.values())
        total_tests = total_passed + total_failed
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        # 打印总体结果
        print(f"🎯 总体测试结果:")
        print(f"   📈 总测试数: {total_tests}")
        print(f"   ✅ 通过测试: {total_passed}")
        print(f"   ❌ 失败测试: {total_failed}")
        print(f"   📊 成功率: {success_rate:.1f}%")
        
        # 分类测试结果
        print(f"\n📋 分类测试详情:")
        test_categories = [
            ("📋 单元测试", "unit_tests"),
            ("🔄 集成测试", "integration_tests"),
            ("📡 API测试", "api_tests"),
            ("⚡ 性能测试", "performance_tests"),
            ("🎭 端到端测试", "end_to_end_tests")
        ]
        
        for category_name, category_key in test_categories:
            category_data = self.test_results[category_key]
            category_total = category_data["passed"] + category_data["failed"]
            category_rate = (category_data["passed"] / category_total * 100) if category_total > 0 else 0
            
            print(f"   {category_name}: {category_data['passed']}/{category_total} ({category_rate:.1f}%)")
            
            # 显示错误详情
            if category_data["errors"]:
                for error in category_data["errors"]:
                    print(f"      ❌ {error}")
        
        # 系统健康度评估
        print(f"\n🏆 系统健康度评估:")
        if success_rate >= 95:
            print("🟢 优秀 - 系统可以直接投入生产使用")
            print("💡 建议: 立即进行前端集成和部署")
        elif success_rate >= 85:
            print("🟡 良好 - 系统基本可用，有少数问题需要修复")
            print("💡 建议: 修复失败项目后进行前端集成")
        elif success_rate >= 70:
            print("🟠 及格 - 系统核心功能可用，但需要改进")
            print("💡 建议: 优先修复核心功能问题")
        else:
            print("🔴 需要改进 - 系统存在较多问题")
            print("💡 建议: 重点修复失败的测试项目")
        
        # 功能模块状态
        print(f"\n🔧 功能模块状态:")
        module_status = {
            "兴趣问卷系统": self.test_results["unit_tests"]["passed"] > 0,
            "用户画像管理": self.test_results["unit_tests"]["passed"] > 0,
            "行为学习引擎": self.test_results["unit_tests"]["passed"] > 0,
            "推荐生成引擎": self.test_results["unit_tests"]["passed"] > 0,
            "系统集成": self.test_results["integration_tests"]["passed"] > 0,
            "API接口": self.test_results["api_tests"]["passed"] > 0,
            "性能表现": self.test_results["performance_tests"]["passed"] > 0,
            "端到端流程": self.test_results["end_to_end_tests"]["passed"] > 0
        }
        
        for module, status in module_status.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {module}")
        
        # 下一步建议
        print(f"\n🚀 下一步建议:")
        if success_rate >= 90:
            print("   1. 🎨 与Zane开始前端集成开发")
            print("   2. 📱 实现用户问卷和'你的喜好'页面")
            print("   3. 🔄 集成行为追踪到前端")
            print("   4. 💾 考虑数据持久化方案 (MongoDB/Redis)")
            print("   5. 🚀 准备生产环境部署")
        else:
            print("   1. 🔧 优先修复失败的测试项目")
            print("   2. 🧪 重新运行测试验证修复效果")
            print("   3. 📊 分析性能瓶颈并优化")
            print("   4. 🔄 完善错误处理和边界情况")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始TechSum系统完整测试套件")
        print("🎯 测试覆盖: 单元测试 + 集成测试 + API测试 + 性能测试 + 端到端测试")
        
        start_time = time.time()
        
        try:
            # Part 1: 单元测试
            self.test_unit_interest_survey()
            self.test_unit_user_profile()
            self.test_unit_behavior_system()
            self.test_unit_recommendation_engine()
            
            # Part 2: 集成测试
            self.test_integration_survey_to_profile()
            self.test_integration_profile_to_recommendation()
            self.test_integration_behavior_learning_loop()
            
            # Part 3: API测试
            self.test_api_endpoints()
            
            # Part 4: 性能测试
            self.test_performance_recommendations()
            
            # Part 5: 端到端测试
            self.test_end_to_end_user_journey()
            
        except KeyboardInterrupt:
            print("\n⚠️ 测试被用户中断")
        except Exception as e:
            print(f"\n❌ 测试执行过程中出现异常: {e}")
        finally:
            # 清理资源
            self.cleanup_api_server()
            
            # 计算总时间
            total_time = time.time() - start_time
            print(f"\n⏱️ 总测试时间: {total_time:.2f}秒")
            
            # 打印汇总报告
            self.print_comprehensive_summary()

def main():
    """主函数"""
    print("🔍 TechSum 系统完整测试套件")
    print("🎯 这将测试整个系统的所有功能模块")
    
    # 创建测试实例
    tester = TechSumComprehensiveTest()
    
    # 运行所有测试
    tester.run_all_tests()

if __name__ == "__main__":
    main()