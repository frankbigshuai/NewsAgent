from typing import List, Dict, Optional
from models.data_adapter import DataAdapter
import math
import time
import hashlib
import json
from datetime import datetime, timedelta

class CachedRecommendationEngine:
    """
    性能优化版推荐引擎 - 带智能缓存系统
    🚀 目标：从1.7秒优化到0.3秒内
    """
    
    def __init__(self):
        self.data_adapter = DataAdapter()
        
        # 🗄️ 缓存系统
        self.news_cache = {}           # 新闻数据缓存
        self.recommendation_cache = {} # 推荐结果缓存  
        self.score_cache = {}          # 个性化分数缓存
        
        # ⏰ 缓存过期时间（秒）
        self.CACHE_SETTINGS = {
            "news_ttl": 30 * 60,        # 新闻缓存30分钟
            "recommendation_ttl": 10 * 60,  # 推荐缓存10分钟
            "score_ttl": 5 * 60,        # 分数缓存5分钟
        }
        
        # 📊 缓存统计
        self.cache_stats = {
            "news_hits": 0,
            "news_misses": 0,
            "recommendation_hits": 0,
            "recommendation_misses": 0,
            "total_requests": 0
        }
        
        # 兴趣类别定义
        self.interest_categories = {
            "ai_ml": ["ChatGPT", "GPT", "Claude", "Gemini", "机器学习", "深度学习", "LLM", "AI Agent", "OpenAI", "Anthropic"],
            "startup_venture": ["YCombinator", "融资", "创业", "独角兽", "IPO", "风投", "VC", "Series A", "Series B", "天使投资"],
            "web3_crypto": ["Bitcoin", "Ethereum", "区块链", "DeFi", "NFT", "加密货币", "Web3", "Solana", "Polygon"],
            "programming": ["Python", "JavaScript", "React", "Vue", "开源", "GitHub", "框架", "TypeScript", "Node.js"],
            "hardware_chips": ["芯片", "半导体", "GPU", "CPU", "NVIDIA", "AMD", "量子计算", "Intel", "Apple Silicon"],
            "consumer_tech": ["iPhone", "特斯拉", "Apple", "小米", "电动汽车", "智能家居", "Android", "Samsung"],
            "enterprise_saas": ["SaaS", "企业服务", "办公软件", "CRM", "云计算", "AWS", "Azure", "Salesforce", "Slack", "Notion"],
            "social_media": ["Twitter", "抖音", "社交媒体", "直播", "短视频", "Instagram", "TikTok", "YouTube", "Facebook", "LinkedIn"]
        }
    
    def _generate_cache_key(self, prefix: str, data: any) -> str:
        """生成缓存键"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        hash_obj = hashlib.md5(data_str.encode())
        return f"{prefix}_{hash_obj.hexdigest()[:12]}"
    
    def _is_cache_valid(self, cache_entry: Dict, ttl: int) -> bool:
        """检查缓存是否有效"""
        if not cache_entry:
            return False
        
        cache_time = cache_entry.get("timestamp", 0)
        current_time = time.time()
        
        return (current_time - cache_time) < ttl
    
    def _set_cache(self, cache_dict: Dict, key: str, value: any) -> None:
        """设置缓存"""
        cache_dict[key] = {
            "data": value,
            "timestamp": time.time()
        }
        
        # 🧹 简单的缓存清理：保持最多100个条目
        if len(cache_dict) > 100:
            # 删除最旧的20个条目
            old_keys = sorted(cache_dict.keys(), 
                            key=lambda k: cache_dict[k]["timestamp"])[:20]
            for old_key in old_keys:
                del cache_dict[old_key]
    
    def get_cached_news_data(self) -> List[Dict]:
        """
        🚀 获取缓存的新闻数据
        """
        cache_key = "news_data_all"
        
        # 检查缓存
        if cache_key in self.news_cache:
            cache_entry = self.news_cache[cache_key]
            if self._is_cache_valid(cache_entry, self.CACHE_SETTINGS["news_ttl"]):
                self.cache_stats["news_hits"] += 1
                print("💾 使用新闻缓存数据")
                return cache_entry["data"]
        
        # 缓存未命中，获取新数据
        self.cache_stats["news_misses"] += 1
        print("🌐 从API获取新闻数据")
        
        news_data = self.data_adapter.get_news_data()
        if not news_data:
            news_data = self.data_adapter.get_mock_data()
        
        # 存入缓存
        self._set_cache(self.news_cache, cache_key, news_data)
        
        return news_data
    
    def get_cached_personalized_scores(self, news_list: List[Dict], 
                                     user_interests: List[str], 
                                     user_weights: Dict[str, float]) -> List[Dict]:
        """
        🚀 获取缓存的个性化分数
        """
        user_profile = {
            "interests": sorted(user_interests),
            "weights": user_weights
        }
        cache_key = self._generate_cache_key("scores", user_profile)
        
        # 检查缓存
        if cache_key in self.score_cache:
            cache_entry = self.score_cache[cache_key]
            if self._is_cache_valid(cache_entry, self.CACHE_SETTINGS["score_ttl"]):
                cached_scores = cache_entry["data"]
                
                # 验证缓存的新闻ID是否与当前新闻匹配
                cached_ids = set(item["id"] for item in cached_scores)
                current_ids = set(news["id"] for news in news_list)
                
                if cached_ids == current_ids:
                    print("💾 使用分数缓存")
                    return cached_scores
        
        # 缓存未命中，计算新分数
        print("🔄 计算个性化分数")
        scored_news = []
        
        for news in news_list:
            score = self.calculate_personalized_score(news, user_interests, user_weights)
            if score > 0.1:
                news_copy = news.copy()
                news_copy["personalized_score"] = round(score, 3)
                scored_news.append(news_copy)
        
        # 存入缓存
        self._set_cache(self.score_cache, cache_key, scored_news)
        
        return scored_news
    
    def recommend_for_user(self, user_id: str, user_interests: List[str], 
                          user_weights: Dict[str, float], limit: int = 10) -> List[Dict]:
        """
        🚀 高性能推荐生成 - 带缓存优化
        """
        start_time = time.time()
        self.cache_stats["total_requests"] += 1
        
        # 🗝️ 生成推荐缓存键
        recommendation_key_data = {
            "interests": sorted(user_interests),
            "weights": user_weights,
            "limit": limit
        }
        rec_cache_key = self._generate_cache_key("rec", recommendation_key_data)
        
        # 📋 检查推荐缓存
        if rec_cache_key in self.recommendation_cache:
            cache_entry = self.recommendation_cache[rec_cache_key]
            if self._is_cache_valid(cache_entry, self.CACHE_SETTINGS["recommendation_ttl"]):
                self.cache_stats["recommendation_hits"] += 1
                elapsed = time.time() - start_time
                print(f"⚡ 缓存命中！推荐生成时间: {elapsed:.3f}秒")
                return cache_entry["data"]
        
        # 缓存未命中，生成新推荐
        self.cache_stats["recommendation_misses"] += 1
        
        # 1️⃣ 获取缓存的新闻数据
        all_news = self.get_cached_news_data()
        
        # 2️⃣ 获取缓存的个性化分数
        scored_news = self.get_cached_personalized_scores(all_news, user_interests, user_weights)
        
        # 3️⃣ 排序
        scored_news.sort(key=lambda x: x["personalized_score"], reverse=True)
        
        # 4️⃣ 应用多样性控制
        diverse_news = self._apply_diversity_control(scored_news, user_interests, limit)
        
        # 📊 输出多样性统计
        if diverse_news:
            category_dist = {}
            for news in diverse_news:
                cat = news.get("category", "unknown")
                category_dist[cat] = category_dist.get(cat, 0) + 1
            
            print(f"🌈 多样性统计: {category_dist}")
            print(f"📊 类别数量: {len(category_dist)}")
        
        # 🗄️ 存入推荐缓存
        self._set_cache(self.recommendation_cache, rec_cache_key, diverse_news)
        
        elapsed = time.time() - start_time
        print(f"🚀 推荐生成完成，耗时: {elapsed:.3f}秒")
        
        return diverse_news
    
    def get_cache_statistics(self) -> Dict:
        """获取缓存统计信息"""
        total_news_requests = self.cache_stats["news_hits"] + self.cache_stats["news_misses"]
        total_rec_requests = self.cache_stats["recommendation_hits"] + self.cache_stats["recommendation_misses"]
        
        news_hit_rate = (self.cache_stats["news_hits"] / total_news_requests * 100) if total_news_requests > 0 else 0
        rec_hit_rate = (self.cache_stats["recommendation_hits"] / total_rec_requests * 100) if total_rec_requests > 0 else 0
        
        return {
            "总请求数": self.cache_stats["total_requests"],
            "新闻缓存": {
                "命中次数": self.cache_stats["news_hits"],
                "未命中次数": self.cache_stats["news_misses"],
                "命中率": f"{news_hit_rate:.1f}%"
            },
            "推荐缓存": {
                "命中次数": self.cache_stats["recommendation_hits"],
                "未命中次数": self.cache_stats["recommendation_misses"],
                "命中率": f"{rec_hit_rate:.1f}%"
            },
            "缓存大小": {
                "新闻缓存": len(self.news_cache),
                "推荐缓存": len(self.recommendation_cache),
                "分数缓存": len(self.score_cache)
            }
        }
    
    def clear_cache(self, cache_type: str = "all") -> None:
        """清理缓存"""
        if cache_type == "all" or cache_type == "news":
            self.news_cache.clear()
            print("🧹 新闻缓存已清理")
        
        if cache_type == "all" or cache_type == "recommendations":
            self.recommendation_cache.clear()
            print("🧹 推荐缓存已清理")
        
        if cache_type == "all" or cache_type == "scores":
            self.score_cache.clear()
            print("🧹 分数缓存已清理")
    
    def warm_up_cache(self, sample_users: List[Dict]) -> None:
        """
        🔥 缓存预热 - 提前为常见用户类型生成推荐
        """
        print("🔥 开始缓存预热...")
        
        # 预热新闻数据缓存
        self.get_cached_news_data()
        
        # 预热常见用户类型的推荐
        for user in sample_users:
            self.recommend_for_user(
                user.get("user_id", "warmup"),
                user.get("interests", []),
                user.get("weights", {}),
                limit=10
            )
        
        print("🔥 缓存预热完成")
    
    # 原有的核心算法方法保持不变
    def calculate_personalized_score(self, news: Dict, user_interests: List[str], user_weights: Dict[str, float]) -> float:
        """核心算法：计算个性化相关性分数"""
        if not user_interests or not user_weights:
            return 0.0
        
        score = 0.0
        
        # 1. 类别匹配分数（40%权重）
        category_score = self._calculate_category_score(news, user_interests, user_weights)
        score += category_score * 0.4
        
        # 2. 关键词匹配分数（30%权重）
        keyword_score = self._calculate_keyword_score(news, user_interests)
        score += keyword_score * 0.3
        
        # 3. 新闻热度分数（20%权重）
        hot_score = news.get("hot_score", 0.5)
        score += hot_score * 0.2
        
        # 4. 时效性分数（10%权重）
        time_score = self._calculate_time_score(news.get("publish_time", ""))
        score += time_score * 0.1
        
        return score
    
    def _calculate_category_score(self, news: Dict, user_interests: List[str], user_weights: Dict[str, float]) -> float:
        """计算类别匹配分数"""
        news_category = news.get("category", "")
        
        if news_category in user_interests:
            return user_weights.get(news_category, 0) * 5.0
        
        related_score = 0.0
        for category in user_interests:
            if self._is_related_category(news_category, category):
                related_score += user_weights.get(category, 0) * 2.0
        
        return related_score
    
    def _calculate_keyword_score(self, news: Dict, user_interests: List[str]) -> float:
        """计算关键词匹配分数"""
        news_text = f"{news.get('title', '')} {news.get('summary', '')}".lower()
        
        user_keywords = []
        for category in user_interests:
            if category in self.interest_categories:
                user_keywords.extend([kw.lower() for kw in self.interest_categories[category]])
        
        if not user_keywords:
            return 0.0
        
        matches = 0
        for keyword in user_keywords:
            if keyword in news_text:
                matches += 1
        
        return min(matches / len(user_keywords), 1.0)
    
    def _calculate_time_score(self, publish_time: str) -> float:
        """计算时效性分数"""
        try:
            if not publish_time:
                return 0.5
            
            pub_time = datetime.fromisoformat(publish_time.replace('Z', ''))
            hours_diff = (datetime.now() - pub_time.replace(tzinfo=None)).total_seconds() / 3600
            
            if hours_diff <= 24:
                return 1.0
            elif hours_diff <= 48:
                return 0.8
            elif hours_diff <= 72:
                return 0.6
            else:
                return 0.4
        except:
            return 0.5
    
    def _is_related_category(self, category1: str, category2: str) -> bool:
        """判断两个类别是否相关"""
        related_categories = {
            "ai_ml": ["programming", "hardware_chips"],
            "programming": ["ai_ml", "hardware_chips"],
            "startup_venture": ["ai_ml", "web3_crypto", "consumer_tech"],
            "web3_crypto": ["startup_venture", "programming"],
            "hardware_chips": ["ai_ml", "programming", "consumer_tech"],
            "consumer_tech": ["ai_ml", "hardware_chips", "startup_venture"]
        }
        
        return category2 in related_categories.get(category1, [])
    
    # 多样性控制方法（从之前的代码复制）
    def _apply_diversity_control(self, scored_news: List[Dict], user_interests: List[str], limit: int) -> List[Dict]:
        """改进的多样性控制算法"""
        if not scored_news or limit <= 0:
            return []
        
        user_interest_slots = int(limit * 0.7)
        related_slots = int(limit * 0.2)
        exploration_slots = limit - user_interest_slots - related_slots
        
        user_interest_news = []
        related_news = []
        exploration_news = []
        
        for news in scored_news:
            category = news.get("category", "general")
            
            if category in user_interests:
                user_interest_news.append(news)
            elif self._is_any_related_category(category, user_interests):
                related_news.append(news)
            else:
                exploration_news.append(news)
        
        diverse_recommendations = []
        
        user_recommendations = self._select_balanced_news(
            user_interest_news, user_interests, user_interest_slots
        )
        diverse_recommendations.extend(user_recommendations)
        
        if related_news and related_slots > 0:
            diverse_recommendations.extend(related_news[:related_slots])
        
        if exploration_news and exploration_slots > 0:
            exploration_news.sort(key=lambda x: x.get("hot_score", 0), reverse=True)
            diverse_recommendations.extend(exploration_news[:exploration_slots])
        
        if len(diverse_recommendations) < limit:
            remaining_slots = limit - len(diverse_recommendations)
            all_remaining = [news for news in scored_news 
                            if news not in diverse_recommendations]
            diverse_recommendations.extend(all_remaining[:remaining_slots])
        
        final_recommendations = self._interleave_recommendations(
            diverse_recommendations, user_interests
        )
        
        return final_recommendations[:limit]
    
    def _select_balanced_news(self, news_list: List[Dict], user_interests: List[str], total_slots: int) -> List[Dict]:
        """在用户兴趣内容中实现类别平衡"""
        if not news_list or not user_interests or total_slots <= 0:
            return []
        
        category_groups = {}
        for news in news_list:
            category = news.get("category", "general")
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(news)
        
        slots_per_category = max(1, total_slots // len(user_interests))
        
        balanced_news = []
        for category in user_interests:
            if category in category_groups:
                category_news = sorted(
                    category_groups[category], 
                    key=lambda x: x.get("personalized_score", 0), 
                    reverse=True
                )
                balanced_news.extend(category_news[:slots_per_category])
        
        if len(balanced_news) < total_slots:
            remaining_slots = total_slots - len(balanced_news)
            all_remaining = [news for news in news_list if news not in balanced_news]
            all_remaining.sort(key=lambda x: x.get("personalized_score", 0), reverse=True)
            balanced_news.extend(all_remaining[:remaining_slots])
        
        return balanced_news
    
    def _is_any_related_category(self, category: str, user_interests: List[str]) -> bool:
        """检查类别是否与用户任何兴趣相关"""
        for user_interest in user_interests:
            if self._is_related_category(category, user_interest):
                return True
        return False
    
    def _interleave_recommendations(self, recommendations: List[Dict], user_interests: List[str]) -> List[Dict]:
        """交错排列推荐内容，避免同类别聚集"""
        if len(recommendations) <= 3:
            return recommendations
        
        category_groups = {}
        for news in recommendations:
            category = news.get("category", "general")
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(news)
        
        if len(category_groups) <= 1:
            return recommendations
        
        interleaved = []
        category_indices = {cat: 0 for cat in category_groups.keys()}
        
        while len(interleaved) < len(recommendations):
            for category in category_groups.keys():
                if category_indices[category] < len(category_groups[category]):
                    interleaved.append(category_groups[category][category_indices[category]])
                    category_indices[category] += 1
                    
                    if len(interleaved) >= len(recommendations):
                        break
        
        return interleaved