# enhanced_behavior_system.py - 完全工作的增强版 (数据库版本)
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import math
import hashlib
from dataclasses import dataclass

# 导入数据库
from .database import db

@dataclass
class BehaviorEvent:
    """行为事件数据类"""
    user_id: str
    action: str
    news_id: str
    news_category: str
    news_title: str = ""
    reading_duration: int = 0
    scroll_percentage: float = 0.0
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class EnhancedBehaviorSystem:
    """
    完全工作的增强版行为学习系统 (数据库版本)
    🎯 基于调试版本的成功逻辑，加上数据库持久化
    """
    
    def __init__(self, recommendation_engine=None, test_mode=False):
        # 🔗 集成推荐引擎
        self.recommendation_engine = recommendation_engine
        self.test_mode = test_mode
        
        # 📊 增强的行为权重映射
        self.behavior_weights = {
            'view': 0.01,
            'click': 0.03,
            'read': 0.05,
            'deep_read': 0.12,
            'share': 0.18,
            'like': 0.08,
            'bookmark': 0.10,
            'comment': 0.06,
            'dislike': -0.12,
            'skip': -0.04,
            'report': -0.20,
            'block_category': -0.25
        }
        
        # 🎛️ 智能学习参数
        self.learning_config = {
            'base_learning_rate': 0.12,
            'adaptive_rate': True,
            'decay_factor': 0.95,
            'max_days': 30,
            'confidence_threshold': 10,
            'exploration_rate': 0.1,
            'min_weight': 0.02,
            'max_weight': 0.45
        }
        
        # 🎯 参与度阈值
        self.engagement_thresholds = {
            'deep_read_duration': 90,
            'skip_duration': 15,
            'high_scroll': 75,
            'low_scroll': 25,
            'quality_reading': 60,
            'bounce_threshold': 5
        }
        
        # 💾 内存缓存（性能优化）
        self.user_behaviors_cache = {}
        self.user_preferences_cache = {}
        self.anomaly_detection = {}
        
        # 📈 统计数据
        self.system_stats = {
            'total_behaviors': 0,
            'total_users': 0,
            'learning_updates': 0,
            'anomalies_detected': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # 🔄 从数据库加载现有数据
        self._load_behaviors_from_db()
        
        print("✅ 行为学习系统初始化完成 (数据库模式)")
    
    def _load_behaviors_from_db(self):
        """从数据库加载用户行为数据"""
        try:
            all_behaviors = db.load_all_user_behaviors()
            
            for user_id, behaviors in all_behaviors.items():
                self.user_behaviors_cache[user_id] = behaviors
                self.system_stats['total_behaviors'] += len(behaviors)
            
            self.system_stats['total_users'] = len(all_behaviors)
            print(f"✅ 从数据库加载了 {len(all_behaviors)} 个用户的行为数据")
            
        except Exception as e:
            print(f"❌ 从数据库加载行为数据失败: {e}")
    
    def track_behavior(self, event: BehaviorEvent) -> Dict:
        """
        🎯 完全工作的行为追踪 - 保存到数据库
        """
        print(f"🔍 调试: 接收到行为事件")
        print(f"   用户ID: {event.user_id}")
        print(f"   行为: {event.action}")
        print(f"   类别: {event.news_category}")
        print(f"   时长: {event.reading_duration}")
        
        try:
            # 🛡️ 轻量级异常检测
            if self._detect_anomaly_light(event):
                self.system_stats['anomalies_detected'] += 1
                return {
                    "success": False,
                    "error": "异常行为检测",
                    "reason": "行为频率过高"
                }
            
            # 📊 生成行为ID
            behavior_id = f"behavior_{abs(hash(f'{event.user_id}{event.timestamp}{event.news_id}'))}"
            
            # 📊 智能行为调整
            enhanced_action = self._smart_action_adjustment(event)
            
            # 📊 计算增强参与度分数
            engagement_score = self._calculate_enhanced_engagement(event, enhanced_action)
            
            # 💾 构建行为数据
            behavior_data = {
                "behavior_id": behavior_id,
                "user_id": event.user_id,
                "action": enhanced_action,
                "original_action": event.action,
                "news_category": event.news_category,
                "news_title": event.news_title,
                "reading_duration": event.reading_duration,
                "scroll_percentage": event.scroll_percentage,
                "engagement_score": engagement_score,
                "timestamp": event.timestamp
            }
            
            # 💾 保存到数据库
            if db.save_user_behavior(behavior_data):
                # 🔄 更新内存缓存
                self._store_behavior_in_cache(behavior_data)
                
                # 🧠 智能学习更新
                learning_result = self._intelligent_preference_update(behavior_data)
                
                # 🗑️ 数据清理（定期清理旧数据）
                self._cleanup_old_data(event.user_id)
                
                # 📊 更新统计
                self._update_statistics(behavior_data)
                
                # 📊 计算用户置信度
                user_confidence = self._calculate_user_confidence(event.user_id)
                
                return {
                    "success": True,
                    "behavior_id": behavior_id,
                    "enhanced_action": enhanced_action,
                    "engagement_score": engagement_score,
                    "learning_update": learning_result,
                    "user_confidence": user_confidence
                }
            else:
                return {
                    "success": False,
                    "error": "数据库保存失败"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"内部错误: {str(e)}"
            }
    
    def _store_behavior_in_cache(self, behavior_data: Dict) -> None:
        """将行为数据存储到内存缓存"""
        user_id = behavior_data["user_id"]
        
        if user_id not in self.user_behaviors_cache:
            self.user_behaviors_cache[user_id] = []
        
        self.user_behaviors_cache[user_id].append(behavior_data)
        
        # 保持缓存不超过100条记录（性能优化）
        if len(self.user_behaviors_cache[user_id]) > 100:
            self.user_behaviors_cache[user_id] = self.user_behaviors_cache[user_id][-100:]
    
    def _intelligent_preference_update(self, behavior_data: Dict) -> Dict:
        """
        🧠 智能偏好更新算法 (带缓存优化)
        """
        user_id = behavior_data["user_id"]
        category = behavior_data["news_category"]
        engagement_score = behavior_data["engagement_score"]
        
        # 🏗️ 获取或初始化用户偏好
        if user_id not in self.user_preferences_cache:
            # 尝试从数据库加载（通过profile manager）
            self.user_preferences_cache[user_id] = {
                "ai_ml": 0.125,
                "startup_venture": 0.125,
                "web3_crypto": 0.125,
                "programming": 0.125,
                "hardware_chips": 0.125,
                "consumer_tech": 0.125,
                "enterprise_saas": 0.125,
                "social_media": 0.125
            }
        
        current_prefs = self.user_preferences_cache[user_id]
        
        # 🔍 检查类别是否存在
        if category not in current_prefs:
            return {
                "category": category,
                "error": f"未知类别: {category}"
            }
        
        # 🎯 自适应学习率计算
        user_confidence = self._calculate_user_confidence(user_id)
        adaptive_lr = self._calculate_adaptive_learning_rate(user_confidence)
        
        # 📊 计算权重调整
        time_weight = self._calculate_time_weight(behavior_data["timestamp"])
        
        # 基础权重调整
        weight_adjustment = engagement_score * adaptive_lr * time_weight
        
        old_weight = current_prefs[category]
        new_weight = old_weight + weight_adjustment
        
        # 🎛️ 权重边界控制
        new_weight = max(self.learning_config['min_weight'], 
                        min(self.learning_config['max_weight'], new_weight))
        
        current_prefs[category] = new_weight
        
        # 🔄 智能归一化
        self._smart_normalize_weights(current_prefs, category, weight_adjustment)
        
        # 📊 更新学习统计
        self.system_stats['learning_updates'] += 1
        
        return {
            "category": category,
            "action": behavior_data["action"],
            "old_weight": round(old_weight, 4),
            "new_weight": round(current_prefs[category], 4),
            "adjustment": round(weight_adjustment, 4),
            "learning_rate": round(adaptive_lr, 4),
            "user_confidence": round(user_confidence, 3),
            "engagement_score": round(engagement_score, 4)
        }
    
    def get_user_preferences(self, user_id: str) -> Dict[str, float]:
        """获取用户偏好 (优先从缓存)"""
        if user_id in self.user_preferences_cache:
            self.system_stats['cache_hits'] += 1
            return self.user_preferences_cache[user_id].copy()
        
        # 缓存未命中，返回默认值
        self.system_stats['cache_misses'] += 1
        default_prefs = {
            "ai_ml": 0.125,
            "startup_venture": 0.125, 
            "web3_crypto": 0.125,
            "programming": 0.125,
            "hardware_chips": 0.125,
            "consumer_tech": 0.125,
            "enterprise_saas": 0.125,
            "social_media": 0.125
        }
        
        self.user_preferences_cache[user_id] = default_prefs
        return default_prefs.copy()
    
    def get_intelligent_recommendations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """智能推荐生成"""
        if not self.recommendation_engine:
            raise Exception("推荐引擎未初始化")
        
        # 📊 获取学习后的用户偏好
        learned_preferences = self.get_user_preferences(user_id)
        
        # 🎯 提取用户主要兴趣
        sorted_prefs = sorted(learned_preferences.items(), key=lambda x: x[1], reverse=True)
        user_interests = [cat for cat, weight in sorted_prefs if weight > 0.1][:3]
        
        # 🚀 生成推荐
        recommendations = self.recommendation_engine.recommend_for_user(
            user_id=user_id,
            user_interests=user_interests,
            user_weights=learned_preferences,
            limit=limit
        )
        
        return recommendations
    
    def get_system_statistics(self) -> Dict:
        """获取系统统计信息"""
        # 获取数据库统计
        db_stats = db.get_database_stats()
        
        # 更新内存统计
        active_users = len(self.user_behaviors_cache)
        total_behaviors = self.system_stats['total_behaviors']
        
        return {
            **self.system_stats,
            "active_users": active_users,
            "avg_behaviors_per_user": total_behaviors / max(active_users, 1),
            "learning_efficiency": self.system_stats['learning_updates'] / max(total_behaviors, 1),
            "database_stats": db_stats,
            "cache_performance": {
                "cache_hits": self.system_stats['cache_hits'],
                "cache_misses": self.system_stats['cache_misses'],
                "hit_rate": f"{self.system_stats['cache_hits'] / max(self.system_stats['cache_hits'] + self.system_stats['cache_misses'], 1) * 100:.1f}%"
            }
        }
    
    def analyze_user_behavior_patterns(self, user_id: str, days: int = 7) -> Dict:
        """用户行为分析 (从数据库获取完整历史)"""
        try:
            # 从数据库获取用户行为
            behaviors = db.load_user_behaviors(user_id, limit=1000)
            
            if not behaviors:
                return {"error": "用户行为数据不存在"}
            
            # 过滤指定天数的数据
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_behaviors = []
            
            for b in behaviors:
                try:
                    if datetime.fromisoformat(b["timestamp"]) > cutoff_date:
                        recent_behaviors.append(b)
                except:
                    continue
            
            if not recent_behaviors:
                return {"error": f"最近{days}天没有行为数据"}
            
            # 基础统计
            action_counts = {}
            for behavior in recent_behaviors:
                action = behavior.get('action', 'unknown')
                action_counts[action] = action_counts.get(action, 0) + 1
            
            return {
                "user_id": user_id,
                "total_behaviors": len(recent_behaviors),
                "action_distribution": action_counts,
                "user_type": self._classify_user_type(action_counts),
                "analysis_period_days": days
            }
            
        except Exception as e:
            return {"error": f"分析失败: {str(e)}"}
    
    # ===========================================
    # 🔧 数据库特定方法
    # ===========================================
    
    def sync_cache_to_db(self) -> int:
        """将缓存数据同步到数据库"""
        synced_count = 0
        
        # 这里主要是preferences缓存，因为behaviors已经实时保存
        # 如果有需要，可以实现preferences的定期保存
        
        return synced_count
    
    def reload_from_db(self):
        """从数据库重新加载数据"""
        self.user_behaviors_cache.clear()
        self.user_preferences_cache.clear()
        self._load_behaviors_from_db()
        print("✅ 从数据库重新加载行为数据")
    
    def cleanup_old_behaviors(self, days: int = 30) -> int:
        """清理数据库中的旧行为数据"""
        return db.cleanup_old_behaviors(days)
    
    # ===========================================
    # 🔧 原有辅助方法 (保持不变)
    # ===========================================
    
    def _calculate_user_confidence(self, user_id: str) -> float:
        """用户置信度计算 (基于缓存数据)"""
        if user_id not in self.user_behaviors_cache:
            return 0.0
        
        behavior_count = len(self.user_behaviors_cache[user_id])
        confidence_threshold = self.learning_config['confidence_threshold']
        
        # 基于行为数量的置信度
        base_confidence = min(behavior_count / confidence_threshold, 1.0)
        
        # 基于行为多样性的调整
        if behavior_count > 0:
            actions = [b.get("action", "") for b in self.user_behaviors_cache[user_id]]
            unique_actions = len(set(actions))
            diversity_bonus = min(unique_actions / 6, 0.2)
            base_confidence += diversity_bonus
        
        return min(base_confidence, 1.0)
    
    def _detect_anomaly_light(self, event: BehaviorEvent) -> bool:
        """轻量级异常检测"""
        if self.test_mode:
            # 测试模式：只检测超高频率
            user_id = event.user_id
            
            try:
                current_time = datetime.fromisoformat(event.timestamp)
            except:
                return False
            
            if user_id not in self.anomaly_detection:
                self.anomaly_detection[user_id] = {
                    "behavior_count_last_hour": 0,
                    "reset_time": current_time
                }
                return False
            
            user_anomaly = self.anomaly_detection[user_id]
            
            # 重置计数
            if current_time - user_anomaly["reset_time"] > timedelta(hours=1):
                user_anomaly["behavior_count_last_hour"] = 0
                user_anomaly["reset_time"] = current_time
            
            # 只检测超高频率
            user_anomaly["behavior_count_last_hour"] += 1
            if user_anomaly["behavior_count_last_hour"] > 1000:
                return True
            
            return False
        
        # 生产模式的异常检测逻辑...
        return False
    
    # 其他辅助方法保持原有实现...
    def _smart_action_adjustment(self, event: BehaviorEvent) -> str:
        """智能行为类型调整"""
        action = event.action
        duration = event.reading_duration
        scroll = event.scroll_percentage
        
        if action == 'read':
            if duration >= self.engagement_thresholds['deep_read_duration']:
                if scroll >= self.engagement_thresholds['high_scroll']:
                    return 'deep_read'
                else:
                    return 'read'
            elif duration <= self.engagement_thresholds['skip_duration']:
                return 'skip'
            elif scroll < self.engagement_thresholds['low_scroll']:
                return 'skip'
        
        elif action == 'click':
            if duration > self.engagement_thresholds['quality_reading']:
                return 'read'
            elif duration <= self.engagement_thresholds['bounce_threshold']:
                return 'skip'
        
        return action
    
    def _calculate_enhanced_engagement(self, event: BehaviorEvent, action: str) -> float:
        """计算增强参与度分数"""
        base_score = self.behavior_weights.get(action, 0.01)
        
        # 时长调整
        if action in ['read', 'deep_read']:
            if event.reading_duration > 60:
                duration_factor = min(event.reading_duration / 120, 1.0)
                base_score *= (1 + duration_factor * 0.5)
        
        # 滚动调整
        if event.scroll_percentage > self.engagement_thresholds['high_scroll']:
            base_score *= 1.3
        elif event.scroll_percentage < self.engagement_thresholds['low_scroll']:
            base_score *= 0.7
        
        # 时间上下文调整
        try:
            hour = datetime.fromisoformat(event.timestamp).hour
            if 9 <= hour <= 17:  # 工作时间
                base_score *= 1.1
            elif 21 <= hour <= 23:  # 晚上深度阅读时间
                base_score *= 1.2
        except:
            pass
        
        return max(0.001, base_score)
    
    def _calculate_adaptive_learning_rate(self, confidence: float) -> float:
        """自适应学习率计算"""
        base_lr = self.learning_config['base_learning_rate']
        
        if confidence < 0.3:
            return base_lr * 1.4  # 新用户学更快
        elif confidence > 0.7:
            return base_lr * 0.8  # 老用户学更稳
        else:
            return base_lr
    
    def _smart_normalize_weights(self, weights: Dict[str, float], 
                                updated_category: str, adjustment: float) -> None:
        """智能权重归一化"""
        total = sum(weights.values())
        
        if total <= 0:
            # 重置为均匀分布
            uniform_weight = 1.0 / len(weights)
            for category in weights:
                weights[category] = uniform_weight
            return
        
        # 如果是正向调整，从其他类别按比例减少
        if adjustment > 0:
            other_categories = [cat for cat in weights if cat != updated_category]
            total_other = sum(weights[cat] for cat in other_categories)
            
            if total_other > 0 and total > 1.0:
                excess = total - 1.0
                reduction_factor = excess / total_other
                
                for cat in other_categories:
                    weights[cat] *= (1 - reduction_factor)
                    # 确保不会低于最小权重
                    weights[cat] = max(self.learning_config['min_weight'], weights[cat])
        
        # 最终归一化确保和为1
        final_total = sum(weights.values())
        if final_total > 0:
            for category in weights:
                weights[category] /= final_total
    
    def _calculate_time_weight(self, timestamp: str) -> float:
        """计算时间权重"""
        try:
            behavior_time = datetime.fromisoformat(timestamp)
            hours_ago = (datetime.now() - behavior_time).total_seconds() / 3600
            days_ago = hours_ago / 24
            
            time_weight = self.learning_config['decay_factor'] ** days_ago
            return max(0.1, time_weight)
        except:
            return 1.0
    
    def _cleanup_old_data(self, user_id: str) -> None:
        """清理缓存中的过期数据"""
        if user_id not in self.user_behaviors_cache:
            return
        
        max_days = self.learning_config['max_days']
        cutoff_date = datetime.now() - timedelta(days=max_days)
        
        cleaned_behaviors = []
        for b in self.user_behaviors_cache[user_id]:
            try:
                if datetime.fromisoformat(b["timestamp"]) > cutoff_date:
                    cleaned_behaviors.append(b)
            except:
                continue
        
        self.user_behaviors_cache[user_id] = cleaned_behaviors
    
    def _update_statistics(self, behavior_data: Dict) -> None:
        """更新系统统计"""
        self.system_stats['total_behaviors'] += 1
        
        user_id = behavior_data["user_id"]
        if user_id not in self.user_behaviors_cache or len(self.user_behaviors_cache[user_id]) == 1:
            self.system_stats['total_users'] += 1
    
    def _classify_user_type(self, action_counts: Dict) -> str:
        """用户类型分类"""
        total_actions = sum(action_counts.values())
        if total_actions == 0:
            return "inactive"
        
        deep_read_ratio = action_counts.get('deep_read', 0) / total_actions
        share_ratio = action_counts.get('share', 0) / total_actions
        skip_ratio = action_counts.get('skip', 0) / total_actions
        
        if deep_read_ratio > 0.3:
            return "deep_reader"
        elif share_ratio > 0.1:
            return "active_sharer"
        elif skip_ratio > 0.4:
            return "quick_scanner"
        else:
            return "casual_reader"