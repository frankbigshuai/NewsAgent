# user_profile.py - TechSum 用户画像管理系统 (数据库版本)
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json
import uuid

# 导入数据库
from .database import db

@dataclass
class UserProfile:
    """用户画像数据结构"""
    user_id: str
    created_at: str
    updated_at: str
    
    # 基础信息（来自问卷）
    basic_info: Dict[str, Any]
    
    # 兴趣权重（问卷初始化 + 行为学习动态调整）
    interest_weights: Dict[str, float]
    
    # 行为特征（从行为数据推断）
    behavior_profile: Dict[str, Any]
    
    # 个性化参数
    personalization: Dict[str, Any]
    
    # 原始问卷数据（保留）
    survey_data: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """从字典创建实例"""
        return cls(**data)
    
    def save_to_db(self) -> bool:
        """保存到数据库"""
        return db.save_user_profile(self.to_dict())

class UserProfileManager:
    """
    用户画像管理系统 (数据库版本)
    🎯 负责：问卷 → 画像创建，行为 → 画像更新，画像分析
    """
    
    def __init__(self, survey_system=None, behavior_system=None):
        from .interest_survey import survey_instance
        
        # 🔗 集成其他系统
        self.survey_system = survey_system or survey_instance
        self.behavior_system = behavior_system
        
        # 💾 用户画像缓存（从数据库加载）
        self.user_profiles: Dict[str, UserProfile] = {}
        
        # 📊 系统统计
        self.stats = {
            "total_profiles": 0,
            "survey_created": 0,
            "behavior_updated": 0,
            "last_cleanup": datetime.now(),
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # 🔄 从数据库加载现有画像
        self._load_profiles_from_db()
        
        print("✅ 用户画像管理系统初始化完成 (数据库模式)")
    
    def _load_profiles_from_db(self):
        """从数据库加载所有用户画像"""
        try:
            profile_dicts = db.load_all_user_profiles()
            
            for user_id, profile_dict in profile_dicts.items():
                profile = UserProfile.from_dict(profile_dict)
                self.user_profiles[user_id] = profile
            
            self.stats["total_profiles"] = len(self.user_profiles)
            print(f"✅ 从数据库加载了 {len(self.user_profiles)} 个用户画像")
            
        except Exception as e:
            print(f"❌ 从数据库加载用户画像失败: {e}")
    
    def create_profile_from_survey(self, user_id: str, survey_answers: Dict[str, Any]) -> UserProfile:
        """
        📋 从问卷答案创建用户画像 (保存到数据库)
        """
        try:
            # 1. 验证问卷答案
            validation = self.survey_system.validate_answers(survey_answers)
            if not validation["valid"]:
                raise ValueError(f"问卷答案无效: {validation['errors']}")
            
            # 2. 转换为画像数据
            profile_data = self.survey_system.convert_answers_to_profile(survey_answers)
            
            # 3. 创建用户画像对象
            current_time = datetime.now().isoformat()
            
            user_profile = UserProfile(
                user_id=user_id,
                created_at=current_time,
                updated_at=current_time,
                basic_info=profile_data["basic_info"],
                interest_weights=profile_data["interest_weights"],
                behavior_profile=profile_data.get("behavior_profile", {
                    "reading_depth": "medium",
                    "engagement_level": "medium", 
                    "exploration_tendency": "balanced",
                    "activity_pattern": "regular"
                }),
                personalization=profile_data["personalization"],
                survey_data=survey_answers
            )
            
            # 4. 保存到数据库
            if user_profile.save_to_db():
                # 5. 更新缓存
                self.user_profiles[user_id] = user_profile
                
                # 6. 更新统计
                self.stats["total_profiles"] += 1
                self.stats["survey_created"] += 1
                
                print(f"✅ 用户 {user_id} 画像创建成功并保存到数据库")
                return user_profile
            else:
                raise Exception("数据库保存失败")
            
        except Exception as e:
            print(f"❌ 用户 {user_id} 画像创建失败: {e}")
            raise
    
    def update_profile_from_behavior(self, user_id: str, behavior_data: Dict[str, Any]) -> UserProfile:
        """
        🔄 根据行为数据更新用户画像 (保存到数据库)
        """
        # 1. 获取现有画像
        profile = self.get_profile(user_id)
        if not profile:
            # 如果没有画像，创建默认画像
            profile = self._create_default_profile(user_id)
        
        try:
            # 2. 如果有行为学习系统，获取更新后的权重
            if self.behavior_system:
                # 从行为系统获取学习后的权重
                learned_weights = self.behavior_system.get_user_preferences(user_id)
                if learned_weights:
                    profile.interest_weights = learned_weights
            
            # 3. 更新行为特征
            self._update_behavior_characteristics(profile, behavior_data)
            
            # 4. 更新个性化参数
            self._update_personalization_params(profile, behavior_data)
            
            # 5. 更新时间戳
            profile.updated_at = datetime.now().isoformat()
            
            # 6. 保存到数据库
            if profile.save_to_db():
                # 7. 更新缓存
                self.user_profiles[user_id] = profile
                
                # 8. 更新统计
                self.stats["behavior_updated"] += 1
                
                print(f"✅ 用户 {user_id} 画像更新成功并保存到数据库")
                return profile
            else:
                raise Exception("数据库保存失败")
            
        except Exception as e:
            print(f"❌ 用户 {user_id} 画像更新失败: {e}")
            raise
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        📊 获取用户画像 (优先从缓存，缓存未命中从数据库加载)
        """
        # 1. 优先从缓存获取
        if user_id in self.user_profiles:
            self.stats["cache_hits"] += 1
            return self.user_profiles[user_id]
        
        # 2. 缓存未命中，从数据库加载
        self.stats["cache_misses"] += 1
        profile_dict = db.load_user_profile(user_id)
        
        if profile_dict:
            profile = UserProfile.from_dict(profile_dict)
            # 加载到缓存
            self.user_profiles[user_id] = profile
            print(f"💾 从数据库加载用户画像: {user_id}")
            return profile
        
        return None
    
    def get_profile_for_recommendations(self, user_id: str) -> Dict[str, Any]:
        """
        🎯 获取用于推荐的画像数据
        """
        profile = self.get_profile(user_id)
        if not profile:
            return self._get_default_recommendation_profile()
        
        # 提取推荐所需的关键信息
        recommendation_profile = {
            "user_id": user_id,
            "interest_weights": profile.interest_weights,
            "primary_interests": self._get_primary_interests(profile),
            "reading_preference": profile.basic_info.get("reading_preference", "summary"),
            "professional_background": profile.basic_info.get("professional_background", "unknown"),
            "confidence_score": profile.personalization.get("confidence_score", 0.3),
            "exploration_level": profile.behavior_profile.get("exploration_tendency", "balanced")
        }
        
        return recommendation_profile
    
    def analyze_profile_evolution(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        📈 分析用户画像演变
        """
        profile = self.get_profile(user_id)
        if not profile:
            return {"error": "用户画像不存在"}
        
        # 简化版分析（生产环境需要历史数据）
        analysis = {
            "user_id": user_id,
            "profile_age_days": self._calculate_profile_age(profile),
            "current_interests": self._get_primary_interests(profile),
            "interest_distribution": profile.interest_weights,
            "engagement_evolution": self._analyze_engagement_trend(profile),
            "stability_score": self._calculate_interest_stability(profile),
            "recommendation_effectiveness": self._estimate_recommendation_quality(profile)
        }
        
        return analysis
    
    def get_all_profiles_summary(self) -> Dict[str, Any]:
        """
        📊 获取所有用户画像统计摘要 (数据库版本)
        """
        # 获取数据库统计
        db_stats = db.get_database_stats()
        
        if db_stats.get("total_users", 0) == 0:
            return {"total_users": 0, "message": "暂无用户画像"}
        
        # 统计各专业背景分布
        background_distribution = {}
        reading_preference_distribution = {}
        top_interests = {}
        
        for profile in self.user_profiles.values():
            # 专业背景统计
            bg = profile.basic_info.get("professional_background", "unknown")
            background_distribution[bg] = background_distribution.get(bg, 0) + 1
            
            # 阅读偏好统计
            rp = profile.basic_info.get("reading_preference", "unknown")
            reading_preference_distribution[rp] = reading_preference_distribution.get(rp, 0) + 1
            
            # 兴趣权重统计
            for interest, weight in profile.interest_weights.items():
                if interest not in top_interests:
                    top_interests[interest] = []
                top_interests[interest].append(weight)
        
        # 计算平均兴趣权重
        avg_interests = {}
        for interest, weights in top_interests.items():
            avg_interests[interest] = sum(weights) / len(weights)
        
        # 排序获取最受欢迎的兴趣
        sorted_interests = sorted(avg_interests.items(), key=lambda x: x[1], reverse=True)
        
        summary = {
            "total_users": db_stats.get("total_users", 0),
            "creation_stats": {
                "survey_created": self.stats["survey_created"],
                "behavior_updated": self.stats["behavior_updated"]
            },
            "demographics": {
                "professional_backgrounds": background_distribution,
                "reading_preferences": reading_preference_distribution
            },
            "popular_interests": sorted_interests[:5],
            "average_confidence": sum(p.personalization.get("confidence_score", 0) for p in self.user_profiles.values()) / len(self.user_profiles) if self.user_profiles else 0,
            "database_stats": db_stats,
            "cache_performance": {
                "cache_hits": self.stats["cache_hits"],
                "cache_misses": self.stats["cache_misses"],
                "hit_rate": f"{self.stats['cache_hits'] / max(self.stats['cache_hits'] + self.stats['cache_misses'], 1) * 100:.1f}%"
            }
        }
        
        return summary
    
    # ===========================================
    # 🔧 数据库特定方法
    # ===========================================
    
    def sync_cache_to_db(self) -> int:
        """将缓存中的所有画像同步到数据库"""
        synced_count = 0
        for profile in self.user_profiles.values():
            if profile.save_to_db():
                synced_count += 1
        
        print(f"✅ 同步了 {synced_count} 个用户画像到数据库")
        return synced_count
    
    def clear_cache(self):
        """清空缓存"""
        self.user_profiles.clear()
        self.stats["cache_hits"] = 0
        self.stats["cache_misses"] = 0
        print("✅ 用户画像缓存已清空")
    
    def reload_from_db(self):
        """从数据库重新加载所有画像"""
        self.clear_cache()
        self._load_profiles_from_db()
    
    # ===========================================
    # 🔧 私有辅助方法 (保持原有逻辑)
    # ===========================================
    
    def _create_default_profile(self, user_id: str) -> UserProfile:
        """创建默认用户画像（行为优先场景）"""
        current_time = datetime.now().isoformat()
        
        default_profile = UserProfile(
            user_id=user_id,
            created_at=current_time,
            updated_at=current_time,
            basic_info={
                "professional_background": "unknown",
                "reading_preference": "summary",
                "usage_scenarios": [],
                "onboarding_completed": False
            },
            interest_weights={
                "ai_ml": 0.125,
                "programming": 0.125,
                "web3_crypto": 0.125,
                "startup_venture": 0.125,
                "hardware_chips": 0.125,
                "consumer_tech": 0.125,
                "enterprise_saas": 0.125,
                "social_media": 0.125
            },
            behavior_profile={
                "reading_depth": "medium",
                "engagement_level": "medium",
                "exploration_tendency": "balanced",
                "activity_pattern": "irregular"
            },
            personalization={
                "confidence_score": 0.1,  # 默认画像置信度较低
                "total_interactions": 0,
                "last_active": current_time,
                "favorite_categories": [],
                "preferred_content_type": "summary",
                "onboarding_completed": False
            },
            survey_data={}
        )
        
        # 保存到数据库
        if default_profile.save_to_db():
            self.user_profiles[user_id] = default_profile
            self.stats["total_profiles"] += 1
            print(f"✅ 用户 {user_id} 默认画像创建成功并保存到数据库")
        
        return default_profile
    
    def _update_behavior_characteristics(self, profile: UserProfile, behavior_data: Dict[str, Any]):
        """更新行为特征"""
        action = behavior_data.get("action", "")
        duration = behavior_data.get("reading_duration", 0)
        engagement_score = behavior_data.get("engagement_score", 0)
        
        # 更新阅读深度
        if action in ["deep_read"] or duration > 120:
            profile.behavior_profile["reading_depth"] = "deep"
        elif action in ["skip"] or duration < 15:
            profile.behavior_profile["reading_depth"] = "light"
        else:
            profile.behavior_profile["reading_depth"] = "medium"
        
        # 更新参与度
        if engagement_score > 0.15:
            profile.behavior_profile["engagement_level"] = "high"
        elif engagement_score < 0.05:
            profile.behavior_profile["engagement_level"] = "low"
        else:
            profile.behavior_profile["engagement_level"] = "medium"
    
    def _update_personalization_params(self, profile: UserProfile, behavior_data: Dict[str, Any]):
        """更新个性化参数"""
        # 增加交互次数
        profile.personalization["total_interactions"] += 1
        
        # 更新最后活跃时间
        profile.personalization["last_active"] = datetime.now().isoformat()
        
        # 根据交互次数更新置信度
        interactions = profile.personalization["total_interactions"]
        if interactions > 50:
            profile.personalization["confidence_score"] = min(1.0, 0.8 + interactions * 0.002)
        elif interactions > 20:
            profile.personalization["confidence_score"] = min(0.8, 0.5 + interactions * 0.015)
        else:
            profile.personalization["confidence_score"] = min(0.5, 0.1 + interactions * 0.02)
        
        # 更新喜爱类别
        category = behavior_data.get("news_category")
        if category and behavior_data.get("action") in ["deep_read", "share", "bookmark"]:
            fav_categories = profile.personalization.get("favorite_categories", [])
            if category not in fav_categories:
                fav_categories.append(category)
                profile.personalization["favorite_categories"] = fav_categories[:3]  # 最多保留3个
    
    def _get_primary_interests(self, profile: UserProfile) -> List[str]:
        """获取用户主要兴趣"""
        sorted_interests = sorted(
            profile.interest_weights.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return [interest for interest, weight in sorted_interests[:3] if weight > 0.1]
    
    def _get_default_recommendation_profile(self) -> Dict[str, Any]:
        """获取默认推荐画像"""
        return {
            "user_id": "anonymous",
            "interest_weights": {
                "ai_ml": 0.125,
                "programming": 0.125,
                "web3_crypto": 0.125,
                "startup_venture": 0.125,
                "hardware_chips": 0.125,
                "consumer_tech": 0.125,
                "enterprise_saas": 0.125,
                "social_media": 0.125
            },
            "primary_interests": ["ai_ml", "programming", "startup_venture"],
            "reading_preference": "summary",
            "professional_background": "unknown",
            "confidence_score": 0.1,
            "exploration_level": "balanced"
        }
    
    def _calculate_profile_age(self, profile: UserProfile) -> int:
        """计算画像年龄（天数）"""
        try:
            created = datetime.fromisoformat(profile.created_at)
            return (datetime.now() - created).days
        except:
            return 0
    
    def _analyze_engagement_trend(self, profile: UserProfile) -> str:
        """分析参与度趋势（简化版）"""
        engagement = profile.behavior_profile.get("engagement_level", "medium")
        interactions = profile.personalization.get("total_interactions", 0)
        
        if engagement == "high" and interactions > 30:
            return "持续高参与"
        elif engagement == "high":
            return "初期高参与"
        elif engagement == "low" and interactions > 20:
            return "参与度下降"
        else:
            return "稳定参与"
    
    def _calculate_interest_stability(self, profile: UserProfile) -> float:
        """计算兴趣稳定性得分"""
        weights = list(profile.interest_weights.values())
        max_weight = max(weights)
        min_weight = min(weights)
        
        # 权重差异越大，兴趣越专一（稳定性越高）
        stability = (max_weight - min_weight) / max_weight if max_weight > 0 else 0
        return round(stability, 3)
    
    def _estimate_recommendation_quality(self, profile: UserProfile) -> str:
        """估算推荐质量"""
        confidence = profile.personalization.get("confidence_score", 0)
        stability = self._calculate_interest_stability(profile)
        
        if confidence > 0.7 and stability > 0.3:
            return "高质量"
        elif confidence > 0.4 or stability > 0.2:
            return "中等质量"
        else:
            return "需要改进"