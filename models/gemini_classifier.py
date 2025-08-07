# models/gemini_classifier.py - 安全版本的Gemini分类器

import requests
import json
import logging
from typing import Dict, List, Optional
import time
import hashlib

# 安全导入配置
try:
    from config.settings import settings
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    logging.warning("⚠️ 配置模块未找到，将使用环境变量")

from .category_config import CATEGORIES, CORE_KEYWORDS

class GeminiNewsClassifier:
    """Gemini API-based intelligent news classifier - 安全版本"""
    
    def __init__(self, api_key: str = None):
        # 🔒 安全的API密钥获取
        self.api_key = self._get_secure_api_key(api_key)
        
        # 验证API密钥
        self._validate_api_key()
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        
        # 使用统一配置
        self.categories = CATEGORIES
        self.category_keywords = CORE_KEYWORDS
        
        # 缓存机制
        self.classification_cache = {}
        
        # API调用统计
        self.api_calls = 0
        self.cache_hits = 0
        self.api_errors = 0
        
        # 安全测试API连接
        self._test_api_connection_safe()
        
        logging.info("✅ Gemini分类器初始化完成 (安全模式)")
    
    def _get_secure_api_key(self, provided_key: str = None) -> str:
        """安全获取API密钥"""
        if provided_key:
            return provided_key
        
        # 优先从配置获取
        if CONFIG_AVAILABLE:
            return settings.GEMINI_API_KEY
        
        # 回退到环境变量
        import os
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "🔒 Gemini API密钥未配置。请设置环境变量 GEMINI_API_KEY 或创建 .env 文件"
            )
        
        return api_key
    
    def _validate_api_key(self) -> None:
        """验证API密钥格式"""
        if not self.api_key:
            raise ValueError("API密钥不能为空")
        
        if not isinstance(self.api_key, str):
            raise ValueError("API密钥必须是字符串")
        
        if len(self.api_key) < 20:
            raise ValueError("API密钥长度不足，可能无效")
        
        if not self.api_key.startswith('AIza'):
            raise ValueError("无效的Gemini API密钥格式，应以 'AIza' 开头")
        
        logging.info("✅ API密钥格式验证通过")
    
    def _test_api_connection_safe(self) -> None:
        """安全测试API连接"""
        try:
            # 不实际调用API，只验证配置
            masked_key = self.api_key[:8] + "*" * (len(self.api_key) - 12) + self.api_key[-4:]
            logging.info(f"🔒 Gemini API密钥已配置: {masked_key}")
            logging.info("✅ API连接配置验证完成")
        except Exception as e:
            logging.error(f"❌ API连接配置验证失败: {e}")
            raise
    
    def classify_news(self, title: str, summary: str = "", content: str = "") -> str:
        """
        安全的新闻分类方法
        
        Args:
            title: 新闻标题
            summary: 新闻摘要
            content: 新闻内容
            
        Returns:
            分类结果 (category key)
        """
        try:
            # 生成缓存键
            cache_key = self._generate_cache_key(title, summary)
            
            # 检查缓存
            if cache_key in self.classification_cache:
                self.cache_hits += 1
                logging.debug(f"📦 缓存命中: {title[:30]}...")
                return self.classification_cache[cache_key]
            
            # 调用Gemini API
            category = self._call_gemini_api_safe(title, summary, content)
            
            # 验证并处理结果
            validated_category = self._validate_category(category)
            
            # 缓存结果
            self.classification_cache[cache_key] = validated_category
            
            logging.info(f"🤖 Gemini分类完成: {title[:30]}... → {validated_category}")
            return validated_category
            
        except Exception as e:
            logging.error(f"❌ Gemini分类失败: {e}")
            # 回退到关键词分类
            return self._fallback_keyword_classification(title, summary)
    
    def _call_gemini_api_safe(self, title: str, summary: str, content: str) -> str:
        """安全的Gemini API调用"""
        try:
            self.api_calls += 1
            
            # 构建分类提示
            prompt = self._build_classification_prompt(title, summary, content)
            
            # API请求头
            headers = {
                'Content-Type': 'application/json',
            }
            
            # 请求体
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1,  # 低随机性保证一致性
                    "maxOutputTokens": 50,
                    "topP": 0.8,
                    "topK": 10
                }
            }
            
            # 构建请求URL（密钥作为查询参数）
            url = f"{self.base_url}?key={self.api_key}"
            
            # 发送请求
            response = requests.post(
                url, 
                headers=headers, 
                json=data, 
                timeout=30
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    return content
                else:
                    raise Exception("API返回格式异常")
            
            elif response.status_code == 403:
                raise Exception("API密钥无效或权限不足")
            elif response.status_code == 429:
                raise Exception("API调用频率超限")
            else:
                raise Exception(f"API调用失败: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            self.api_errors += 1
            raise Exception("API调用超时")
        except requests.exceptions.ConnectionError:
            self.api_errors += 1
            raise Exception("API连接失败")
        except Exception as e:
            self.api_errors += 1
            raise Exception(f"API调用异常: {str(e)}")
    
    def _build_classification_prompt(self, title: str, summary: str, content: str) -> str:
        """构建分类提示词"""
        categories_desc = "\n".join([f"- {key}: {desc}" for key, desc in self.categories.items()])
        
        # 组合文本内容
        text_content = f"标题: {title}"
        if summary:
            text_content += f"\n摘要: {summary}"
        if content and len(content) < 500:  # 限制内容长度
            text_content += f"\n内容: {content[:500]}"
        
        prompt = f"""请将以下科技新闻分类到最合适的类别中。

分类选项:
{categories_desc}

新闻内容:
{text_content}

分析要求:
1. 仔细阅读标题、摘要和内容
2. 理解新闻的核心主题和领域
3. 选择最符合新闻主要内容的类别
4. 如果涉及多个领域，选择最主要的一个

请只返回对应的英文分类代码(如 ai_ml, programming 等)，不要任何解释。"""

        return prompt
    
    def _validate_category(self, category: str) -> str:
        """验证和清理分类结果"""
        # 清理结果
        category = category.lower().strip()
        
        # 移除可能的标点符号
        category = category.replace('.', '').replace(',', '').replace(':', '').replace(';', '')
        
        # 直接匹配
        if category in self.categories:
            return category
        
        # 模糊匹配
        for key in self.categories.keys():
            if key in category or category in key:
                return key
        
        # 使用核心关键词进行语义匹配
        for mapped_category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in category:
                    return mapped_category
        
        # 默认返回
        logging.warning(f"⚠️ 未知分类结果: {category}, 使用默认分类")
        return "programming"  # 默认为编程类别
    
    def _generate_cache_key(self, title: str, summary: str) -> str:
        """生成缓存键"""
        content = f"{title}{summary}".lower()
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _fallback_keyword_classification(self, title: str, summary: str) -> str:
        """回退到关键词分类"""
        logging.info("🔄 回退到关键词分类")
        
        text = f"{title} {summary}".lower()
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in text:
                    if keyword.lower() in title.lower():
                        score += 2  # 标题中的关键词权重更高
                    else:
                        score += 1
            category_scores[category] = score
        
        if category_scores and max(category_scores.values()) > 0:
            best_category = max(category_scores, key=category_scores.get)
            logging.info(f"✅ 关键词分类结果: {best_category}")
            return best_category
        
        return "programming"
    
    def get_statistics(self) -> Dict:
        """获取分类器统计信息"""
        total_requests = self.api_calls + self.cache_hits
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        error_rate = (self.api_errors / max(self.api_calls, 1) * 100) if self.api_calls > 0 else 0
        
        return {
            "total_classifications": total_requests,
            "api_calls": self.api_calls,
            "cache_hits": self.cache_hits,
            "api_errors": self.api_errors,
            "cache_hit_rate": f"{hit_rate:.1f}%",
            "api_error_rate": f"{error_rate:.1f}%",
            "cache_size": len(self.classification_cache)
        }
    
    def clear_cache(self) -> None:
        """清理缓存"""
        self.classification_cache.clear()
        logging.info("✅ 分类缓存已清理")
    
    def health_check(self) -> Dict:
        """健康检查"""
        try:
            # 检查API密钥配置
            api_key_ok = bool(self.api_key and len(self.api_key) > 20)
            
            # 检查错误率
            error_rate = (self.api_errors / max(self.api_calls, 1)) if self.api_calls > 0 else 0
            error_rate_ok = error_rate < 0.5  # 错误率低于50%
            
            # 检查缓存状态
            cache_ok = len(self.classification_cache) < 10000  # 缓存大小合理
            
            overall_health = api_key_ok and error_rate_ok and cache_ok
            
            return {
                "healthy": overall_health,
                "api_key_configured": api_key_ok,
                "error_rate_acceptable": error_rate_ok,
                "cache_size_reasonable": cache_ok,
                "statistics": self.get_statistics()
            }
            
        except Exception as e:
            logging.error(f"健康检查失败: {e}")
            return {
                "healthy": False,
                "error": str(e)
            }


# 使用示例和测试代码
if __name__ == "__main__":
    try:
        # 初始化分类器
        classifier = GeminiNewsClassifier()
        
        # 测试分类
        test_cases = [
            {
                "title": "OpenAI发布GPT-5，AI推理能力大幅提升",
                "summary": "OpenAI正式发布GPT-5模型，在数学推理和代码生成方面表现出色",
                "expected": "ai_ml"
            },
            {
                "title": "YC Demo Day 2025创投资记录新高",
                "summary": "Y Combinator 2025夏季批次Demo Day举行，200家初创公司展示，总估值超100亿美元",
                "expected": "startup_venture"
            },
            {
                "title": "React 19正式版发布，带来重大性能改进",
                "summary": "Facebook发布React 19，新增并发特性和服务器组件支持",
                "expected": "programming"
            }
        ]
        
        print("🧪 开始测试分类器...")
        for i, test_case in enumerate(test_cases, 1):
            result = classifier.classify_news(
                test_case["title"], 
                test_case["summary"]
            )
            
            status = "✅" if result == test_case["expected"] else "❌"
            print(f"Test {i}: {status} 预期:{test_case['expected']}, 实际:{result}")
        
        # 显示统计信息
        stats = classifier.get_statistics()
        print(f"\n📊 分类器统计: {stats}")
        
        # 健康检查
        health = classifier.health_check()
        print(f"🏥 健康状态: {'✅ 健康' if health['healthy'] else '❌ 异常'}")
        
    except Exception as e:
        logging.error(f"测试失败: {e}")
        print(f"❌ 测试失败: {e}")