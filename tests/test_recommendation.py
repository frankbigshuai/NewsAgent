# ==============================================
# 📁 test_cached_recommendation_engine.py - 性能测试
# ==============================================

import sys
import os
import time
from typing import List, Dict

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from cached_recommendation_engine import CachedRecommendationEngine
    print("✅ cached_recommendation_engine模块导入成功")
except ImportError as e:
    print(f"❌ 导入cached_recommendation_engine失败: {e}")
    print("💡 请确保 cached_recommendation_engine.py 文件存在")
    sys.exit(1)

class PerformanceTestSuite:
    """性能测试套件"""
    
    def __init__(self):
        print("🔧 初始化缓存版推荐引擎...")
        self.engine = CachedRecommendationEngine()
        
        # 测试用户数据
        self.test_users = {
            "ai_lover": {
                "user_id": "ai_lover_123",
                "interests": ["ai_ml", "programming"],
                "weights": {
                    "ai_ml": 0.9,
                    "programming": 0.7,
                    "startup_venture": 0.3,
                    "web3_crypto": 0.2,
                    "hardware_chips": 0.5,
                    "consumer_tech": 0.4,
                    "enterprise_saas": 0.3,
                    "social_media": 0.2
                }
            },
            "investor": {
                "user_id": "investor_456",
                "interests": ["startup_venture", "web3_crypto", "ai_ml"],
                "weights": {
                    "startup_venture": 0.9,
                    "web3_crypto": 0.8,
                    "ai_ml": 0.6,
                    "consumer_tech": 0.5,
                    "hardware_chips": 0.4,
                    "programming": 0.3,
                    "enterprise_saas": 0.4,
                    "social_media": 0.2
                }
            },
            "general_user": {
                "user_id": "general_789",
                "interests": ["consumer_tech", "ai_ml"],
                "weights": {
                    "consumer_tech": 0.7,
                    "ai_ml": 0.6,
                    "programming": 0.4,
                    "startup_venture": 0.4,
                    "web3_crypto": 0.3,
                    "hardware_chips": 0.4,
                    "enterprise_saas": 0.3,
                    "social_media": 0.5
                }
            }
        }
    
    def run_all_tests(self):
        """运行所有性能测试"""
        print("\n" + "="*60)
        print("⚡ 开始性能测试 - 缓存优化版推荐引擎")
        print("="*60)
        
        # 冷启动测试
        self.test_cold_start_performance()
        
        # 缓存效果测试
        self.test_cache_effectiveness()
        
        # 并发性能测试
        self.test_concurrent_requests()
        
        # 缓存预热测试
        self.test_cache_warmup()
        
        # 缓存统计展示
        self.show_cache_statistics()
        
        # 缓存管理测试
        self.test_cache_management()
        
        print("\n🎉 性能测试完成！")
    
    def test_cold_start_performance(self):
        """测试冷启动性能"""
        print("\n🥶 测试冷启动性能（无缓存）...")
        
        # 清理所有缓存
        self.engine.clear_cache("all")
        
        ai_user = self.test_users["ai_lover"]
        
        # 第一次请求（冷启动）
        start_time = time.time()
        recommendations = self.engine.recommend_for_user(
            ai_user["user_id"],
            ai_user["interests"],
            ai_user["weights"],
            limit=10
        )
        cold_start_time = time.time() - start_time
        
        print(f"❄️  冷启动时间: {cold_start_time:.3f}秒")
        print(f"📋 生成推荐: {len(recommendations)} 条")
        
        if cold_start_time < 2.0:
            print("✅ 冷启动性能良好")
        elif cold_start_time < 3.0:
            print("⚠️  冷启动性能可接受")
        else:
            print("❌ 冷启动性能需要优化")
    
    def test_cache_effectiveness(self):
        """测试缓存效果"""
        print("\n🚀 测试缓存效果...")
        
        ai_user = self.test_users["ai_lover"]
        
        # 第二次相同请求（应该命中缓存）
        start_time = time.time()
        recommendations = self.engine.recommend_for_user(
            ai_user["user_id"],
            ai_user["interests"],
            ai_user["weights"],
            limit=10
        )
        cached_time = time.time() - start_time
        
        print(f"⚡ 缓存命中时间: {cached_time:.3f}秒")
        
        if cached_time < 0.1:
            print("✅ 缓存效果优秀！")
        elif cached_time < 0.3:
            print("✅ 缓存效果良好")
        elif cached_time < 0.5:
            print("⚠️  缓存效果一般")
        else:
            print("❌ 缓存效果不佳")
        
        # 测试不同用户（部分命中缓存）
        print("\n📊 测试不同用户的缓存效果...")
        
        for user_type, user_data in self.test_users.items():
            start_time = time.time()
            recs = self.engine.recommend_for_user(
                user_data["user_id"],
                user_data["interests"],
                user_data["weights"],
                limit=10
            )
            elapsed = time.time() - start_time
            print(f"   {user_type}: {elapsed:.3f}秒 ({len(recs)}条推荐)")
    
    def test_concurrent_requests(self):
        """测试并发请求性能"""
        print("\n🔥 测试并发请求性能...")
        
        # 模拟5个并发请求
        start_time = time.time()
        
        for i in range(5):
            user_type = list(self.test_users.keys())[i % len(self.test_users)]
            user_data = self.test_users[user_type]
            
            recs = self.engine.recommend_for_user(
                f"{user_data['user_id']}_{i}",
                user_data["interests"],
                user_data["weights"],
                limit=10
            )
        
        total_time = time.time() - start_time
        avg_time = total_time / 5
        
        print(f"🔄 5次并发请求总时间: {total_time:.3f}秒")
        print(f"📊 平均每次请求: {avg_time:.3f}秒")
        
        if avg_time < 0.3:
            print("✅ 并发性能优秀")
        elif avg_time < 0.6:
            print("✅ 并发性能良好")
        else:
            print("⚠️  并发性能可以优化")
    
    def test_cache_warmup(self):
        """测试缓存预热"""
        print("\n🔥 测试缓存预热...")
        
        # 清理缓存
        self.engine.clear_cache("all")
        
        # 准备预热用户数据
        warmup_users = [
            {
                "user_id": "warmup_ai",
                "interests": ["ai_ml", "programming"],
                "weights": {"ai_ml": 0.9, "programming": 0.7}
            },
            {
                "user_id": "warmup_investor", 
                "interests": ["startup_venture", "ai_ml"],
                "weights": {"startup_venture": 0.8, "ai_ml": 0.6}
            }
        ]
        
        # 执行预热
        warmup_start = time.time()
        self.engine.warm_up_cache(warmup_users)
        warmup_time = time.time() - warmup_start
        
        print(f"🔥 缓存预热耗时: {warmup_time:.3f}秒")
        
        # 测试预热后的性能
        test_start = time.time()
        for user in warmup_users:
            recs = self.engine.recommend_for_user(
                user["user_id"],
                user["interests"], 
                user["weights"],
                limit=10
            )
        test_time = time.time() - test_start
        
        print(f"⚡ 预热后请求时间: {test_time:.3f}秒")
    
    def show_cache_statistics(self):
        """显示缓存统计"""
        print("\n📊 缓存统计信息...")
        
        stats = self.engine.get_cache_statistics()
        
        print(f"📈 总请求数: {stats['总请求数']}")
        print(f"💾 新闻缓存命中率: {stats['新闻缓存']['命中率']}")
        print(f"🎯 推荐缓存命中率: {stats['推荐缓存']['命中率']}")
        
        print("\n📦 缓存大小:")
        for cache_type, size in stats['缓存大小'].items():
            print(f"   {cache_type}: {size} 条目")
        
        # 计算性能提升
        news_hit_rate = float(stats['新闻缓存']['命中率'].rstrip('%'))
        rec_hit_rate = float(stats['推荐缓存']['命中率'].rstrip('%'))
        
        if news_hit_rate > 50 or rec_hit_rate > 30:
            print("✅ 缓存效果显著，性能大幅提升！")
        elif news_hit_rate > 20 or rec_hit_rate > 10:
            print("✅ 缓存效果良好")
        else:
            print("⚠️  缓存效果有限，可能需要调整策略")
    
    def test_cache_management(self):
        """测试缓存管理功能"""
        print("\n🧹 测试缓存管理功能...")
        
        # 测试部分清理
        print("🧹 清理推荐缓存...")
        self.engine.clear_cache("recommendations")
        
        print("🧹 清理新闻缓存...")
        self.engine.clear_cache("news")
        
        # 验证缓存已清理
        stats_after = self.engine.get_cache_statistics()
        print(f"📦 清理后缓存大小: {stats_after['缓存大小']}")
        
        print("✅ 缓存管理功能正常")
    
    def benchmark_vs_original(self):
        """
        与原版推荐引擎性能对比
        需要原版 recommendation_engine.py 在同一目录
        """
        print("\n⚔️  性能对比测试...")
        
        try:
            from cached_recommendation_engine import RecommendationEngine
            original_engine = RecommendationEngine()
            print("✅ 原版引擎加载成功")
        except ImportError:
            print("⚠️  无法加载原版引擎，跳过对比测试")
            return
        
        ai_user = self.test_users["ai_lover"]
        test_rounds = 3
        
        # 测试原版引擎
        print("🐌 测试原版引擎性能...")
        original_times = []
        for i in range(test_rounds):
            start = time.time()
            original_engine.recommend_for_user(
                ai_user["user_id"],
                ai_user["interests"],
                ai_user["weights"],
                limit=10
            )
            original_times.append(time.time() - start)
        
        avg_original = sum(original_times) / len(original_times)
        print(f"   原版平均时间: {avg_original:.3f}秒")
        
        # 测试缓存版引擎
        print("🚀 测试缓存版引擎性能...")
        self.engine.clear_cache("all")  # 公平对比，清理缓存
        
        cached_times = []
        for i in range(test_rounds):
            start = time.time()
            self.engine.recommend_for_user(
                ai_user["user_id"],
                ai_user["interests"],
                ai_user["weights"],
                limit=10
            )
            cached_times.append(time.time() - start)
        
        avg_cached = sum(cached_times) / len(cached_times)
        print(f"   缓存版平均时间: {avg_cached:.3f}秒")
        
        # 计算性能提升
        if avg_original > 0:
            improvement = (avg_original - avg_cached) / avg_original * 100
            speedup = avg_original / avg_cached
            
            print(f"\n📈 性能提升:")
            print(f"   时间节省: {improvement:.1f}%")
            print(f"   速度提升: {speedup:.1f}x")
            
            if improvement > 50:
                print("🏆 性能提升显著！")
            elif improvement > 20:
                print("✅ 性能提升明显")
            else:
                print("⚠️  性能提升有限")

def main():
    """主函数"""
    print("🚀 启动缓存版推荐引擎性能测试")
    
    # 创建测试实例
    tester = PerformanceTestSuite()
    
    # 运行所有测试
    tester.run_all_tests()
    
    # 与原版对比（可选）
    print("\n" + "="*60)
    tester.benchmark_vs_original()
    
    print("\n💡 性能优化建议:")
    print("   1. 新闻缓存命中率 >50% = 优秀")
    print("   2. 推荐生成时间 <0.3秒 = 用户体验优秀")
    print("   3. 可以考虑使用Redis实现分布式缓存")
    print("   4. 定期清理过期缓存，避免内存泄漏")

if __name__ == "__main__":
    main()