# database.py - TechSum 数据持久化系统
import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import contextmanager

class TechSumDatabase:
    """TechSum数据库管理器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, "techsum.db")
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 用户画像表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    basic_info TEXT NOT NULL,
                    interest_weights TEXT NOT NULL,
                    behavior_profile TEXT NOT NULL,
                    personalization TEXT NOT NULL,
                    survey_data TEXT NOT NULL
                )
            """)
            
            # 用户行为表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_behaviors (
                    behavior_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    news_id TEXT NOT NULL,
                    news_category TEXT NOT NULL,
                    news_title TEXT,
                    reading_duration INTEGER DEFAULT 0,
                    scroll_percentage REAL DEFAULT 0.0,
                    engagement_score REAL DEFAULT 0.0,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            """)
            
            # 新闻反馈表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news_feedback (
                    feedback_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    news_id TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    feedback TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
                )
            """)
            
            # 系统统计表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_stats (
                    stat_key TEXT PRIMARY KEY,
                    stat_value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            print("✅ 数据库表初始化完成")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 允许通过列名访问
        try:
            yield conn
        finally:
            conn.close()
    
    # ===========================================
    # 用户画像相关操作
    # ===========================================
    
    def save_user_profile(self, profile_dict: Dict[str, Any]) -> bool:
        """保存用户画像"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO user_profiles 
                    (user_id, created_at, updated_at, basic_info, interest_weights, 
                     behavior_profile, personalization, survey_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile_dict["user_id"],
                    profile_dict["created_at"],
                    profile_dict["updated_at"],
                    json.dumps(profile_dict["basic_info"]),
                    json.dumps(profile_dict["interest_weights"]),
                    json.dumps(profile_dict["behavior_profile"]),
                    json.dumps(profile_dict["personalization"]),
                    json.dumps(profile_dict["survey_data"])
                ))
                
                conn.commit()
                print(f"✅ 用户画像保存成功: {profile_dict['user_id']}")
                return True
                
        except Exception as e:
            print(f"❌ 保存用户画像失败: {e}")
            return False
    
    def load_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """加载用户画像"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM user_profiles WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                return {
                    "user_id": row["user_id"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                    "basic_info": json.loads(row["basic_info"]),
                    "interest_weights": json.loads(row["interest_weights"]),
                    "behavior_profile": json.loads(row["behavior_profile"]),
                    "personalization": json.loads(row["personalization"]),
                    "survey_data": json.loads(row["survey_data"])
                }
                
        except Exception as e:
            print(f"❌ 加载用户画像失败: {e}")
            return None
    
    def load_all_user_profiles(self) -> Dict[str, Dict[str, Any]]:
        """加载所有用户画像"""
        profiles = {}
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT user_id FROM user_profiles")
                user_ids = [row["user_id"] for row in cursor.fetchall()]
                
                for user_id in user_ids:
                    profile = self.load_user_profile(user_id)
                    if profile:
                        profiles[user_id] = profile
                
                print(f"✅ 加载了 {len(profiles)} 个用户画像")
                
        except Exception as e:
            print(f"❌ 加载所有用户画像失败: {e}")
        
        return profiles
    
    # ===========================================
    # 用户行为相关操作
    # ===========================================
    
    def save_user_behavior(self, behavior_dict: Dict[str, Any]) -> bool:
        """保存用户行为"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO user_behaviors 
                    (behavior_id, user_id, action, news_id, news_category, news_title,
                     reading_duration, scroll_percentage, engagement_score, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    behavior_dict["behavior_id"],
                    behavior_dict["user_id"],
                    behavior_dict["action"],
                    behavior_dict["news_id"],
                    behavior_dict["news_category"],
                    behavior_dict.get("news_title", ""),
                    behavior_dict.get("reading_duration", 0),
                    behavior_dict.get("scroll_percentage", 0.0),
                    behavior_dict.get("engagement_score", 0.0),
                    behavior_dict["timestamp"]
                ))
                
                conn.commit()
                print(f"✅ 用户行为保存成功: {behavior_dict['behavior_id']}")
                return True
                
        except Exception as e:
            print(f"❌ 保存用户行为失败: {e}")
            return False
    
    def load_user_behaviors(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """加载用户行为历史"""
        behaviors = []
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM user_behaviors 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (user_id, limit))
                
                for row in cursor.fetchall():
                    behaviors.append({
                        "behavior_id": row["behavior_id"],
                        "user_id": row["user_id"],
                        "action": row["action"],
                        "news_id": row["news_id"],
                        "news_category": row["news_category"],
                        "news_title": row["news_title"],
                        "reading_duration": row["reading_duration"],
                        "scroll_percentage": row["scroll_percentage"],
                        "engagement_score": row["engagement_score"],
                        "timestamp": row["timestamp"]
                    })
                
                print(f"✅ 加载了用户 {user_id} 的 {len(behaviors)} 条行为记录")
                
        except Exception as e:
            print(f"❌ 加载用户行为失败: {e}")
        
        return behaviors
    
    def load_all_user_behaviors(self) -> Dict[str, List[Dict[str, Any]]]:
        """加载所有用户行为"""
        all_behaviors = {}
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT DISTINCT user_id FROM user_behaviors")
                user_ids = [row["user_id"] for row in cursor.fetchall()]
                
                for user_id in user_ids:
                    behaviors = self.load_user_behaviors(user_id)
                    if behaviors:
                        all_behaviors[user_id] = behaviors
                
                print(f"✅ 加载了 {len(all_behaviors)} 个用户的行为数据")
                
        except Exception as e:
            print(f"❌ 加载所有用户行为失败: {e}")
        
        return all_behaviors
    
    # ===========================================
    # 反馈相关操作
    # ===========================================
    
    def save_news_feedback(self, feedback_dict: Dict[str, Any]) -> bool:
        """保存新闻反馈"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO news_feedback 
                    (feedback_id, user_id, news_id, rating, feedback, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    feedback_dict["feedback_id"],
                    feedback_dict["user_id"],
                    feedback_dict["news_id"],
                    feedback_dict["rating"],
                    feedback_dict.get("feedback", ""),
                    feedback_dict["timestamp"]
                ))
                
                conn.commit()
                print(f"✅ 新闻反馈保存成功: {feedback_dict['feedback_id']}")
                return True
                
        except Exception as e:
            print(f"❌ 保存新闻反馈失败: {e}")
            return False
    
    # ===========================================
    # 统计相关操作
    # ===========================================
    
    def save_system_stats(self, stats: Dict[str, Any]) -> bool:
        """保存系统统计"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                current_time = datetime.now().isoformat()
                
                for key, value in stats.items():
                    cursor.execute("""
                        INSERT OR REPLACE INTO system_stats 
                        (stat_key, stat_value, updated_at)
                        VALUES (?, ?, ?)
                    """, (key, json.dumps(value), current_time))
                
                conn.commit()
                print("✅ 系统统计保存成功")
                return True
                
        except Exception as e:
            print(f"❌ 保存系统统计失败: {e}")
            return False
    
    def load_system_stats(self) -> Dict[str, Any]:
        """加载系统统计"""
        stats = {}
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT stat_key, stat_value FROM system_stats")
                for row in cursor.fetchall():
                    stats[row["stat_key"]] = json.loads(row["stat_value"])
                
                print(f"✅ 加载了 {len(stats)} 项系统统计")
                
        except Exception as e:
            print(f"❌ 加载系统统计失败: {e}")
        
        return stats
    
    # ===========================================
    # 数据库维护
    # ===========================================
    
    def cleanup_old_behaviors(self, days: int = 30) -> int:
        """清理旧的行为数据"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.isoformat()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM user_behaviors 
                    WHERE timestamp < ?
                """, (cutoff_str,))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                print(f"✅ 清理了 {deleted_count} 条旧行为记录")
                return deleted_count
                
        except Exception as e:
            print(f"❌ 清理旧行为数据失败: {e}")
            return 0
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        stats = {}
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 用户数量
                cursor.execute("SELECT COUNT(*) as count FROM user_profiles")
                stats["total_users"] = cursor.fetchone()["count"]
                
                # 行为记录数量
                cursor.execute("SELECT COUNT(*) as count FROM user_behaviors")
                stats["total_behaviors"] = cursor.fetchone()["count"]
                
                # 反馈数量
                cursor.execute("SELECT COUNT(*) as count FROM news_feedback")
                stats["total_feedback"] = cursor.fetchone()["count"]
                
                # 数据库文件大小
                if os.path.exists(self.db_path):
                    stats["db_size_mb"] = round(os.path.getsize(self.db_path) / 1024 / 1024, 2)
                
                print("✅ 数据库统计获取成功")
                
        except Exception as e:
            print(f"❌ 获取数据库统计失败: {e}")
        
        return stats

# 创建全局数据库实例
db = TechSumDatabase()

if __name__ == "__main__":
    # 测试数据库功能
    print("🧪 测试数据库功能...")
    
    # 测试保存用户画像
    test_profile = {
        "user_id": "test_db_user",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "basic_info": {"bg": "engineer"},
        "interest_weights": {"ai_ml": 0.5, "programming": 0.3},
        "behavior_profile": {"depth": "medium"},
        "personalization": {"confidence": 0.3},
        "survey_data": {"tech_interests": ["ai_ml"]}
    }
    
    db.save_user_profile(test_profile)
    loaded_profile = db.load_user_profile("test_db_user")
    print(f"📊 加载的画像: {loaded_profile}")
    
    # 测试数据库统计
    stats = db.get_database_stats()
    print(f"📈 数据库统计: {stats}")