# survey_api.py - 修复版 (解决导入和Pydantic问题)
import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent  # 回到项目根目录
sys.path.insert(0, str(project_root))

# Railway环境适配
def get_railway_config():
    """获取Railway环境配置"""
    return {
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", "8001")),
        "debug": os.getenv("RAILWAY_ENVIRONMENT", "production") != "production"
    }

# 尝试导入你的核心系统，修复导入路径
try:
    # 尝试多种导入路径
    try:
        # 方式1: 从当前目录的models
        from models.interest_survey import survey_instance
        from models.user_profile import UserProfileManager
        from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
        from models.cached_recommendation_engine import CachedRecommendationEngine
    except ImportError:
        # 方式2: 从上级目录的models
        sys.path.append(str(project_root))
        from models.interest_survey import survey_instance
        from models.user_profile import UserProfileManager
        from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
        from models.cached_recommendation_engine import CachedRecommendationEngine
    
    print("✅ 完整系统模块导入成功")
    print(f"📁 项目根目录: {project_root}")
    FULL_SYSTEM = True
    
    # 初始化核心系统
    print("🚀 初始化TechSum API系统...")
    recommendation_engine = CachedRecommendationEngine()
    behavior_system = EnhancedBehaviorSystem(recommendation_engine, test_mode=False)
    profile_manager = UserProfileManager(survey_instance, behavior_system)
    print("✅ TechSum API系统初始化完成")
    
except ImportError as e:
    print(f"⚠️  完整系统导入失败，使用简化版本")
    print(f"🔍 导入错误详情: {e}")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"📁 Python路径: {sys.path[:3]}...")  # 只显示前几个路径
    FULL_SYSTEM = False
    
    # 简化版本的内存存储
    class SimplifiedStorage:
        def __init__(self):
            self.users = {}
            self.behaviors = {}
            
        def get_mock_survey_data(self):
            return {
                "metadata": {
                    "version": "1.0",
                    "estimated_time": "2-3分钟",
                    "total_questions": 5
                },
                "questions": {
                    "技术兴趣": {
                        "question": "以下技术领域，你最关注哪些？(最多选4个)",
                        "type": "multiple_choice",
                        "options": {
                            "ai_ml": "🤖 AI/机器学习",
                            "programming": "💻 编程开发",
                            "web3_crypto": "🔗 区块链/加密货币",
                            "startup_venture": "🚀 创业投资",
                            "hardware_chips": "⚡ 硬件芯片",
                            "consumer_tech": "📱 消费电子"
                        },
                        "max_selections": 4
                    },
                    "专业背景": {
                        "question": "你的专业背景是？",
                        "type": "single_choice",
                        "options": {
                            "engineer": "👨‍💻 工程师/开发者",
                            "product": "📋 产品经理",
                            "investor": "💰 投资人",
                            "student": "🎓 学生",
                            "other": "🔧 其他"
                        }
                    }
                }
            }
        
        def get_mock_news_data(self):
            return [
                {
                    "id": "news_1",
                    "title": "OpenAI发布GPT-5模型，AI能力再次突破",
                    "summary": "OpenAI正式发布GPT-5，在推理能力和多模态理解方面实现重大突破",
                    "content": "OpenAI今日正式发布了备受期待的GPT-5模型。据官方介绍，GPT-5在数学推理、代码生成、多模态理解等方面相比GPT-4有显著提升...",
                    "category": "ai_ml",
                    "source": "TechCrunch",
                    "publish_time": datetime.now().isoformat(),
                    "hot_score": 0.95,
                    "personalized_score": 0.8,
                    "url": "https://techcrunch.com/gpt5-release",
                    "image_url": ""
                },
                {
                    "id": "news_2", 
                    "title": "React 19正式版发布，带来并发特性",
                    "summary": "Facebook发布React 19，新增服务器组件和并发渲染支持",
                    "content": "React团队今日发布了React 19正式版，这个版本引入了期待已久的并发特性和服务器组件支持...",
                    "category": "programming",
                    "source": "React Blog",
                    "publish_time": datetime.now().isoformat(),
                    "hot_score": 0.88,
                    "personalized_score": 0.7,
                    "url": "https://react.dev/blog/react-19",
                    "image_url": ""
                },
                {
                    "id": "news_3",
                    "title": "比特币突破10万美元大关",
                    "summary": "比特币价格首次突破10万美元，加密货币市场迎来新高点",
                    "content": "比特币价格在今日早间突破了历史性的10万美元关口，这标志着加密货币市场的又一个重要里程碑...",
                    "category": "web3_crypto",
                    "source": "CoinDesk",
                    "publish_time": datetime.now().isoformat(),
                    "hot_score": 0.92,
                    "personalized_score": 0.75,
                    "url": "https://coindesk.com/bitcoin-100k",
                    "image_url": ""
                }
            ]
    
    # 创建简化存储实例
    storage = SimplifiedStorage()

# FastAPI应用配置
app = FastAPI(
    title="NewsAgent API - Railway部署版",
    description="科技新闻个性化推荐系统 - 基于你的完整功能，支持降级运行",
    version="2.0.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ===========================================
# 📋 修复Pydantic数据模型 (V2兼容)
# ===========================================

class SurveyAnswers(BaseModel):
    """问卷答案数据模型"""
    user_id: str = Field(..., description="用户ID")
    answers: Dict[str, Any] = Field(..., description="问卷答案")
    
    class Config:
        # Pydantic V2 兼容
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "answers": {
                    "技术兴趣": ["ai_ml", "programming", "startup_venture"],
                    "专业背景": "engineer", 
                    "阅读习惯": "summary",
                    "使用场景": ["morning", "evening"],
                    "AI关注程度": 4
                }
            }
        }

class BehaviorEventData(BaseModel):
    """行为事件数据模型"""
    user_id: str = Field(..., description="用户ID")
    action: str = Field(..., description="行为类型")
    news_id: str = Field(..., description="新闻ID")
    news_category: str = Field(..., description="新闻类别")
    news_title: str = Field(default="", description="新闻标题")
    reading_duration: int = Field(default=0, description="阅读时长(秒)")
    scroll_percentage: float = Field(default=0.0, description="滚动百分比")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "action": "read",
                "news_id": "news_001",
                "news_category": "ai_ml",
                "news_title": "OpenAI发布GPT-5技术详解",
                "reading_duration": 120,
                "scroll_percentage": 85.0
            }
        }

class PersonalizedFeedRequest(BaseModel):
    """个性化新闻流请求"""
    user_id: str = Field(..., description="用户ID")
    limit: int = Field(default=20, ge=1, le=50, description="返回新闻数量")
    category_filter: Optional[str] = Field(None, description="类别过滤")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_12345",
                "limit": 20,
                "category_filter": "ai_ml"
            }
        }

# ===========================================
# 🏥 健康检查和调试信息
# ===========================================

@app.get("/")
async def root():
    """Railway健康检查"""
    return {
        "message": "NewsAgent API - Railway部署版",
        "status": "running",
        "version": "2.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "system_mode": "完整系统" if FULL_SYSTEM else "简化模式",
        "docs": "/docs",
        "endpoints": [
            "/health",
            "/api/v2/survey/questions",
            "/api/v2/survey/submit",
            "/api/v2/behavior/track",
            "/api/v2/personalized-feed",
            "/api/v2/news/trending"
        ]
    }

@app.get("/health")
async def health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "railway_env": os.getenv("RAILWAY_ENVIRONMENT"),
            "project": os.getenv("RAILWAY_PROJECT_NAME"),
            "service": os.getenv("RAILWAY_SERVICE_NAME"),
            "port": os.getenv("PORT")
        },
        "system": {
            "full_system_available": FULL_SYSTEM,
            "api_key_configured": bool(os.getenv("GEMINI_API_KEY")),
            "modules_loaded": "完整功能" if FULL_SYSTEM else "基础功能",
            "working_directory": str(Path.cwd()),
            "project_root": str(project_root)
        }
    }

@app.get("/debug")
async def debug_info():
    """调试信息接口"""
    return {
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "project_root": str(project_root),
        "python_path": sys.path[:5],  # 显示前5个路径
        "environment_vars": {
            "PORT": os.getenv("PORT"),
            "RAILWAY_ENVIRONMENT": os.getenv("RAILWAY_ENVIRONMENT"),
            "GEMINI_API_KEY_SET": bool(os.getenv("GEMINI_API_KEY"))
        },
        "full_system": FULL_SYSTEM
    }

# ===========================================
# 📋 你的原有API接口 - 完全兼容版本
# ===========================================

@app.get("/api/v2/survey/questions")
async def get_survey_questions():
    """📋 获取问卷结构API"""
    try:
        if FULL_SYSTEM:
            survey_data = survey_instance.get_survey_for_frontend()
        else:
            survey_data = storage.get_mock_survey_data()
        
        return {
            "success": True,
            "data": survey_data,
            "message": "问卷结构获取成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问卷失败: {str(e)}")

@app.post("/api/v2/survey/submit")
async def submit_survey(survey_data: SurveyAnswers):
    """📋 提交问卷答案API"""
    try:
        user_id = survey_data.user_id
        answers = survey_data.answers
        
        if FULL_SYSTEM:
            # 使用完整系统
            validation = survey_instance.validate_answers(answers)
            if not validation["valid"]:
                raise HTTPException(
                    status_code=400, 
                    detail=f"问卷答案无效: {validation['errors']}"
                )
            
            user_profile = profile_manager.create_profile_from_survey(user_id, answers)
            survey_summary = survey_instance.get_survey_summary(answers)
            rec_profile = profile_manager.get_profile_for_recommendations(user_id)
            initial_recommendations = behavior_system.get_intelligent_recommendations(
                user_id=user_id,
                limit=5
            )
            
            return {
                "success": True,
                "message": "问卷提交成功，用户画像已创建",
                "data": {
                    "user_id": user_id,
                    "profile_created": True,
                    "survey_summary": survey_summary,
                    "interest_weights": rec_profile["interest_weights"],
                    "primary_interests": rec_profile["primary_interests"],
                    "confidence_score": rec_profile["confidence_score"],
                    "initial_recommendations": len(initial_recommendations),
                    "onboarding_completed": True
                }
            }
        else:
            # 简化版本
            interests = answers.get("技术兴趣", ["ai_ml"])
            background = answers.get("专业背景", "engineer")
            
            # 计算基础权重
            weight_per_interest = 1.0 / len(interests) if interests else 0.5
            interest_weights = {}
            all_categories = ["ai_ml", "programming", "web3_crypto", "startup_venture", "hardware_chips", "consumer_tech", "enterprise_saas", "social_media"]
            
            for cat in all_categories:
                if cat in interests:
                    interest_weights[cat] = weight_per_interest
                else:
                    interest_weights[cat] = 0.02  # 最小权重
            
            # 重新归一化
            total = sum(interest_weights.values())
            for cat in interest_weights:
                interest_weights[cat] /= total
            
            profile = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "interests": interests,
                "background": background,
                "confidence_score": 0.3,
                "interest_weights": interest_weights
            }
            
            storage.users[user_id] = profile
            
            return {
                "success": True,
                "message": "问卷提交成功，用户画像已创建",
                "data": {
                    "user_id": user_id,
                    "profile_created": True,
                    "interest_weights": interest_weights,
                    "primary_interests": interests,
                    "confidence_score": 0.3,
                    "onboarding_completed": True
                }
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问卷提交失败: {str(e)}")

@app.post("/api/v2/behavior/track")
async def track_user_behavior(behavior_data: BehaviorEventData):
    """🔄 用户行为追踪API"""
    try:
        if FULL_SYSTEM:
            # 完整系统逻辑
            behavior_event = BehaviorEvent(
                user_id=behavior_data.user_id,
                action=behavior_data.action,
                news_id=behavior_data.news_id,
                news_category=behavior_data.news_category,
                news_title=behavior_data.news_title,
                reading_duration=behavior_data.reading_duration,
                scroll_percentage=behavior_data.scroll_percentage
            )
            
            learning_result = behavior_system.track_behavior(behavior_event)
            
            if not learning_result["success"]:
                raise HTTPException(status_code=400, detail=learning_result.get("error", "行为追踪失败"))
            
            updated_profile = profile_manager.update_profile_from_behavior(
                behavior_data.user_id,
                {
                    "action": learning_result["enhanced_action"],
                    "news_category": behavior_data.news_category,
                    "reading_duration": behavior_data.reading_duration,
                    "engagement_score": learning_result["engagement_score"]
                }
            )
            
            return {
                "success": True,
                "message": "行为追踪成功，画像已更新",
                "data": {
                    "behavior_id": learning_result["behavior_id"],
                    "enhanced_action": learning_result["enhanced_action"],
                    "engagement_score": learning_result["engagement_score"],
                    "user_confidence": learning_result["user_confidence"],
                    "profile_updated": True,
                    "new_confidence": updated_profile.personalization["confidence_score"]
                }
            }
        else:
            # 简化版本
            behavior_id = f"behavior_{uuid.uuid4().hex[:8]}"
            
            if behavior_data.user_id not in storage.behaviors:
                storage.behaviors[behavior_data.user_id] = []
            
            # 计算简单的参与度分数
            engagement_score = 0.1  # 基础分数
            if behavior_data.action == "read" and behavior_data.reading_duration > 60:
                engagement_score = 0.2
            elif behavior_data.action in ["like", "share", "bookmark"]:
                engagement_score = 0.15
            
            behavior_record = {
                "behavior_id": behavior_id,
                "action": behavior_data.action,
                "news_id": behavior_data.news_id,
                "news_category": behavior_data.news_category,
                "engagement_score": engagement_score,
                "timestamp": datetime.now().isoformat()
            }
            
            storage.behaviors[behavior_data.user_id].append(behavior_record)
            
            return {
                "success": True,
                "message": "行为追踪成功",
                "data": {
                    "behavior_id": behavior_id,
                    "enhanced_action": behavior_data.action,
                    "engagement_score": engagement_score,
                    "profile_updated": True
                }
            }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"行为追踪失败: {str(e)}")

@app.post("/api/v2/personalized-feed")
async def get_personalized_feed(request: PersonalizedFeedRequest):
    """🎯 个性化新闻流API"""
    try:
        user_id = request.user_id
        limit = request.limit
        
        if FULL_SYSTEM:
            # 完整系统推荐
            rec_profile = profile_manager.get_profile_for_recommendations(user_id)
            recommendations = behavior_system.get_intelligent_recommendations(
                user_id=user_id,
                limit=limit
            )
            
            if request.category_filter:
                recommendations = [
                    rec for rec in recommendations 
                    if rec.get("category") == request.category_filter
                ]
            
            reading_pref = rec_profile.get("reading_preference", "summary")
            formatted_feed = []
            
            for rec in recommendations:
                formatted_item = {
                    "id": rec.get("id"),
                    "title": rec.get("title"),
                    "category": rec.get("category"),
                    "source": rec.get("source"),
                    "publish_time": rec.get("publish_time"),
                    "url": rec.get("url"),
                    "hot_score": rec.get("hot_score", 0),
                    "personalized_score": rec.get("personalized_score", 0),
                    "image_url": rec.get("image_url", "")
                }
                
                if reading_pref == "summary":
                    formatted_item["content"] = rec.get("summary", "")[:200] + "..."
                elif reading_pref == "deep":
                    formatted_item["content"] = rec.get("content", "")
                else:
                    formatted_item["content"] = rec.get("summary", "")
                
                formatted_feed.append(formatted_item)
            
            explanation = {
                "summary": f"基于你的兴趣推荐了{len(formatted_feed)}条新闻",
                "confidence_level": "高" if rec_profile.get("confidence_score", 0) > 0.7 else "中"
            }
            
            return {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "total_recommendations": len(formatted_feed),
                    "recommendations": formatted_feed,
                    "user_profile": {
                        "primary_interests": rec_profile["primary_interests"],
                        "confidence_score": rec_profile["confidence_score"],
                        "reading_preference": rec_profile["reading_preference"]
                    },
                    "explanation": explanation,
                    "last_updated": datetime.now().isoformat()
                }
            }
        else:
            # 简化版本推荐
            news_data = storage.get_mock_news_data()
            user_profile = storage.users.get(user_id, {})
            user_interests = user_profile.get("interests", ["ai_ml", "programming"])
            
            # 简单的个性化算法
            recommendations = []
            for news in news_data:
                # 基础分数
                score = news["hot_score"] * 0.5
                
                # 兴趣匹配加分
                if news["category"] in user_interests:
                    score += 0.3
                
                # 类别过滤
                if request.category_filter and news["category"] != request.category_filter:
                    continue
                
                news_copy = news.copy()
                news_copy["personalized_score"] = round(score, 3)
                
                # 根据阅读偏好调整内容
                news_copy["content"] = news["summary"][:200] + "..."
                
                recommendations.append(news_copy)
            
            # 按个性化分数排序
            recommendations.sort(key=lambda x: x["personalized_score"], reverse=True)
            
            return {
                "success": True,
                "data": {
                    "user_id": user_id,
                    "total_recommendations": len(recommendations[:limit]),
                    "recommendations": recommendations[:limit],
                    "user_profile": {
                        "primary_interests": user_interests,
                        "confidence_score": user_profile.get("confidence_score", 0.3),
                        "reading_preference": "summary"
                    },
                    "explanation": {
                        "summary": f"基于你对{', '.join(user_interests)}的兴趣，推荐了{len(recommendations[:limit])}条新闻",
                        "confidence_level": "中"
                    },
                    "last_updated": datetime.now().isoformat()
                }
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取个性化推荐失败: {str(e)}")

@app.get("/api/v2/news/trending")
async def get_trending_news(limit: int = 20, category: Optional[str] = None):
    """🔥 获取热门新闻API"""
    try:
        if FULL_SYSTEM:
            if category:
                trending_news = recommendation_engine.data_adapter.get_news_by_category(category, limit)
            else:
                all_news = recommendation_engine.data_adapter.get_news_data()
                trending_news = sorted(all_news, key=lambda x: x.get("hot_score", 0), reverse=True)[:limit]
        else:
            trending_news = storage.get_mock_news_data()
            if category:
                trending_news = [news for news in trending_news if news["category"] == category]
            trending_news.sort(key=lambda x: x.get("hot_score", 0), reverse=True)
            trending_news = trending_news[:limit]
        
        return {
            "success": True,
            "data": {
                "total_news": len(trending_news),
                "news": trending_news,
                "category": category or "all",
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取热门新闻失败: {str(e)}")

@app.get("/api/v2/system/stats")
async def get_system_statistics():
    """📊 系统统计API"""
    try:
        if FULL_SYSTEM:
            profile_stats = profile_manager.get_all_profiles_summary()
            behavior_stats = behavior_system.get_system_statistics()
            cache_stats = recommendation_engine.get_cache_statistics()
            
            return {
                "success": True,
                "data": {
                    "profiles": profile_stats,
                    "behavior_learning": behavior_stats,
                    "recommendation_cache": cache_stats,
                    "system_health": "healthy",
                    "system_mode": "完整功能",
                    "last_updated": datetime.now().isoformat()
                }
            }
        else:
            return {
                "success": True,
                "data": {
                    "total_users": len(storage.users),
                    "total_behaviors": sum(len(behaviors) for behaviors in storage.behaviors.values()),
                    "system_health": "healthy",
                    "system_mode": "简化模式",
                    "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
                    "last_updated": datetime.now().isoformat()
                }
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统统计失败: {str(e)}")

# ===========================================
# 🚀 Railway启动配置
# ===========================================

if __name__ == "__main__":
    import uvicorn
    
    config = get_railway_config()
    
    print(f"🚂 启动NewsAgent API - Railway部署版 (修复版)")
    print(f"🌐 主机: {config['host']}")
    print(f"🎯 端口: {config['port']}")
    print(f"📖 API文档: http://localhost:{config['port']}/docs")
    print(f"🏥 健康检查: http://localhost:{config['port']}/health")
    print(f"🔍 调试信息: http://localhost:{config['port']}/debug")
    print(f"⚙️  系统模式: {'完整功能' if FULL_SYSTEM else '简化模式'}")
    
    if not FULL_SYSTEM:
        print("💡 要启用完整功能，请确保:")
        print("   1. models/ 目录在项目根目录")
        print("   2. 所有依赖模块已安装")
        print("   3. 从项目根目录运行")
    
    uvicorn.run(
        app,
        host=config["host"],
        port=config["port"],
        log_level="info",
        access_log=True
    )