from typing import Dict, List, Optional
from datetime import datetime
import uuid

class ComprehensiveSurveySystem:
    """全方位问卷系统 - Day 5的核心工作"""
    
    def __init__(self):
        self.survey_config = self._init_survey_config()
        self.user_profiles = {}
    
    def _init_survey_config(self) -> Dict:
        """初始化问卷配置 - Day 5任务"""
        return {
            "steps": [
                {
                    "step": 1,
                    "title": "您的职业身份",
                    "type": "single_choice",
                    "options": [
                        {"id": "engineer", "name": "软件工程师", "icon": "💻"},
                        {"id": "product_manager", "name": "产品经理", "icon": "📱"},
                        {"id": "investor", "name": "投资人", "icon": "💰"},
                        {"id": "founder", "name": "创业者", "icon": "🚀"},
                        {"id": "student", "name": "学生", "icon": "🎓"},
                        {"id": "tech_enthusiast", "name": "科技爱好者", "icon": "🔥"}
                    ]
                },
                {
                    "step": 2,
                    "title": "您的专业水平",
                    "type": "single_choice",
                    "options": [
                        {"id": "beginner", "name": "初学者", "icon": "🌱"},
                        {"id": "intermediate", "name": "中级", "icon": "📈"},
                        {"id": "advanced", "name": "高级", "icon": "🎯"},
                        {"id": "expert", "name": "专家", "icon": "🏆"}
                    ]
                },
                {
                    "step": 3,
                    "title": "感兴趣的领域",
                    "type": "multiple_choice",
                    "min_selection": 3,
                    "max_selection": 5,
                    "options": [
                        {"id": "ai_ml", "name": "人工智能", "icon": "🤖"},
                        {"id": "startup_venture", "name": "创业投资", "icon": "🚀"},
                        {"id": "web3_crypto", "name": "区块链", "icon": "🔗"},
                        {"id": "programming", "name": "编程开发", "icon": "💻"},
                        {"id": "hardware_chips", "name": "硬件芯片", "icon": "🔧"},
                        {"id": "consumer_tech", "name": "消费科技", "icon": "📱"}
                    ]
                },
                {
                    "step": 4,
                    "title": "阅读偏好",
                    "type": "single_choice",
                    "options": [
                        {"id": "quick_updates", "name": "快速资讯", "icon": "⚡"},
                        {"id": "detailed_analysis", "name": "深度分析", "icon": "📊"},
                        {"id": "visual_content", "name": "视觉内容", "icon": "🎨"},
                        {"id": "balanced", "name": "均衡搭配", "icon": "⚖️"}
                    ]
                },
                {
                    "step": 5,
                    "title": "使用场景",
                    "type": "multiple_choice",
                    "min_selection": 1,
                    "max_selection": 3,
                    "options": [
                        {"id": "morning_commute", "name": "早晨通勤", "icon": "🚇"},
                        {"id": "work_break", "name": "工作间隙", "icon": "☕"},
                        {"id": "evening_deep_dive", "name": "晚间深度阅读", "icon": "🌙"},
                        {"id": "weekend_research", "name": "周末研究", "icon": "📚"}
                    ]
                }
            ]
        }
    
    def get_survey_step(self, step_number: int) -> Dict:
        """获取问卷步骤 - Day 5任务"""
        if 1 <= step_number <= len(self.survey_config["steps"]):
            return self.survey_config["steps"][step_number - 1]
        return {"error": "无效的步骤号"}
    
    def submit_survey_step(self, session_id: str, step: int, answers: Dict) -> Dict:
        """提交问卷步骤 - Day 5任务"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # 初始化用户画像
        if session_id not in self.user_profiles:
            self.user_profiles[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "steps_completed": [],
                "survey_data": {}
            }
        
        # 保存步骤数据
        self.user_profiles[session_id]["survey_data"][f"step_{step}"] = answers
        
        if step not in self.user_profiles[session_id]["steps_completed"]:
            self.user_profiles[session_id]["steps_completed"].append(step)
        
        return {
            "session_id": session_id,
            "step_saved": step,
            "completed_steps": len(self.user_profiles[session_id]["steps_completed"]),
            "is_complete": len(self.user_profiles[session_id]["steps_completed"]) >= 5
        }
    
    def complete_survey(self, session_id: str) -> Dict:
        """完成问卷并生成用户画像 - Day 5核心任务"""
        if session_id not in self.user_profiles:
            return {"error": "用户画像不存在"}
        
        profile_data = self.user_profiles[session_id]
        
        # 构建结构化画像
        structured_profile = self._build_structured_profile(profile_data)
        
        # 计算智能权重
        intelligent_weights = self._calculate_intelligent_weights(structured_profile)
        
        # 保存到推荐系统
        global user_preferences
        user_preferences[session_id] = {
            "categories": structured_profile["interest_categories"],
            "weights": intelligent_weights,
            "user_role": structured_profile["user_role"],
            "experience_level": structured_profile["experience_level"],
            "reading_preference": structured_profile["reading_preference"],
            "usage_scenarios": structured_profile["usage_scenarios"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "onboarding_completed": True,
            "profile_version": "comprehensive_v1.0"
        }
        
        return {
            "status": "success",
            "session_id": session_id,
            "profile_summary": structured_profile,
            "intelligent_weights": intelligent_weights
        }
    
    def _build_structured_profile(self, profile_data: Dict) -> Dict:
        """构建结构化画像 - Day 5任务"""
        survey_data = profile_data["survey_data"]
        
        return {
            "user_role": survey_data.get("step_1"),
            "experience_level": survey_data.get("step_2"),
            "interest_categories": survey_data.get("step_3", []),
            "reading_preference": survey_data.get("step_4"),
            "usage_scenarios": survey_data.get("step_5", [])
        }
    
    def _calculate_intelligent_weights(self, profile: Dict) -> Dict[str, float]:
        """计算智能权重 - Day 5核心算法"""
        categories = profile["interest_categories"]
        if not categories:
            return {}
        
        # 基础权重（均等分配）
        base_weight = 1.0 / len(categories)
        weights = {cat: base_weight for cat in categories}
        
        # 根据用户角色调整权重
        role_multipliers = {
            "engineer": {"programming": 1.3, "ai_ml": 1.2, "hardware_chips": 1.1},
            "product_manager": {"consumer_tech": 1.3, "startup_venture": 1.2},
            "investor": {"startup_venture": 1.4, "web3_crypto": 1.2},
            "founder": {"startup_venture": 1.4, "ai_ml": 1.1}
        }
        
        user_role = profile["user_role"]
        if user_role in role_multipliers:
            for category, multiplier in role_multipliers[user_role].items():
                if category in weights:
                    weights[category] *= multiplier
        
        # 根据经验水平调整
        experience_multipliers = {
            "beginner": {"programming": 0.8, "hardware_chips": 0.9},
            "expert": {"ai_ml": 1.2, "hardware_chips": 1.1}
        }
        
        experience = profile["experience_level"]
        if experience in experience_multipliers:
            for category, multiplier in experience_multipliers[experience].items():
                if category in weights:
                    weights[category] *= multiplier
        
        # 重新归一化
        total = sum(weights.values())
        if total > 0:
            for category in weights:
                weights[category] /= total
        
        return weights