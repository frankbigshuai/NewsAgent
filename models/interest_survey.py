# interest_survey.py - TechSum 用户兴趣问卷系统
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class InterestSurvey:
    """全方位用户兴趣问卷系统"""
    
    def __init__(self):
        self.survey_structure = {
            "技术兴趣": {
                "question": "以下技术领域，你最关注哪些？(最多选4个)",
                "type": "multiple_choice",
                "options": {
                    "ai_ml": "🤖 AI/机器学习",
                    "programming": "💻 编程开发",
                    "web3_crypto": "🔗 区块链/加密货币", 
                    "startup_venture": "🚀 创业投资",
                    "hardware_chips": "⚡ 硬件芯片",
                    "consumer_tech": "📱 消费电子",
                    "enterprise_saas": "🏢 企业服务",
                    "social_media": "📢 社交媒体"
                },
                "max_selections": 4,
                "weight": 0.4,  # 在画像中的权重
                "required": True
            },
            
            "专业背景": {
                "question": "你的专业背景是？",
                "type": "single_choice",
                "options": {
                    "engineer": "👨‍💻 工程师/开发者",
                    "product": "📋 产品经理",
                    "design": "🎨 设计师",
                    "investor": "💰 投资人",
                    "media": "📺 媒体/KOL",
                    "entrepreneur": "🚀 创业者",
                    "student": "🎓 学生",
                    "other": "🔧 其他"
                },
                "weight": 0.2,
                "required": True
            },
            
            "阅读习惯": {
                "question": "你更喜欢什么样的内容？",
                "type": "single_choice", 
                "options": {
                    "deep": "📚 深度长文，详细分析",
                    "summary": "⚡ 精简摘要，抓住要点",
                    "news": "📰 新闻快讯，及时更新",
                    "opinion": "💭 观点评论，多角度思考"
                },
                "weight": 0.15,
                "required": True
            },
            
            "使用场景": {
                "question": "你通常什么时候阅读科技新闻？(最多选3个)",
                "type": "multiple_choice",
                "options": {
                    "morning": "🌅 早晨通勤",
                    "lunch": "🍽️ 午休时间", 
                    "evening": "🌆 晚上下班后",
                    "weekend": "🏖️ 周末闲暇",
                    "anytime": "⏰ 随时随地"
                },
                "max_selections": 3,
                "weight": 0.15,
                "required": False
            },
            
            "AI关注程度": {
                "question": "对于AI/ML内容，你的关注程度是？",
                "type": "scale",
                "scale": 5,
                "labels": ["😴 不感兴趣", "😐 略有关注", "🙂 一般关注", "😃 很感兴趣", "🤩 极度关注"],
                "weight": 0.1,
                "required": False
            }
        }
        
        # 问卷元数据
        self.survey_metadata = {
            "version": "1.0",
            "estimated_time": "2-3分钟",
            "total_questions": len(self.survey_structure),
            "created_at": datetime.now().isoformat()
        }
    
    def get_survey_for_frontend(self) -> Dict[str, Any]:
        """
        获取前端友好的问卷格式
        """
        return {
            "metadata": self.survey_metadata,
            "questions": self.survey_structure
        }
    
    def validate_answers(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证用户答案的有效性
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        for question_id, question_config in self.survey_structure.items():
            user_answer = answers.get(question_id)
            
            # 检查必填项
            if question_config.get("required", False) and not user_answer:
                validation_result["valid"] = False
                validation_result["errors"].append(f"问题 '{question_id}' 是必填项")
                continue
            
            if not user_answer:
                continue
                
            # 验证答案格式
            if question_config["type"] == "single_choice":
                if user_answer not in question_config["options"]:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"问题 '{question_id}' 答案无效")
                    
            elif question_config["type"] == "multiple_choice":
                if not isinstance(user_answer, list):
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"问题 '{question_id}' 应该是列表格式")
                    continue
                
                # 检查选择数量限制
                max_selections = question_config.get("max_selections", len(question_config["options"]))
                if len(user_answer) > max_selections:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"问题 '{question_id}' 最多选择{max_selections}个选项")
                
                # 检查选项有效性
                for option in user_answer:
                    if option not in question_config["options"]:
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"问题 '{question_id}' 包含无效选项: {option}")
                        
            elif question_config["type"] == "scale":
                try:
                    scale_value = int(user_answer)
                    if not (1 <= scale_value <= question_config["scale"]):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"问题 '{question_id}' 评分应在1-{question_config['scale']}之间")
                except (ValueError, TypeError):
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"问题 '{question_id}' 评分格式无效")
        
        return validation_result
    
    def convert_answers_to_profile(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        将问卷答案转换为用户画像初始数据
        """
        # 首先验证答案
        validation = self.validate_answers(answers)
        if not validation["valid"]:
            raise ValueError(f"问卷答案验证失败: {validation['errors']}")
        
        profile_data = {
            "basic_info": {},
            "interest_weights": {},
            "behavior_profile": {},
            "personalization": {},
            "survey_data": answers.copy()
        }
        
        # 1. 处理技术兴趣 → 兴趣权重
        tech_interests = answers.get("技术兴趣", [])
        if tech_interests:
            # 基础权重：每个类别 0.125 (1/8)
            base_weight = 0.125
            interest_boost = 0.15  # 选中的类别额外获得的权重
            
            # 初始化所有类别为基础权重
            all_categories = ["ai_ml", "programming", "web3_crypto", "startup_venture", 
                            "hardware_chips", "consumer_tech", "enterprise_saas", "social_media"]
            
            profile_data["interest_weights"] = {cat: base_weight for cat in all_categories}
            
            # 为选中的类别增加权重
            if tech_interests:
                boost_per_category = interest_boost / len(tech_interests)
                total_reduction = interest_boost / (len(all_categories) - len(tech_interests))
                
                for category in tech_interests:
                    profile_data["interest_weights"][category] += boost_per_category
                
                # 从未选中的类别中按比例减少权重
                for category in all_categories:
                    if category not in tech_interests:
                        profile_data["interest_weights"][category] -= total_reduction
                        # 确保权重不会为负
                        profile_data["interest_weights"][category] = max(0.02, profile_data["interest_weights"][category])
        
        # 2. 处理专业背景
        background = answers.get("专业背景")
        if background:
            profile_data["basic_info"]["professional_background"] = background
            
            # 根据专业背景调整某些类别权重
            background_adjustments = {
                "engineer": {"programming": 0.05, "ai_ml": 0.03},
                "product": {"startup_venture": 0.04, "consumer_tech": 0.03},
                "investor": {"startup_venture": 0.06, "web3_crypto": 0.02},
                "media": {"social_media": 0.04, "consumer_tech": 0.02},
                "entrepreneur": {"startup_venture": 0.05, "enterprise_saas": 0.03}
            }
            
            adjustments = background_adjustments.get(background, {})
            for category, adjustment in adjustments.items():
                if category in profile_data["interest_weights"]:
                    profile_data["interest_weights"][category] += adjustment
        
        # 3. 处理阅读习惯
        reading_habit = answers.get("阅读习惯")
        if reading_habit:
            profile_data["basic_info"]["reading_preference"] = reading_habit
            
            # 映射到行为特征
            reading_depth_mapping = {
                "deep": "deep",
                "summary": "medium", 
                "news": "light",
                "opinion": "medium"
            }
            profile_data["behavior_profile"]["reading_depth"] = reading_depth_mapping.get(reading_habit, "medium")
            profile_data["personalization"]["preferred_content_type"] = reading_habit
        
        # 4. 处理使用场景
        usage_scenarios = answers.get("使用场景", [])
        if usage_scenarios:
            profile_data["basic_info"]["usage_scenarios"] = usage_scenarios
            
            # 根据使用场景推断活跃度
            if len(usage_scenarios) >= 4:
                profile_data["behavior_profile"]["activity_pattern"] = "very_active"
            elif len(usage_scenarios) >= 2:
                profile_data["behavior_profile"]["activity_pattern"] = "regular"
            else:
                profile_data["behavior_profile"]["activity_pattern"] = "irregular"
        
        # 5. 处理AI关注程度
        ai_interest = answers.get("AI关注程度")
        if ai_interest:
            try:
                ai_scale = int(ai_interest)
                # 根据评分调整AI权重
                ai_weight_adjustment = (ai_scale - 3) * 0.02  # 中性值是3
                if "ai_ml" in profile_data["interest_weights"]:
                    profile_data["interest_weights"]["ai_ml"] += ai_weight_adjustment
                    profile_data["interest_weights"]["ai_ml"] = max(0.02, min(0.4, profile_data["interest_weights"]["ai_ml"]))
            except (ValueError, TypeError):
                pass
        
        # 6. 设置初始个性化参数
        profile_data["personalization"] = {
            "confidence_score": 0.3,  # 问卷完成后的初始置信度
            "total_interactions": 0,
            "last_active": datetime.now().isoformat(),
            "favorite_categories": tech_interests[:2] if tech_interests else [],
            "preferred_content_type": reading_habit or "summary",
            "onboarding_completed": True
        }
        
        # 确保权重和为1
        total_weight = sum(profile_data["interest_weights"].values())
        if total_weight > 0:
            for category in profile_data["interest_weights"]:
                profile_data["interest_weights"][category] /= total_weight
        
        return profile_data
    
    def get_survey_summary(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成问卷结果摘要（用于向用户展示）
        """
        summary = {
            "completion_time": datetime.now().isoformat(),
            "total_questions": len(self.survey_structure),
            "answered_questions": len([q for q in answers.values() if q]),
            "completion_rate": len([q for q in answers.values() if q]) / len(self.survey_structure) * 100
        }
        
        # 生成兴趣标签
        tech_interests = answers.get("技术兴趣", [])
        interest_labels = []
        for interest in tech_interests:
            if interest in self.survey_structure["技术兴趣"]["options"]:
                interest_labels.append(self.survey_structure["技术兴趣"]["options"][interest])
        
        summary["interest_labels"] = interest_labels
        summary["primary_interests"] = tech_interests
        summary["professional_background"] = answers.get("专业背景", "未填写")
        summary["reading_preference"] = answers.get("阅读习惯", "未填写")
        
        return summary

# 创建全局实例
survey_instance = InterestSurvey()