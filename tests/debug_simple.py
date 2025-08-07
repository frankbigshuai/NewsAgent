from enhanced_behavior_system import EnhancedBehaviorSystem, BehaviorEvent

# 创建系统
system = EnhancedBehaviorSystem()

# 创建简单事件
event = BehaviorEvent(
    user_id="debug_user",
    action="read",
    news_id="test_news",
    news_category="ai_ml",
    reading_duration=60,
    scroll_percentage=70.0
)

# 测试追踪
print("🧪 开始简单调试测试...")
result = system.track_behavior(event)
print(f"📊 结果: {result}")