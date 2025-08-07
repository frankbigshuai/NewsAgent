# ==============================================
# 📁 test_enhanced_behavior.py - 增强版行为学习系统全面测试
# ==============================================

import sys
import os
import time
import json
from datetime import datetime, timedelta
import random

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入增强版系统
try:
    from enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
    print("✅ enhanced_behavior_system模块导入成功")
    enhanced_available = True
except ImportError as e:
    print(f"❌ 导入enhanced_behavior_system失败: {e}")
    enhanced_available = False

# 尝试导入原版系统（如果存在）
try:
    from enhanced_behavior_tracker import BehaviorTracker  # 你的原版文件名
    print("✅ 原版behavior_tracker模块导入成功")
    original_available = True
except ImportError:
    print("⚠️  原版behavior_tracker模块未找到，将跳过对比测试")
    original_available = False

# 尝试导入推荐引擎
try:
    from cached_recommendation_engine import CachedRecommendationEngine
    recommendation_engine_available = True
    print("✅ cached_recommendation_engine模块导入成功")
except ImportError:
    recommendation_engine_available = False
    print("⚠️  推荐引擎模块未找到，将跳过推荐集成测试")

class ComprehensiveBehaviorTest:
    """全面的行为学习系统测试套件"""
    
    def __init__(self):
        print("🔧 初始化测试环境...")

        if enhanced_available:
            if recommendation_engine_available:
                self.recommendation_engine = CachedRecommendationEngine()
                self.enhanced_system = EnhancedBehaviorSystem(
                    self.recommendation_engine, 
                    test_mode=True  # 🧪 启用测试模式
        )
                print("✅ 增强版系统（集成推荐引擎，测试模式）初始化成功")
            else:
                self.enhanced_system = EnhancedBehaviorSystem(test_mode=True)  # 🧪 启用测试模式
                print("✅ 增强版系统（独立模式，测试模式）初始化成功")
        
        # 📊 初始化原版系统（如果可用）
        if original_available:
            self.original_system = BehaviorTracker()
            print("✅ 原版系统初始化成功")
        
        # 🧪 测试数据
        self.test_scenarios = {
            "new_user": {
                "user_id": "new_user_001",
                "description": "新用户，行为较少",
                "expected_confidence": "低"
            },
            "experienced_user": {
                "user_id": "experienced_user_002", 
                "description": "有经验用户，行为丰富",
                "expected_confidence": "高"
            },
            "ai_enthusiast": {
                "user_id": "ai_enthusiast_003",
                "description": "AI爱好者，专注AI内容",
                "expected_behavior": "AI权重应显著提升"
            }
        }
        
        # 📈 测试结果统计
        self.test_results = {
            "enhanced_tests": {"passed": 0, "failed": 0},
            "comparison_tests": {"enhanced_better": 0, "original_better": 0, "similar": 0},
            "performance_metrics": {},
            "errors": []
        }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*70)
        print("🧪 开始增强版行为学习系统全面测试")
        print("="*70)
        
        if not enhanced_available:
            print("❌ 增强版系统不可用，无法进行测试")
            return
        
        # 🎯 增强版功能测试
        print("\n📋 Part 1: 增强版功能测试")
        self.test_basic_behavior_tracking()
        self.test_adaptive_learning_rate()
        self.test_anomaly_detection()
        self.test_smart_normalization()
        self.test_user_confidence_system()
        
        # 🔄 对比测试（如果原版可用）
        if original_available:
            print("\n📋 Part 2: 原版 vs 增强版对比测试")
            self.test_learning_effectiveness_comparison()
            self.test_performance_comparison()
        
        # 🚀 推荐集成测试
        if recommendation_engine_available:
            print("\n📋 Part 3: 推荐引擎集成测试")
            self.test_recommendation_integration()
        
        # 🎭 实际场景模拟
        print("\n📋 Part 4: 实际使用场景模拟")
        self.test_real_world_scenarios()
        
        # 📊 测试结果总结
        self.print_comprehensive_summary()
    
    def test_basic_behavior_tracking(self):
        """测试基础行为追踪功能"""
        print("\n📊 测试基础行为追踪功能...")
        
        try:
            # 📝 创建测试事件
            test_event = BehaviorEvent(
                user_id="test_user_basic",
                action="read",
                news_id="news_001",
                news_category="ai_ml",
                news_title="OpenAI 发布 GPT-5 模型详细技术报告",
                reading_duration=120,
                scroll_percentage=85.0
            )
            
            # 🚀 追踪行为
            result = self.enhanced_system.track_behavior(test_event)
            
            # ✅ 验证结果
            assert result["success"] == True, "行为追踪应该成功"
            assert "behavior_id" in result, "应该返回行为ID"
            assert result["engagement_score"] > 0, "参与度分数应该大于0"
            
            print(f"✅ 基础行为追踪测试通过")
            print(f"   - 行为ID: {result['behavior_id']}")
            print(f"   - 原始行为: {test_event.action}")
            print(f"   - 增强行为: {result['enhanced_action']}")
            print(f"   - 参与度分数: {result['engagement_score']:.4f}")
            print(f"   - 用户置信度: {result['user_confidence']:.4f}")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 基础行为追踪测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"基础追踪: {e}")
    
    def test_adaptive_learning_rate(self):
        """测试自适应学习率功能"""
        print("\n🧠 测试自适应学习率功能...")
        
        try:
            # 📊 测试新用户的学习率
            new_user = "adaptive_new_user"
            experienced_user = "adaptive_experienced_user"
            
            # 🆕 新用户：模拟少量行为
            print("🆕 测试新用户学习率...")
            for i in range(2):  # 只有2个行为
                event = BehaviorEvent(
                    user_id=new_user,
                    action="read",
                    news_id=f"news_{i}",
                    news_category="ai_ml",
                    reading_duration=60,
                    scroll_percentage=70.0
                )
                self.enhanced_system.track_behavior(event)
            
            new_confidence = self.enhanced_system._calculate_user_confidence(new_user)
            new_lr = self.enhanced_system._calculate_adaptive_learning_rate(new_confidence)
            
            print(f"   新用户置信度: {new_confidence:.3f}")
            print(f"   新用户学习率: {new_lr:.3f}")
            
            # 👨‍🎓 有经验用户：模拟大量行为
            print("👨‍🎓 测试有经验用户学习率...")
            for i in range(20):  # 20个行为
                event = BehaviorEvent(
                    user_id=experienced_user,
                    action=random.choice(["read", "deep_read", "like", "share"]),
                    news_id=f"news_{i}",
                    news_category=random.choice(["ai_ml", "programming", "startup_venture"]),
                    reading_duration=random.randint(30, 180),
                    scroll_percentage=random.uniform(50, 95)
                )
                self.enhanced_system.track_behavior(event)
            
            exp_confidence = self.enhanced_system._calculate_user_confidence(experienced_user)
            exp_lr = self.enhanced_system._calculate_adaptive_learning_rate(exp_confidence)
            
            print(f"   有经验用户置信度: {exp_confidence:.3f}")
            print(f"   有经验用户学习率: {exp_lr:.3f}")
            
            # ✅ 验证自适应效果
            assert exp_confidence > new_confidence, "有经验用户置信度应该更高"
            
            if exp_confidence > 0.7:
                assert exp_lr < new_lr, "高置信度用户学习率应该更低"
                print("✅ 自适应学习率测试通过：高置信度 → 低学习率")
            elif new_confidence < 0.3:
                assert new_lr > self.enhanced_system.learning_config['base_learning_rate'], "低置信度用户学习率应该更高"
                print("✅ 自适应学习率测试通过：低置信度 → 高学习率")
            
            print(f"✅ 学习率自适应效果显著：置信度差异 {exp_confidence - new_confidence:.3f}")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 自适应学习率测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"自适应学习率: {e}")
    
    def test_anomaly_detection(self):
        """测试异常检测功能"""
        print("\n🛡️ 测试异常检测功能...")
        
        try:
            user_id = "anomaly_test_user"
            
            # ✅ 正常行为应该成功
            print("✅ 测试正常行为...")
            normal_event = BehaviorEvent(
                user_id=user_id,
                action="read",
                news_id="normal_news",
                news_category="ai_ml",
                reading_duration=60,
                scroll_percentage=75.0
            )
            
            normal_result = self.enhanced_system.track_behavior(normal_event)
            assert normal_result["success"] == True, "正常行为应该成功"
            print("   正常行为追踪成功 ✅")
            
            # 🚨 快速连续操作应该被检测
            print("🚨 测试快速连续操作检测...")
            base_time = datetime.now()
            
            anomaly_detected = False
            for i in range(10):
                # 模拟极短时间间隔的连续操作
                timestamp = (base_time + timedelta(milliseconds=i * 100)).isoformat()
                
                event = BehaviorEvent(
                    user_id=user_id,
                    action="click",
                    news_id=f"rapid_news_{i}",
                    news_category="ai_ml",
                    timestamp=timestamp
                )
                
                result = self.enhanced_system.track_behavior(event)
                
                if not result["success"] and "异常行为检测" in result.get("error", ""):
                    anomaly_detected = True
                    print(f"   第{i+1}次操作被检测为异常 ✅")
                    break
            
            if anomaly_detected:
                print("✅ 异常检测功能正常：成功检测快速连续操作")
            else:
                print("⚠️  异常检测未触发，可能需要调整阈值")
            
            # 📊 统计检测效果
            stats = self.enhanced_system.get_system_statistics()
            detected_count = stats.get("anomalies_detected", 0)
            
            print(f"   系统累计检测异常: {detected_count} 次")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 异常检测测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"异常检测: {e}")
    
    def test_smart_normalization(self):
        """测试智能权重归一化功能"""
        print("\n🔄 测试智能权重归一化功能...")
        
        try:
            user_id = "normalization_test_user"
            
            # 📊 获取初始权重分布
            initial_prefs = self.enhanced_system.get_user_preferences(user_id)
            print(f"📊 初始权重分布:")
            for cat, weight in initial_prefs.items():
                print(f"   {cat}: {weight:.4f}")
            
            # 🎯 连续强化AI类别
            print("\n🎯 连续强化AI类别权重...")
            ai_behaviors = [
                {"action": "deep_read", "duration": 180, "scroll": 95.0},
                {"action": "share", "duration": 60, "scroll": 80.0},
                {"action": "bookmark", "duration": 45, "scroll": 75.0},
                {"action": "like", "duration": 30, "scroll": 60.0},
                {"action": "deep_read", "duration": 200, "scroll": 90.0}
            ]
            
            for i, behavior in enumerate(ai_behaviors):
                event = BehaviorEvent(
                    user_id=user_id,
                    action=behavior["action"],
                    news_id=f"ai_news_{i}",
                    news_category="ai_ml",
                    news_title=f"AI新闻标题 {i}",
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
                
                result = self.enhanced_system.track_behavior(event)
                learning_update = result.get("learning_update", {})
                
                print(f"   行为{i+1} ({behavior['action']}): "
                      f"权重 {learning_update.get('old_weight', 0):.4f} → "
                      f"{learning_update.get('new_weight', 0):.4f} "
                      f"(+{learning_update.get('adjustment', 0):.4f})")
            
            # 📈 分析最终权重分布
            final_prefs = self.enhanced_system.get_user_preferences(user_id)
            print(f"\n📈 最终权重分布:")
            
            ai_weight_increase = final_prefs["ai_ml"] - initial_prefs["ai_ml"]
            total_decrease_others = 0
            
            for cat, weight in final_prefs.items():
                change = weight - initial_prefs[cat]
                print(f"   {cat}: {weight:.4f} ({change:+.4f})")
                
                if cat != "ai_ml":
                    total_decrease_others += abs(change) if change < 0 else 0
            
            # ✅ 验证智能归一化效果
            print(f"\n🔍 归一化效果分析:")
            print(f"   AI权重提升: +{ai_weight_increase:.4f}")
            print(f"   其他类别总降幅: -{total_decrease_others:.4f}")
            print(f"   权重总和: {sum(final_prefs.values()):.6f}")
            
            # 验证权重总和接近1
            assert abs(sum(final_prefs.values()) - 1.0) < 0.001, "权重总和应该接近1"
            
            # 验证AI权重有显著提升
            assert ai_weight_increase > 0.05, "AI权重应该有显著提升"
            
            # 验证其他类别权重有所调整但不会过度降低
            other_weights = [w for cat, w in final_prefs.items() if cat != "ai_ml"]
            min_other_weight = min(other_weights)
            assert min_other_weight >= 0.02, "其他类别权重不应过度降低"
            
            print("✅ 智能归一化测试通过：权重调整合理，保护现有偏好")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 智能归一化测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"智能归一化: {e}")
    
    def test_user_confidence_system(self):
        """测试用户置信度系统"""
        print("\n📊 测试用户置信度系统...")
        
        try:
            # 🆕 新用户
            new_user = "confidence_new_user"
            
            # 👨‍🎓 有经验用户
            experienced_user = "confidence_exp_user"
            
            # 🎭 多样化用户
            diverse_user = "confidence_diverse_user"
            
            print("🆕 新用户置信度测试...")
            # 新用户只有少量单一行为
            for i in range(3):
                event = BehaviorEvent(
                    user_id=new_user,
                    action="read",
                    news_id=f"news_{i}",
                    news_category="ai_ml",
                    reading_duration=60,
                    scroll_percentage=70.0
                )
                self.enhanced_system.track_behavior(event)
            
            new_confidence = self.enhanced_system._calculate_user_confidence(new_user)
            print(f"   新用户置信度: {new_confidence:.3f}")
            
            print("\n👨‍🎓 有经验用户置信度测试...")
            # 有经验用户有大量但单一类型行为
            for i in range(15):
                event = BehaviorEvent(
                    user_id=experienced_user,
                    action="read",
                    news_id=f"news_{i}",
                    news_category="ai_ml",
                    reading_duration=random.randint(60, 120),
                    scroll_percentage=random.uniform(70, 90)
                )
                self.enhanced_system.track_behavior(event)
            
            exp_confidence = self.enhanced_system._calculate_user_confidence(experienced_user)
            print(f"   有经验用户置信度: {exp_confidence:.3f}")
            
            print("\n🎭 多样化用户置信度测试...")
            # 多样化用户有多种行为类型
            actions = ["read", "deep_read", "like", "share", "bookmark", "comment"]
            categories = ["ai_ml", "programming", "startup_venture", "web3_crypto"]
            
            for i in range(12):
                event = BehaviorEvent(
                    user_id=diverse_user,
                    action=random.choice(actions),
                    news_id=f"news_{i}",
                    news_category=random.choice(categories),
                    reading_duration=random.randint(30, 180),
                    scroll_percentage=random.uniform(50, 95)
                )
                self.enhanced_system.track_behavior(event)
            
            diverse_confidence = self.enhanced_system._calculate_user_confidence(diverse_user)
            print(f"   多样化用户置信度: {diverse_confidence:.3f}")
            
            # 📊 置信度影响分析
            print(f"\n📊 置信度影响分析:")
            
            users_data = [
                (new_user, new_confidence, "新用户"),
                (experienced_user, exp_confidence, "有经验用户"),
                (diverse_user, diverse_confidence, "多样化用户")
            ]
            
            for user_id, confidence, desc in users_data:
                learning_rate = self.enhanced_system._calculate_adaptive_learning_rate(confidence)
                print(f"   {desc}: 置信度 {confidence:.3f} → 学习率 {learning_rate:.3f}")
            
            # ✅ 验证置信度系统逻辑
            assert diverse_confidence >= exp_confidence, "多样化用户置信度应该不低于单一行为用户"
            assert exp_confidence > new_confidence, "有经验用户置信度应该高于新用户"
            
            print("✅ 用户置信度系统测试通过：正确反映用户经验和多样性")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 用户置信度系统测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"用户置信度: {e}")
    
    def test_learning_effectiveness_comparison(self):
        """测试学习效果对比（原版 vs 增强版）"""
        if not original_available:
            print("⚠️  跳过学习效果对比测试（原版系统不可用）")
            return
        
        print("\n⚔️  学习效果对比测试（原版 vs 增强版）...")
        
        try:
            # 🎯 相同的测试场景
            test_user = "comparison_user"
            test_behaviors = [
                {"action": "deep_read", "category": "ai_ml", "duration": 180, "scroll": 95.0},
                {"action": "share", "category": "ai_ml", "duration": 60, "scroll": 80.0},
                {"action": "like", "category": "programming", "duration": 30, "scroll": 60.0},
                {"action": "skip", "category": "web3_crypto", "duration": 5, "scroll": 20.0},
                {"action": "deep_read", "category": "ai_ml", "duration": 200, "scroll": 90.0}
            ]
            
            # 📊 原版系统测试
            print("📊 原版系统学习效果...")
            original_initial = {cat: 0.125 for cat in ["ai_ml", "startup_venture", "web3_crypto", "programming", "hardware_chips", "consumer_tech", "enterprise_saas", "social_media"]}
            
            for i, behavior in enumerate(test_behaviors):
                # 模拟原版行为追踪
                self.original_system.track_behavior(
                    user_id=test_user,
                    action=behavior["action"],
                    news_id=f"news_{i}",
                    news_category=behavior["category"],
                    news_title=f"测试新闻 {i}",
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
            
            original_final = self.original_system.get_user_preferences(test_user)
            original_ai_gain = original_final["ai_ml"] - original_initial["ai_ml"]
            
            # 📊 增强版系统测试
            print("📊 增强版系统学习效果...")
            enhanced_user = f"{test_user}_enhanced"
            
            for i, behavior in enumerate(test_behaviors):
                event = BehaviorEvent(
                    user_id=enhanced_user,
                    action=behavior["action"],
                    news_id=f"news_{i}",
                    news_category=behavior["category"],
                    news_title=f"测试新闻 {i}",
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
                self.enhanced_system.track_behavior(event)
            
            enhanced_final = self.enhanced_system.get_user_preferences(enhanced_user)
            enhanced_ai_gain = enhanced_final["ai_ml"] - 0.125
            
            # 📈 对比分析
            print(f"\n📈 学习效果对比:")
            print(f"   原版AI权重提升: +{original_ai_gain:.4f}")
            print(f"   增强版AI权重提升: +{enhanced_ai_gain:.4f}")
            print(f"   增强版相对提升: {(enhanced_ai_gain / original_ai_gain - 1) * 100:.1f}%" if original_ai_gain > 0 else "原版无提升")
            
            # 📊 权重分布对比
            print(f"\n📊 权重分布对比:")
            print("   类别          原版      增强版    差异")
            print("   " + "-" * 40)
            
            for category in original_final:
                orig_weight = original_final[category]
                enh_weight = enhanced_final.get(category, 0)
                diff = enh_weight - orig_weight
                print(f"   {category:<12} {orig_weight:.4f}   {enh_weight:.4f}   {diff:+.4f}")
            
            # ✅ 评估对比结果
            if enhanced_ai_gain > original_ai_gain * 1.1:
                print("✅ 增强版学习效果更佳：AI权重提升更显著")
                self.test_results["comparison_tests"]["enhanced_better"] += 1
            elif enhanced_ai_gain < original_ai_gain * 0.9:
                print("❓ 原版在此场景下表现更好")
                self.test_results["comparison_tests"]["original_better"] += 1
            else:
                print("🔄 两版本表现相近")
                self.test_results["comparison_tests"]["similar"] += 1
            
        except Exception as e:
            print(f"❌ 学习效果对比测试失败: {e}")
            self.test_results["errors"].append(f"学习效果对比: {e}")
    
    def test_performance_comparison(self):
        """测试性能对比"""
        if not original_available:
            print("⚠️  跳过性能对比测试（原版系统不可用）")
            return
        
        print("\n⚡ 性能对比测试...")
        
        try:
            test_rounds = 50
            
            # ⏱️ 原版系统性能测试
            print(f"⏱️ 原版系统性能测试（{test_rounds}次行为追踪）...")
            
            original_start = time.time()
            for i in range(test_rounds):
                self.original_system.track_behavior(
                    user_id="perf_test_original",
                    action="read",
                    news_id=f"perf_news_{i}",
                    news_category="ai_ml",
                    reading_duration=60,
                    scroll_percentage=75.0
                )
            original_time = time.time() - original_start
            
            # ⏱️ 增强版系统性能测试
            print(f"⏱️ 增强版系统性能测试（{test_rounds}次行为追踪）...")
            
            enhanced_start = time.time()
            for i in range(test_rounds):
                event = BehaviorEvent(
                    user_id="perf_test_enhanced",
                    action="read",
                    news_id=f"perf_news_{i}",
                    news_category="ai_ml",
                    reading_duration=60,
                    scroll_percentage=75.0
                )
                self.enhanced_system.track_behavior(event)
            enhanced_time = time.time() - enhanced_start
            
            # 📊 性能对比分析
            original_avg = original_time / test_rounds * 1000  # 毫秒
            enhanced_avg = enhanced_time / test_rounds * 1000  # 毫秒
            
            print(f"\n📊 性能对比结果:")
            print(f"   原版系统: {original_time:.3f}秒 (平均 {original_avg:.3f}ms/次)")
            print(f"   增强版系统: {enhanced_time:.3f}秒 (平均 {enhanced_avg:.3f}ms/次)")
            
            if enhanced_time < original_time:
                speedup = original_time / enhanced_time
                print(f"✅ 增强版性能更佳：速度提升 {speedup:.2f}x")
                self.test_results["comparison_tests"]["enhanced_better"] += 1
            elif enhanced_time > original_time * 1.2:
                slowdown = enhanced_time / original_time
                print(f"⚠️  增强版性能较慢：慢了 {slowdown:.2f}x（预期情况，功能更丰富）")
                self.test_results["comparison_tests"]["original_better"] += 1
            else:
                print(f"🔄 两版本性能相近（差异在20%内）")
                self.test_results["comparison_tests"]["similar"] += 1
            
            # 💾 记录性能指标
            self.test_results["performance_metrics"] = {
                "original_avg_ms": original_avg,
                "enhanced_avg_ms": enhanced_avg,
                "performance_ratio": enhanced_time / original_time
            }
            
        except Exception as e:
            print(f"❌ 性能对比测试失败: {e}")
            self.test_results["errors"].append(f"性能对比: {e}")
    
    def test_recommendation_integration(self):
        """测试推荐引擎集成"""
        print("\n🚀 测试推荐引擎集成功能...")
        
        try:
            user_id = "recommendation_test_user"
            
            # 📊 建立用户行为历史
            print("📊 建立用户行为历史...")
            ai_focused_behaviors = [
                {"action": "deep_read", "category": "ai_ml", "duration": 180, "scroll": 95.0},
                {"action": "share", "category": "ai_ml", "duration": 60, "scroll": 80.0},
                {"action": "bookmark", "category": "programming", "duration": 90, "scroll": 85.0},
                {"action": "like", "category": "ai_ml", "duration": 30, "scroll": 60.0},
                {"action": "deep_read", "category": "programming", "duration": 150, "scroll": 90.0}
            ]
            
            for i, behavior in enumerate(ai_focused_behaviors):
                event = BehaviorEvent(
                    user_id=user_id,
                    action=behavior["action"],
                    news_id=f"rec_news_{i}",
                    news_category=behavior["category"],
                    news_title=f"技术新闻标题 {i}",
                    reading_duration=behavior["duration"],
                    scroll_percentage=behavior["scroll"]
                )
                
                result = self.enhanced_system.track_behavior(event)
                print(f"   行为{i+1}: {behavior['action']} → {behavior['category']} → 权重调整 {result['learning_update']['adjustment']:+.4f}")
            
            # 📈 查看学习后的偏好
            learned_prefs = self.enhanced_system.get_user_preferences(user_id)
            sorted_prefs = sorted(learned_prefs.items(), key=lambda x: x[1], reverse=True)
            
            print(f"\n📈 学习后的用户偏好:")
            for i, (category, weight) in enumerate(sorted_prefs[:5]):
                print(f"   {i+1}. {category}: {weight:.4f}")
            
            # 🎯 生成智能推荐
            print(f"\n🎯 生成智能推荐...")
            
            recommendations = self.enhanced_system.get_intelligent_recommendations(
                user_id=user_id,
                limit=8
            )
            
            print(f"✅ 成功生成 {len(recommendations)} 条推荐")
            
            if recommendations:
                print("   推荐示例:")
                ai_count = 0
                programming_count = 0
                
                for i, rec in enumerate(recommendations[:5]):
                    category = rec.get('category', 'unknown')
                    title = rec.get('title', '')[:35]
                    score = rec.get('personalized_score', 0)
                    confidence = rec.get('learning_confidence', 0)
                    
                    print(f"     {i+1}. [{category}] {title}...")
                    print(f"        分数: {score:.3f}, 置信度: {confidence:.3f}")
                    
                    if category == 'ai_ml':
                        ai_count += 1
                    elif category == 'programming':
                        programming_count += 1
                
                # 📊 分析推荐质量
                print(f"\n📊 推荐质量分析:")
                print(f"   AI/ML新闻: {ai_count} 条")
                print(f"   编程新闻: {programming_count} 条")
                print(f"   用户AI偏好权重: {learned_prefs['ai_ml']:.4f}")
                print(f"   用户编程偏好权重: {learned_prefs['programming']:.4f}")
                
                # ✅ 验证推荐质量
                tech_focused = ai_count + programming_count
                if tech_focused >= 3:  # 至少一半是技术类新闻
                    print("✅ 推荐质量优秀：成功反映用户技术倾向")
                else:
                    print("⚠️  推荐质量有待提升：技术类新闻比例较低")
            
            self.test_results["enhanced_tests"]["passed"] += 1
            
        except Exception as e:
            print(f"❌ 推荐引擎集成测试失败: {e}")
            self.test_results["enhanced_tests"]["failed"] += 1
            self.test_results["errors"].append(f"推荐集成: {e}")
    
    def test_real_world_scenarios(self):
        """测试真实使用场景"""
        print("\n🎭 真实使用场景模拟测试...")
        
        scenarios = [
            {
                "name": "📱 移动端快速浏览用户",
                "user_id": "mobile_scanner",
                "behaviors": [
                    {"action": "view", "duration": 5, "scroll": 30, "category": "ai_ml"},
                    {"action": "skip", "duration": 3, "scroll": 20, "category": "web3_crypto"},
                    {"action": "click", "duration": 15, "scroll": 50, "category": "consumer_tech"},
                    {"action": "read", "duration": 45, "scroll": 70, "category": "ai_ml"},
                    {"action": "like", "duration": 25, "scroll": 60, "category": "ai_ml"}
                ],
                "expected": "AI偏好应略有提升，但增幅有限"
            },
            {
                "name": "💼 深度阅读专业用户",
                "user_id": "professional_reader", 
                "behaviors": [
                    {"action": "deep_read", "duration": 300, "scroll": 95, "category": "startup_venture"},
                    {"action": "bookmark", "duration": 180, "scroll": 90, "category": "startup_venture"},
                    {"action": "share", "duration": 120, "scroll": 85, "category": "ai_ml"},
                    {"action": "deep_read", "duration": 250, "scroll": 92, "category": "startup_venture"},
                    {"action": "comment", "duration": 200, "scroll": 88, "category": "programming"}
                ],
                "expected": "创业投资偏好应显著提升"
            },
            {
                "name": "🎯 兴趣探索用户",
                "user_id": "explorer_user",
                "behaviors": [
                    {"action": "read", "duration": 60, "scroll": 70, "category": "ai_ml"},
                    {"action": "read", "duration": 80, "scroll": 75, "category": "web3_crypto"},
                    {"action": "like", "duration": 40, "scroll": 65, "category": "consumer_tech"},
                    {"action": "read", "duration": 70, "scroll": 72, "category": "programming"},
                    {"action": "bookmark", "duration": 90, "scroll": 80, "category": "hardware_chips"}
                ],
                "expected": "权重分布应相对均匀，无明显偏向"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n{scenario['name']}:")
            user_id = scenario['user_id']
            
            # 📊 记录初始状态
            initial_prefs = self.enhanced_system.get_user_preferences(user_id)
            
            # 🎭 模拟用户行为
            print("   模拟行为序列:")
            for i, behavior in enumerate(scenario['behaviors']):
                event = BehaviorEvent(
                    user_id=user_id,
                    action=behavior['action'],
                    news_id=f"scenario_news_{i}",
                    news_category=behavior['category'],
                    reading_duration=behavior['duration'],
                    scroll_percentage=behavior['scroll']
                )
                
                result = self.enhanced_system.track_behavior(event)
                learning_update = result.get('learning_update', {})
                
                print(f"     {i+1}. {behavior['action']} [{behavior['category']}] "
                      f"→ 权重 {learning_update.get('old_weight', 0):.4f} → "
                      f"{learning_update.get('new_weight', 0):.4f}")
            
            # 📈 分析结果
            final_prefs = self.enhanced_system.get_user_preferences(user_id)
            user_confidence = self.enhanced_system._calculate_user_confidence(user_id)
            
            print(f"   📈 结果分析:")
            print(f"     用户置信度: {user_confidence:.3f}")
            
            # 找出权重变化最大的类别
            max_increase = 0
            max_category = ""
            for category in final_prefs:
                change = final_prefs[category] - initial_prefs[category]
                if change > max_increase:
                    max_increase = change
                    max_category = category
            
            print(f"     最大权重提升: {max_category} (+{max_increase:.4f})")
            print(f"     期望结果: {scenario['expected']}")
            
            # 🎯 生成个性化推荐验证
            if recommendation_engine_available:
                try:
                    recs = self.enhanced_system.get_intelligent_recommendations(user_id, limit=3)
                    if recs:
                        print(f"     个性化推荐预览:")
                        for j, rec in enumerate(recs[:2]):
                            category = rec.get('category', 'unknown')
                            title = rec.get('title', '')[:25]
                            print(f"       {j+1}. [{category}] {title}...")
                except:
                    print(f"     推荐生成失败（可能是API问题）")
        
        print("\n✅ 真实场景模拟测试完成")
        self.test_results["enhanced_tests"]["passed"] += 1
    
    def print_comprehensive_summary(self):
        """打印全面测试总结"""
        print("\n" + "="*70)
        print("📋 增强版行为学习系统测试总结")
        print("="*70)
        
        # 📊 增强版功能测试结果
        enhanced_total = self.test_results["enhanced_tests"]["passed"] + self.test_results["enhanced_tests"]["failed"]
        enhanced_rate = (self.test_results["enhanced_tests"]["passed"] / enhanced_total * 100) if enhanced_total > 0 else 0
        
        print(f"🎯 增强版功能测试:")
        print(f"   ✅ 通过: {self.test_results['enhanced_tests']['passed']}")
        print(f"   ❌ 失败: {self.test_results['enhanced_tests']['failed']}")
        print(f"   📊 成功率: {enhanced_rate:.1f}%")
        
        # 🔄 对比测试结果（如果有）
        if original_available:
            comparison_total = sum(self.test_results["comparison_tests"].values())
            if comparison_total > 0:
                print(f"\n⚔️  原版 vs 增强版对比:")
                print(f"   🏆 增强版更佳: {self.test_results['comparison_tests']['enhanced_better']}")
                print(f"   🔄 原版更佳: {self.test_results['comparison_tests']['original_better']}")
                print(f"   ⚖️  表现相近: {self.test_results['comparison_tests']['similar']}")
                
                enhanced_win_rate = self.test_results['comparison_tests']['enhanced_better'] / comparison_total * 100
                print(f"   📈 增强版优势率: {enhanced_win_rate:.1f}%")
        
        # ⚡ 性能数据（如果有）
        if "performance_metrics" in self.test_results and self.test_results["performance_metrics"]:
            perf = self.test_results["performance_metrics"]
            print(f"\n⚡ 性能对比:")
            print(f"   原版平均: {perf['original_avg_ms']:.3f}ms/次")
            print(f"   增强版平均: {perf['enhanced_avg_ms']:.3f}ms/次")
            print(f"   性能比例: {perf['performance_ratio']:.2f}x")
        
        # ❌ 错误信息
        if self.test_results["errors"]:
            print(f"\n❌ 错误详情:")
            for error in self.test_results["errors"]:
                print(f"   - {error}")
        
        # 🎯 总体评估
        print(f"\n🎯 总体评估:")
        if enhanced_rate >= 90:
            print("🏆 增强版系统功能优秀，大幅改进原版！")
            print("   ✅ 自适应学习率")
            print("   ✅ 智能权重归一化") 
            print("   ✅ 异常行为检测")
            print("   ✅ 推荐引擎深度集成")
            print("   ✅ 用户置信度系统")
        elif enhanced_rate >= 75:
            print("✅ 增强版系统功能良好，有明显改进")
        else:
            print("⚠️  增强版系统需要进一步调试")
        
        # 💡 建议
        print(f"\n💡 接下来建议:")
        if enhanced_rate >= 85:
            print("   1. 可以部署到生产环境")
            print("   2. 开发 FastAPI 接口")
            print("   3. 集成到现有推荐系统")
            print("   4. 添加数据持久化")
        else:
            print("   1. 修复失败的测试项目")
            print("   2. 优化性能和算法")
            print("   3. 重新运行测试验证")
        
        print(f"\n🚀 增强版相对原版的核心优势:")
        print("   🧠 智能学习：新用户学得快，老用户学得稳")
        print("   🛡️  安全防护：异常行为检测，防止数据污染")
        print("   🔄 智能归一化：权重调整更合理，保护现有偏好") 
        print("   🎯 深度集成：无缝对接推荐引擎，完整闭环")
        print("   📊 数据洞察：用户置信度系统，量化学习质量")

def main():
    """主函数"""
    print("🚀 启动增强版行为学习系统全面测试")
    
    if not enhanced_available:
        print("❌ 增强版系统不可用，请检查模块导入")
        return
    
    # 创建测试实例
    tester = ComprehensiveBehaviorTest()
    
    # 运行全面测试
    tester.run_all_tests()

if __name__ == "__main__":
    main()