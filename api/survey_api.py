# survey_api.py - TechSum 问卷与画像API系统
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

# 导入我们的核心系统
from models.interest_survey import survey_instance
from models.user_profile import UserProfileManager
from models.enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent
from models.cached_recommendation_engine import CachedRecommendationEngine


# FastAPI应用
app = FastAPI(
    title="TechSum 用户画像与推荐API",
    description="科技新闻个性化推荐系统 - 问卷、画像、推荐一体化API",
    version="1.0.0"
)

# ===========================================
# 🏗️ 系统初始化
# ===========================================

# 初始化核心系统
print("🚀 初始化TechSum API系统...")
recommendation_engine = CachedRecommendationEngine()
behavior_system = EnhancedBehaviorSystem(recommendation_engine, test_mode=False)  # 生产模式
profile_manager = UserProfileManager(survey_instance, behavior_system)
print("✅ TechSum API系统初始化完成")

# ===========================================
# 📋 Pydantic数据模型
# ===========================================

class SurveyAnswers(BaseModel):
    """问卷答案数据模型"""
    user_id: str = Field(..., description="用户ID")
    answers: Dict[str, Any] = Field(..., description="问卷答案")
    
    class Config:
        schema_extra = {
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
        schema_extra = {
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

class UserInterestsUpdate(BaseModel):
    """用户兴趣更新数据模型"""
    interests: Dict[str, float] = Field(..., description="兴趣权重字典")
    
    class Config:
        schema_extra = {
            "example": {
                "interests": {
                    "ai_ml": 0.3,
                    "programming": 0.25,
                    "startup_venture": 0.2,
                    "web3_crypto": 0.15,
                    "hardware_chips": 0.1
                }
            }
        }

class NewsFeedback(BaseModel):
    """新闻反馈数据模型"""
    user_id: str = Field(..., description="用户ID")
    rating: int = Field(..., ge=1, le=5, description="评分1-5")
    feedback: str = Field(default="", description="文字反馈")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_12345",
                "rating": 4,
                "feedback": "内容很有用"
            }
        }

# ===========================================
# 📋 问卷相关API
# ===========================================

@app.get("/api/v2/survey/questions", 
         summary="获取问卷结构",
         description="获取用户兴趣问卷的完整结构，用于前端渲染")
async def get_survey_questions():
    """
    📋 获取问卷结构API
    
    返回：
    - 问卷元数据
    - 所有问题和选项
    - 验证规则
    """
    try:
        survey_data = survey_instance.get_survey_for_frontend()
        return {
            "success": True,
            "data": survey_data,
            "message": "问卷结构获取成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问卷失败: {str(e)}")

@app.post("/api/v2/survey/submit",
          summary="提交问卷答案", 
          description="提交用户问卷答案，创建用户画像")
async def submit_survey(survey_data: SurveyAnswers):
    """
    📋 提交问卷答案API
    
    流程：
    1. 验证答案有效性
    2. 创建用户画像
    3. 生成初始推荐
    4. 返回画像摘要
    """
    try:
        user_id = survey_data.user_id
        answers = survey_data.answers
        
        # 1. 验证答案
        validation = survey_instance.validate_answers(answers)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400, 
                detail=f"问卷答案无效: {validation['errors']}"
            )
        
        # 2. 创建用户画像
        user_profile = profile_manager.create_profile_from_survey(user_id, answers)
        
        # 3. 生成问卷摘要
        survey_summary = survey_instance.get_survey_summary(answers)
        
        # 4. 获取推荐用画像数据
        rec_profile = profile_manager.get_profile_for_recommendations(user_id)
        
        # 5. 生成初始推荐（预览）
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
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"问卷提交失败: {str(e)}")

@app.get("/api/v2/profile/{user_id}",
         summary="获取用户画像",
         description="获取指定用户的完整画像信息")
async def get_user_profile(user_id: str):
    """
    👤 获取用户画像API
    """
    try:
        profile = profile_manager.get_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="用户画像不存在")
        
        # 转换为前端友好格式
        profile_data = profile.to_dict()
        
        # 添加分析数据
        analysis = profile_manager.analyze_profile_evolution(user_id)
        
        return {
            "success": True,
            "data": {
                "profile": profile_data,
                "analysis": analysis,
                "last_updated": profile.updated_at
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户画像失败: {str(e)}")

# ===========================================
# 🔄 行为追踪API
# ===========================================

@app.post("/api/v2/behavior/track",
          summary="追踪用户行为",
          description="记录用户行为，更新用户画像")
async def track_user_behavior(behavior_data: BehaviorEventData):
    """
    🔄 用户行为追踪API
    
    流程：
    1. 创建行为事件
    2. 行为学习系统处理
    3. 更新用户画像
    4. 返回学习结果
    """
    try:
        # 1. 创建行为事件
        behavior_event = BehaviorEvent(
            user_id=behavior_data.user_id,
            action=behavior_data.action,
            news_id=behavior_data.news_id,
            news_category=behavior_data.news_category,
            news_title=behavior_data.news_title,
            reading_duration=behavior_data.reading_duration,
            scroll_percentage=behavior_data.scroll_percentage
        )
        
        # 2. 行为学习处理
        learning_result = behavior_system.track_behavior(behavior_event)
        
        if not learning_result["success"]:
            raise HTTPException(status_code=400, detail=learning_result.get("error", "行为追踪失败"))
        
        # 3. 更新用户画像
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
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"行为追踪失败: {str(e)}")

@app.post("/api/v2/behavior/batch",
          summary="批量行为追踪",
          description="批量记录用户行为，提升性能")
async def track_batch_behaviors(behaviors: List[BehaviorEventData]):
    """
    🚀 批量行为追踪API
    """
    try:
        results = []
        for behavior_data in behaviors:
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
            results.append(learning_result)
        
        successful_count = sum(1 for r in results if r.get("success"))
        
        return {
            "success": True,
            "message": f"批量处理完成，成功{successful_count}/{len(behaviors)}条",
            "data": {
                "total_behaviors": len(behaviors),
                "successful_count": successful_count,
                "failed_count": len(behaviors) - successful_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量行为追踪失败: {str(e)}")

# ===========================================
# 🎯 个性化推荐API 
# ===========================================

@app.post("/api/v2/personalized-feed",
          summary="获取个性化新闻流",
          description="基于用户画像生成个性化新闻推荐")
async def get_personalized_feed(request: PersonalizedFeedRequest):
    """
    🎯 个性化新闻流API - "你的喜好"页面核心API
    
    流程：
    1. 获取用户画像
    2. 生成个性化推荐
    3. 根据阅读偏好格式化
    4. 返回推荐结果
    """
    try:
        user_id = request.user_id
        limit = request.limit
        
        # 1. 获取用户画像
        rec_profile = profile_manager.get_profile_for_recommendations(user_id)
        
        # 2. 生成个性化推荐
        recommendations = behavior_system.get_intelligent_recommendations(
            user_id=user_id,
            limit=limit
        )
        
        # 3. 类别过滤（如果指定）
        if request.category_filter:
            recommendations = [
                rec for rec in recommendations 
                if rec.get("category") == request.category_filter
            ]
        
        # 4. 根据用户阅读偏好格式化
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
            
            # 根据阅读偏好调整内容展示
            if reading_pref == "summary":
                formatted_item["content"] = rec.get("summary", "")[:200] + "..."
            elif reading_pref == "deep":
                formatted_item["content"] = rec.get("content", "")
            else:  # news, opinion
                formatted_item["content"] = rec.get("summary", "")
            
            formatted_feed.append(formatted_item)
        
        # 5. 生成推荐解释
        explanation = _generate_recommendation_explanation(rec_profile, len(formatted_feed))
        
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取个性化推荐失败: {str(e)}")

@app.get("/api/v2/feed/explanation/{user_id}",
         summary="获取推荐解释",
         description="解释为什么推荐这些内容")
async def get_recommendation_explanation(user_id: str):
    """
    💡 推荐解释API
    """
    try:
        rec_profile = profile_manager.get_profile_for_recommendations(user_id)
        explanation = _generate_recommendation_explanation(rec_profile, 10)
        
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "explanation": explanation,
                "interests": rec_profile["primary_interests"],
                "confidence": rec_profile["confidence_score"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取推荐解释失败: {str(e)}")

# ===========================================
# 🔥 热门新闻和通用功能API
# ===========================================

@app.get("/api/v2/news/trending",
         summary="获取热门新闻",
         description="获取热门新闻，用于首页展示")
async def get_trending_news(limit: int = 20, category: Optional[str] = None):
    """
    🔥 获取热门新闻API
    用于首页展示，不需要个性化
    """
    try:
        # 获取热门新闻
        if category:
            trending_news = recommendation_engine.data_adapter.get_news_by_category(category, limit)
        else:
            all_news = recommendation_engine.data_adapter.get_news_data()
            # 按热度排序
            trending_news = sorted(all_news, key=lambda x: x.get("hot_score", 0), reverse=True)[:limit]
        
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

@app.get("/api/v2/search",
         summary="搜索新闻",
         description="搜索新闻内容，支持个性化排序")
async def search_news(query: str, user_id: Optional[str] = None, limit: int = 20):
    """
    搜索新闻API
    如果提供user_id，会进行个性化排序
    """
    try:
        all_news = recommendation_engine.data_adapter.get_news_data()
        
        # 简单的关键词搜索
        search_results = []
        query_lower = query.lower()
        
        for news in all_news:
            title = news.get("title", "").lower()
            summary = news.get("summary", "").lower()
            
            if query_lower in title or query_lower in summary:
                # 计算相关性分数
                relevance_score = 0
                if query_lower in title:
                    relevance_score += 2
                if query_lower in summary:
                    relevance_score += 1
                
                news_copy = news.copy()
                news_copy["relevance_score"] = relevance_score
                search_results.append(news_copy)
        
        # 排序：相关性 + 热度
        search_results.sort(
            key=lambda x: (x["relevance_score"], x.get("hot_score", 0)), 
            reverse=True
        )
        
        # 如果有用户ID，进行个性化调整
        if user_id:
            user_profile = profile_manager.get_profile_for_recommendations(user_id)
            if user_profile:
                # 根据用户兴趣调整排序
                for news in search_results:
                    category = news.get("category", "")
                    if category in user_profile["interest_weights"]:
                        news["relevance_score"] *= (1 + user_profile["interest_weights"][category])
                
                search_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "success": True,
            "total_results": len(search_results),
            "news": search_results[:limit],
            "query": query,
            "personalized": user_id is not None,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# ===========================================
# ⚙️ 用户设置和管理API
# ===========================================

@app.put("/api/v2/profile/{user_id}/interests",
         summary="更新用户兴趣",
         description="用户手动调整兴趣偏好")
async def update_user_interests(user_id: str, interests_data: UserInterestsUpdate):
    """
    🎛️ 更新用户兴趣权重API
    用户可以在设置页面手动调整兴趣偏好
    """
    try:
        interests = interests_data.interests
        
        profile = profile_manager.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="用户画像不存在")
        
        # 验证权重和为1
        total_weight = sum(interests.values())
        if abs(total_weight - 1.0) > 0.01:
            raise HTTPException(status_code=400, detail="兴趣权重总和必须为1")
        
        # 更新兴趣权重
        profile.interest_weights = interests
        profile.updated_at = datetime.now().isoformat()
        
        return {
            "success": True,
            "message": "兴趣偏好更新成功",
            "data": {
                "updated_interests": interests,
                "updated_at": profile.updated_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新兴趣失败: {str(e)}")

@app.get("/api/v2/profile/{user_id}/settings",
         summary="获取用户设置",
         description="获取用户的个人设置信息")
async def get_user_settings(user_id: str):
    """
    ⚙️ 获取用户设置API
    """
    try:
        profile = profile_manager.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        settings = {
            "user_id": user_id,
            "interests": profile.interest_weights,
            "reading_preference": profile.basic_info.get("reading_preference", "summary"),
            "professional_background": profile.basic_info.get("professional_background", "unknown"),
            "usage_scenarios": profile.basic_info.get("usage_scenarios", []),
            "notifications_enabled": True,  # 默认值
            "email_digest": False,  # 默认值
            "last_updated": profile.updated_at
        }
        
        return {
            "success": True,
            "data": settings
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户设置失败: {str(e)}")

@app.post("/api/v2/news/{news_id}/feedback",
          summary="提交新闻反馈",
          description="用户对推荐新闻进行评分反馈")
async def submit_news_feedback(news_id: str, feedback_data: NewsFeedback):
    """
    📝 新闻质量反馈API
    用户可以对推荐的新闻进行评分和反馈
    """
    try:
        user_id = feedback_data.user_id
        rating = feedback_data.rating
        feedback = feedback_data.feedback
        
        # 记录反馈
        feedback_record = {
            "feedback_id": f"feedback_{uuid.uuid4().hex[:8]}",
            "user_id": user_id,
            "news_id": news_id,
            "rating": rating,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        # 这里应该存储到数据库
        # await store_feedback(feedback_record)
        
        # 基于反馈调整推荐 - 转换为行为事件
        if rating <= 2:  # 负面反馈
            # 记录为dislike行为
            behavior_event = BehaviorEvent(
                user_id=user_id,
                action="dislike",
                news_id=news_id,
                news_category="unknown",  # 需要从新闻数据中获取
                news_title="",
                reading_duration=0,
                scroll_percentage=0.0
            )
            behavior_system.track_behavior(behavior_event)
        elif rating >= 4:  # 正面反馈
            # 记录为like行为
            behavior_event = BehaviorEvent(
                user_id=user_id,
                action="like",
                news_id=news_id,
                news_category="unknown",
                news_title="",
                reading_duration=0,
                scroll_percentage=0.0
            )
            behavior_system.track_behavior(behavior_event)
        
        return {
            "success": True,
            "message": "反馈提交成功",
            "data": feedback_record
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交反馈失败: {str(e)}")

# ===========================================
# 📊 系统统计和监控API
# ===========================================

@app.get("/api/v2/system/stats",
         summary="获取系统统计",
         description="获取用户画像系统统计信息")
async def get_system_statistics():
    """
    📊 系统统计API
    """
    try:
        # 用户画像统计
        profile_stats = profile_manager.get_all_profiles_summary()
        
        # 行为学习统计
        behavior_stats = behavior_system.get_system_statistics()
        
        # 推荐引擎统计
        cache_stats = recommendation_engine.get_cache_statistics()
        
        return {
            "success": True,
            "data": {
                "profiles": profile_stats,
                "behavior_learning": behavior_stats,
                "recommendation_cache": cache_stats,
                "system_health": "healthy",
                "last_updated": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统统计失败: {str(e)}")

# ===========================================
# 🔧 辅助函数
# ===========================================

def _generate_recommendation_explanation(rec_profile: Dict[str, Any], count: int) -> Dict[str, Any]:
    """生成推荐解释"""
    primary_interests = rec_profile.get("primary_interests", [])
    confidence = rec_profile.get("confidence_score", 0)
    background = rec_profile.get("professional_background", "unknown")
    
    # 基础解释
    explanation = {
        "summary": f"基于你对{', '.join(primary_interests)}的兴趣，为你推荐了{count}条相关新闻",
        "reasons": [],
        "confidence_level": "高" if confidence > 0.7 else "中" if confidence > 0.4 else "低"
    }
    
    # 详细原因
    if primary_interests:
        explanation["reasons"].append(f"你主要关注 {', '.join(primary_interests)} 领域")
    
    if background != "unknown":
        explanation["reasons"].append(f"结合你的{background}背景进行了调整")
    
    if confidence > 0.7:
        explanation["reasons"].append("基于你的历史阅读行为，推荐准确度较高")
    elif confidence < 0.3:
        explanation["reasons"].append("随着你的使用，推荐会越来越精准")
    
    return explanation

# ===========================================
# 🚀 API启动配置
# ===========================================

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动TechSum API服务器...")
    print("📖 API文档地址: http://localhost:8001/docs")
    print("🎯 问卷API: http://localhost:8001/api/v2/survey/questions")
    print("👤 用户画像: http://localhost:8001/api/v2/profile/{user_id}")
    print("🔄 行为追踪: http://localhost:8001/api/v2/behavior/track")
    print("🎯 个性化推荐: http://localhost:8001/api/v2/personalized-feed")
    print("🔥 热门新闻: http://localhost:8001/api/v2/news/trending")
    
    uvicorn.run(
        "survey_api:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )