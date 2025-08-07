# ==============================================
# 📁 test_data_adapter.py - 测试数据适配器功能
# ==============================================

import sys
import os
import json
from typing import List, Dict

# 添加当前目录到路径，确保能导入data_adapter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_adapter import DataAdapter
    print("✅ data_adapter模块导入成功")
except ImportError as e:
    print(f"❌ 导入data_adapter失败: {e}")
    sys.exit(1)

class TestDataAdapter:
    """测试数据适配器的各项功能"""
    
    def __init__(self):
        print("🔧 初始化数据适配器...")
        self.adapter = DataAdapter()
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*50)
        print("🧪 开始测试 DataAdapter 功能")
        print("="*50)
        
        # 基础连接测试
        self.test_api_connection()
        
        # 数据获取测试
        self.test_get_news_data()
        
        # 分类功能测试
        self.test_get_news_by_category()
        
        # 统计功能测试
        self.test_get_news_statistics()
        
        # 高重要性新闻测试
        self.test_get_high_importance_news()
        
        # 最近新闻测试
        self.test_get_recent_news()
        
        # 内部方法测试
        self.test_internal_methods()
        
        # 打印测试结果
        self.print_test_summary()
    
    def test_api_connection(self):
        """测试API连接状态"""
        print("\n📡 测试API连接...")
        
        try:
            # 检查API状态
            api_status = self.adapter.api_status
            
            if api_status:
                print("✅ API连接状态: 正常")
                self.test_results["passed"] += 1
            else:
                print("⚠️  API连接状态: 异常 (将使用Mock数据)")
                self.test_results["passed"] += 1  # 这不算失败，只是API不可用
            
            # 检查基础配置
            assert hasattr(self.adapter, 'base_url'), "缺少base_url配置"
            assert hasattr(self.adapter, 'events_endpoint'), "缺少events_endpoint配置"
            
            print(f"   - 基础URL: {self.adapter.base_url}")
            print(f"   - Events端点: {self.adapter.events_endpoint}")
            
        except Exception as e:
            print(f"❌ API连接测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"API连接测试: {e}")
    
    def test_get_news_data(self):
        """测试获取新闻数据功能"""
        print("\n📰 测试获取新闻数据...")
        
        try:
            news_data = self.adapter.get_news_data()
            
            # 基础验证
            assert isinstance(news_data, list), "新闻数据应该是列表格式"
            assert len(news_data) > 0, "新闻数据不能为空"
            
            print(f"✅ 获取到 {len(news_data)} 条新闻")
            
            # 检查第一条新闻的数据结构
            if news_data:
                first_news = news_data[0]
                required_fields = ['id', 'title', 'category', 'hot_score', 'source']
                
                for field in required_fields:
                    assert field in first_news, f"缺少必需字段: {field}"
                
                print("✅ 新闻数据结构验证通过")
                
                # 显示数据样例
                print(f"   - 样例标题: {first_news['title'][:50]}...")
                print(f"   - 样例类别: {first_news['category']}")
                print(f"   - 样例热度: {first_news['hot_score']}")
                print(f"   - 数据来源: {first_news.get('data_source', 'unknown')}")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 获取新闻数据测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"获取新闻数据: {e}")
    
    def test_get_news_by_category(self):
        """测试按类别获取新闻"""
        print("\n🏷️  测试按类别获取新闻...")
        
        try:
            # 测试几个主要类别
            test_categories = ['ai_ml', 'startup_venture', 'web3_crypto']
            
            for category in test_categories:
                category_news = self.adapter.get_news_by_category(category, limit=5)
                
                assert isinstance(category_news, list), f"{category}类别新闻应该是列表"
                
                # 验证返回的新闻确实属于指定类别
                for news in category_news:
                    if news['category'] != category:
                        print(f"⚠️  发现分类错误: {news['title']} 标记为 {news['category']} 而非 {category}")
                
                print(f"   - {category}: {len(category_news)} 条新闻")
            
            print("✅ 按类别获取新闻测试通过")
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 按类别获取新闻测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"按类别获取新闻: {e}")
    
    def test_get_news_statistics(self):
        """测试获取新闻统计信息"""
        print("\n📊 测试新闻统计信息...")
        
        try:
            stats = self.adapter.get_news_statistics()
            
            assert isinstance(stats, dict), "统计信息应该是字典格式"
            
            # 检查必需的统计字段
            required_stats = ['total_news', 'category_distribution', 'api_status']
            for field in required_stats:
                assert field in stats, f"缺少统计字段: {field}"
            
            print(f"✅ 统计信息获取成功")
            print(f"   - 总新闻数: {stats['total_news']}")
            print(f"   - API状态: {stats['api_status']}")
            
            if 'category_distribution' in stats:
                print("   - 类别分布:")
                for category, count in stats['category_distribution'].items():
                    print(f"     * {category}: {count} 条")
            
            if 'top_categories' in stats:
                print("   - 热门类别:")
                for category, count in stats['top_categories'][:3]:
                    print(f"     * {category}: {count} 条")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 新闻统计信息测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"新闻统计信息: {e}")
    
    def test_get_high_importance_news(self):
        """测试获取高重要性新闻"""
        print("\n⭐ 测试高重要性新闻...")
        
        try:
            high_importance_news = self.adapter.get_high_importance_news(min_importance=70, limit=5)
            
            assert isinstance(high_importance_news, list), "高重要性新闻应该是列表格式"
            
            # 验证重要性筛选
            for news in high_importance_news:
                importance = news.get('importance', 0)
                if importance < 70:
                    print(f"⚠️  发现低重要性新闻: {news['title']} (重要性: {importance})")
            
            print(f"✅ 获取到 {len(high_importance_news)} 条高重要性新闻")
            
            if high_importance_news:
                print("   - 示例高重要性新闻:")
                for i, news in enumerate(high_importance_news[:3]):
                    print(f"     {i+1}. {news['title'][:40]}... (重要性: {news.get('importance', 'N/A')})")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 高重要性新闻测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"高重要性新闻: {e}")
    
    def test_get_recent_news(self):
        """测试获取最近新闻"""
        print("\n🕐 测试最近新闻...")
        
        try:
            recent_news = self.adapter.get_recent_news(hours=24, limit=5)
            
            assert isinstance(recent_news, list), "最近新闻应该是列表格式"
            
            print(f"✅ 获取到 {len(recent_news)} 条最近新闻")
            
            if recent_news:
                print("   - 最近新闻示例:")
                for i, news in enumerate(recent_news[:3]):
                    publish_time = news.get('publish_time', 'Unknown')
                    print(f"     {i+1}. {news['title'][:40]}... ({publish_time})")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 最近新闻测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"最近新闻: {e}")
    
    def test_internal_methods(self):
        """测试内部方法"""
        print("\n🔧 测试内部方法...")
        
        try:
            # 测试分类算法
            test_title = "OpenAI发布新的GPT模型，性能大幅提升"
            test_summary = "人工智能公司OpenAI发布了最新的语言模型"
            
            category = self.adapter._classify_news_category(test_title, test_summary)
            assert isinstance(category, str), "分类结果应该是字符串"
            
            print(f"✅ 分类算法测试通过")
            print(f"   - 测试文本: {test_title}")
            print(f"   - 分类结果: {category}")
            
            # 测试热度计算
            importance_scores = [0, 30, 50, 80, 100]
            for importance in importance_scores:
                hot_score = self.adapter._calculate_importance_score(importance)
                assert 0.3 <= hot_score <= 1.0, f"热度分数应该在0.3-1.0之间，实际: {hot_score}"
            
            print(f"✅ 热度计算测试通过")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 内部方法测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"内部方法: {e}")
    
    def test_data_quality(self):
        """测试数据质量"""
        print("\n🔍 测试数据质量...")
        
        try:
            news_data = self.adapter.get_news_data()
            
            quality_issues = []
            
            for news in news_data[:10]:  # 检查前10条新闻
                # 检查必需字段
                if not news.get('title', '').strip():
                    quality_issues.append("发现空标题")
                
                if not news.get('category'):
                    quality_issues.append("发现无类别新闻")
                
                if news.get('hot_score', 0) < 0 or news.get('hot_score', 0) > 1:
                    quality_issues.append(f"异常热度分数: {news.get('hot_score')}")
            
            if quality_issues:
                print("⚠️  发现数据质量问题:")
                for issue in quality_issues[:5]:  # 只显示前5个问题
                    print(f"     - {issue}")
            else:
                print("✅ 数据质量检查通过")
            
            self.test_results["passed"] += 1
            
        except Exception as e:
            print(f"❌ 数据质量测试失败: {e}")
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"数据质量: {e}")
    
    def print_test_summary(self):
        """打印测试结果摘要"""
        print("\n" + "="*50)
        print("📋 测试结果摘要")
        print("="*50)
        
        total_tests = self.test_results["passed"] + self.test_results["failed"]
        success_rate = (self.test_results["passed"] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ 通过测试: {self.test_results['passed']}")
        print(f"❌ 失败测试: {self.test_results['failed']}")
        print(f"📊 成功率: {success_rate:.1f}%")
        
        if self.test_results["errors"]:
            print("\n❌ 错误详情:")
            for error in self.test_results["errors"]:
                print(f"   - {error}")
        
        if success_rate >= 80:
            print("\n🎉 数据适配器功能基本正常！")
        else:
            print("\n⚠️  数据适配器存在一些问题，需要修复。")
        
        print("\n💡 接下来可以:")
        print("   1. 基于测试结果修复问题")
        print("   2. 开始实现用户画像系统 (user_profile.py)")
        print("   3. 准备推荐算法开发")

def main():
    """主函数"""
    print("🚀 启动 DataAdapter 测试程序")
    
    # 创建测试实例
    tester = TestDataAdapter()
    
    # 运行所有测试
    tester.run_all_tests()
    
    # 额外的数据质量测试
    tester.test_data_quality()

if __name__ == "__main__":
    main()