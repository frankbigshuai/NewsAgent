#!/usr/bin/env python3
# test_gemini_fixed.py - 修正后的测试新闻分类系统

import sys
import os
import traceback
from typing import Dict, Any

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_category_config():
    """测试统一配置文件"""
    print("🧪 测试 category_config.py...")
    
    try:
        from models.category_config import (
            CATEGORIES, CATEGORY_KEYWORDS, CORE_KEYWORDS, 
            CHINESE_CATEGORIES, get_category_display_name,
            get_all_categories, get_category_keywords
        )
        
        # 测试基本配置
        print(f"✅ 类别数量: {len(CATEGORIES)}")
        print(f"✅ 详细关键词库类别数: {len(CATEGORY_KEYWORDS)}")
        print(f"✅ 核心关键词库类别数: {len(CORE_KEYWORDS)}")
        print(f"✅ 中文类别数: {len(CHINESE_CATEGORIES)}")
        
        # 测试工具函数
        assert get_category_display_name("ai_ml", "zh") == "人工智能"
        assert get_category_display_name("ai_ml", "en") == "Artificial Intelligence/Machine Learning"
        print("✅ 类别显示名称函数正常")
        
        # 检查关键词数量
        for category in CATEGORIES.keys():
            detailed_count = len(get_category_keywords(category, detailed=True))
            core_count = len(get_category_keywords(category, detailed=False))
            print(f"   {category}: 详细关键词 {detailed_count}, 核心关键词 {core_count}")
        
        print("✅ category_config.py 测试通过\n")
        return True
        
    except Exception as e:
        print(f"❌ category_config.py 测试失败: {e}")
        print(traceback.format_exc())
        return False

def test_gemini_classifier():
    """测试Gemini分类器"""
    print("🧪 测试 gemini_classifier.py...")
    
    try:
        from models.gemini_classifier import GeminiNewsClassifier
        
        # 创建分类器实例（跳过API连接测试）
        print("⏳ 初始化Gemini分类器...")
        
        # 临时禁用API连接测试
        import models.gemini_classifier as gc
        original_test_method = gc.GeminiNewsClassifier._test_api_connection
        gc.GeminiNewsClassifier._test_api_connection = lambda self: print("⏭️ 跳过API连接测试")
        
        classifier = GeminiNewsClassifier()
        
        # 恢复原方法
        gc.GeminiNewsClassifier._test_api_connection = original_test_method
        
        # 测试配置是否正确加载
        assert len(classifier.categories) == 8
        assert len(classifier.category_keywords) == 8
        print("✅ 配置加载正确")
        
        # 测试缓存key生成
        key1 = classifier._generate_cache_key("Test Title", "Test Summary")
        key2 = classifier._generate_cache_key("Test Title", "Test Summary")
        key3 = classifier._generate_cache_key("Different Title", "Test Summary")
        
        assert key1 == key2
        assert key1 != key3
        print("✅ 缓存key生成正常")
        
        # 测试类别验证
        assert classifier._validate_category("ai_ml") == "ai_ml"
        assert classifier._validate_category("AI_ML") == "ai_ml"
        assert classifier._validate_category("artificial intelligence") == "ai_ml"
        assert classifier._validate_category("unknown_category") == "programming"
        print("✅ 类别验证功能正常")
        
        # 测试回退分类
        result = classifier._fallback_keyword_classification(
            "OpenAI releases new GPT model", 
            "Advanced AI language model with improved capabilities"
        )
        assert result == "ai_ml"
        print("✅ 关键词回退分类正常")
        
        # 测试统计功能
        stats = classifier.get_statistics()
        assert "total_classifications" in stats
        assert "cache_hit_rate" in stats
        print("✅ 统计功能正常")
        
        print("✅ gemini_classifier.py 测试通过\n")
        return True
        
    except Exception as e:
        print(f"❌ gemini_classifier.py 测试失败: {e}")
        print(traceback.format_exc())
        return False

def test_data_adapter():
    """测试数据适配器"""
    print("🧪 测试 data_adapter.py...")
    
    try:
        from models.data_adapter import DataAdapter
        
        print("⏳ 初始化数据适配器...")
        
        # 临时禁用API连接测试
        import models.data_adapter as da
        original_test_method = da.DataAdapter._test_events_connection
        da.DataAdapter._test_events_connection = lambda self: True
        
        adapter = DataAdapter()
        
        # 恢复原方法
        da.DataAdapter._test_events_connection = original_test_method
        
        # 测试配置是否正确加载
        assert len(adapter.categories) == 8
        assert len(adapter.category_keywords) == 8
        print("✅ 配置加载正确")
        
        # 测试关键词分类
        result = adapter._classify_with_keywords(
            "Python developer creates new web framework",
            "A new Python web framework for building APIs"
        )
        assert result == "programming"
        print("✅ 关键词分类正常")
        
        # 测试重要性评分计算
        score1 = adapter._calculate_importance_score(0)
        score2 = adapter._calculate_importance_score(50)
        score3 = adapter._calculate_importance_score(100)
        
        assert 0.3 <= score1 <= 1.0
        assert 0.3 <= score2 <= 1.0
        assert 0.3 <= score3 <= 1.0
        assert score1 < score2 < score3
        print("✅ 重要性评分计算正常")
        
        # 测试内容构建
        articles = [
            {"title": "Article 1", "feed": "Feed A"},
            {"title": "Article 2", "feed": "Feed B"}
        ]
        content = adapter._build_content_from_articles(articles)
        assert "Article 1 (Feed A)" in content
        assert "Article 2 (Feed B)" in content
        print("✅ 内容构建功能正常")
        
        # 测试去重功能
        news_list = [
            {"title": "Same Title", "id": "1"},
            {"title": "Same Title", "id": "2"},
            {"title": "Different Title", "id": "3"}
        ]
        unique_news = adapter._deduplicate_news(news_list)
        assert len(unique_news) == 2
        print("✅ 去重功能正常")
        
        # 测试Mock数据
        mock_data = adapter.get_mock_data()
        assert len(mock_data) == 5
        assert all("title" in item for item in mock_data)
        assert all("category" in item for item in mock_data)
        print("✅ Mock数据正常")
        
        print("✅ data_adapter.py 测试通过\n")
        return True
        
    except Exception as e:
        print(f"❌ data_adapter.py 测试失败: {e}")
        print(traceback.format_exc())
        return False

def test_integration():
    """集成测试"""
    print("🧪 集成测试...")
    
    try:
        from models.data_adapter import DataAdapter
        
        # 使用Mock模式测试
        import models.data_adapter as da
        original_test_method = da.DataAdapter._test_events_connection
        da.DataAdapter._test_events_connection = lambda self: False  # 强制使用Mock数据
        
        adapter = DataAdapter()
        
        # 恢复原方法
        da.DataAdapter._test_events_connection = original_test_method
        
        # 测试获取新闻数据（使用Mock数据）
        print("⏳ 测试获取新闻数据...")
        news_data = adapter.get_news_data()
        assert len(news_data) > 0
        print(f"✅ 获取到 {len(news_data)} 条新闻")
        
        # 测试按类别获取新闻
        ai_news = adapter.get_news_by_category("ai_ml", limit=3)
        print(f"✅ AI类别新闻: {len(ai_news)} 条")
        
        # 测试高重要性新闻
        important_news = adapter.get_high_importance_news(min_importance=70, limit=5)
        print(f"✅ 高重要性新闻: {len(important_news)} 条")
        
        # 测试统计功能
        stats = adapter.get_news_statistics()
        assert "total_news" in stats
        assert "category_distribution" in stats
        assert "api_status" in stats
        print("✅ 统计功能正常")
        print(f"   总新闻数: {stats['total_news']}")
        print(f"   API状态: {stats['api_status']}")
        print(f"   Gemini状态: {stats['gemini_status']}")
        
        # 显示类别分布
        if "category_distribution" in stats:
            print("   类别分布:")
            for category, count in stats["category_distribution"].items():
                from models.category_config import get_category_display_name
                display_name = get_category_display_name(category, "zh")
                print(f"     {display_name}: {count} 条")
        
        print("✅ 集成测试通过\n")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        print(traceback.format_exc())
        return False

def test_specific_classifications():
    """测试具体分类案例"""
    print("🧪 测试具体分类案例...")
    
    test_cases = [
        {
            "title": "OpenAI Releases GPT-5 with Advanced Reasoning",
            "summary": "New language model shows significant improvements in AI capabilities",
            "expected": "ai_ml"
        },
        {
            "title": "GitHub Copilot Gets New Code Review Features", 
            "summary": "Microsoft enhances AI-powered coding assistant with review capabilities",
            "expected": "programming"
        },
        {
            "title": "Bitcoin Reaches New All-Time High of $100K",
            "summary": "Cryptocurrency market sees massive gains as institutional adoption grows",
            "expected": "web3_crypto"
        },
        {
            "title": "Y Combinator Demo Day Showcases 200 Startups",
            "summary": "Latest batch includes AI, biotech, and fintech companies seeking funding",
            "expected": "startup_venture"
        },
        {
            "title": "Apple M4 Chip Delivers 40% Performance Boost",
            "summary": "New silicon architecture improves both CPU and GPU performance significantly",
            "expected": "hardware_chips"
        },
        {
            "title": "iPhone 16 Features Revolutionary Camera System",
            "summary": "Apple's latest smartphone includes AI-powered photography enhancements",
            "expected": "consumer_tech"
        },
        {
            "title": "Microsoft Teams Integrates with Salesforce CRM",
            "summary": "Enterprise collaboration platform adds new business intelligence features",
            "expected": "enterprise_saas"
        },
        {
            "title": "TikTok Launches New Creator Monetization Program",
            "summary": "Social media platform expands revenue sharing for content creators",
            "expected": "social_media"
        }
    ]
    
    try:
        from models.data_adapter import DataAdapter
        
        # 使用Mock模式
        import models.data_adapter as da
        original_test_method = da.DataAdapter._test_events_connection
        da.DataAdapter._test_events_connection = lambda self: False
        
        adapter = DataAdapter()
        
        # 恢复原方法
        da.DataAdapter._test_events_connection = original_test_method
        
        correct_predictions = 0
        total_cases = len(test_cases)
        
        for i, case in enumerate(test_cases, 1):
            result = adapter._classify_with_keywords(case["title"], case["summary"])
            is_correct = result == case["expected"]
            
            status = "✅" if is_correct else "❌"
            print(f"   案例 {i}: {status} '{case['title'][:40]}...'")
            print(f"        预期: {case['expected']}, 实际: {result}")
            
            if is_correct:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_cases * 100
        print(f"\n✅ 分类准确率: {accuracy:.1f}% ({correct_predictions}/{total_cases})")
        
        if accuracy >= 75:
            print("✅ 分类性能良好")
            return True
        else:
            print("⚠️ 分类性能需要改进")
            return False
            
    except Exception as e:
        print(f"❌ 分类案例测试失败: {e}")
        print(traceback.format_exc())
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试新闻分类系统...\n")
    print(f"📁 项目根目录: {project_root}")
    print(f"📁 当前工作目录: {os.getcwd()}\n")
    
    # 测试结果
    results = []
    
    # 运行所有测试
    tests = [
        ("配置文件", test_category_config),
        ("Gemini分类器", test_gemini_classifier), 
        ("数据适配器", test_data_adapter),
        ("集成测试", test_integration),
        ("分类案例", test_specific_classifications)
    ]
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # 总结结果
    print(f"{'='*50}")
    print("📊 测试结果总结:")
    print(f"{'='*50}")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {passed} 个测试通过, {failed} 个测试失败")
    
    if failed == 0:
        print("🎉 所有测试都通过了！系统可以正常使用。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查错误信息并修复问题。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)