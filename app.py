# app.py - NewsAgent主应用入口 (修复版)
"""
NewsAgent 科技新闻个性化推荐系统
安全配置管理版本 - 主入口文件
"""

import sys
import os
import logging
from pathlib import Path

# 🔧 修复：在检查环境之前先加载.env文件
from dotenv import load_dotenv
load_dotenv()  # 加载.env文件

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """检查环境配置"""
    errors = []
    warnings = []
    
    # 🔧 修复：先确保.env文件被加载
    env_file = project_root / ".env"
    if env_file.exists():
        # 重新加载确保最新配置
        load_dotenv(env_file)
        print(f"✅ 已加载环境配置文件: {env_file}")
    else:
        warnings.append(".env 文件不存在，将使用系统环境变量")
    
    # 检查必需的环境变量
    required_env_vars = ["GEMINI_API_KEY"]
    for var in required_env_vars:
        value = os.getenv(var)
        if not value:
            errors.append(f"环境变量 {var} 未设置")
        elif value.startswith("your_"):
            errors.append(f"环境变量 {var} 需要设置真实值")
        else:
            # 显示masked版本
            masked = value[:8] + "*" * (len(value) - 12) + value[-4:] if len(value) > 12 else "*" * len(value)
            print(f"✅ {var}: {masked}")
    
    # 检查 .env.example 文件
    env_example = project_root / ".env.example"
    if not env_example.exists():
        warnings.append(".env.example 文件不存在")
    
    # 检查配置文件
    config_file = project_root / "config" / "settings.py"
    if not config_file.exists():
        errors.append("配置文件 config/settings.py 不存在")
    
    return errors, warnings

def main():
    """启动NewsAgent应用"""
    print("🚀 启动NewsAgent科技新闻推荐系统")
    print("=" * 50)
    
    # 1. 环境检查
    print("🔍 检查环境配置...")
    errors, warnings = check_environment()
    
    # 显示警告
    for warning in warnings:
        print(f"⚠️  {warning}")
    
    # 如果有错误，提供详细的解决方案
    if errors:
        print("❌ 环境配置错误:")
        for error in errors:
            print(f"   • {error}")
        
        print("\n💡 详细解决方案:")
        
        # 检查.env文件是否存在
        env_file = project_root / ".env"
        env_example = project_root / ".env.example"
        
        if not env_file.exists():
            if env_example.exists():
                print("   1. 复制环境变量模板:")
                print(f"      cp .env.example .env")
            else:
                print("   1. 创建 .env 文件:")
                print("      echo 'GEMINI_API_KEY=your_api_key_here' > .env")
        
        print("   2. 编辑 .env 文件设置真实的API密钥:")
        print("      nano .env  # 或使用其他编辑器")
        print("   3. API密钥获取地址:")
        print("      https://makersuite.google.com/app/apikey")
        print("   4. 确保密钥格式正确 (以 AIza 开头)")
        
        # 检查配置目录
        config_dir = project_root / "config"
        if not config_dir.exists():
            print("   5. 创建配置目录:")
            print("      mkdir config")
        
        return False
    
    # 2. 导入配置
    try:
        from config.settings import settings
        print("✅ 配置加载成功")
        
        # 显示安全的配置摘要
        config_summary = settings.get_safe_summary()
        print("📊 配置摘要:")
        for key, value in config_summary.items():
            if isinstance(value, bool):
                status = "✅" if value else "❌"
                print(f"   • {key}: {status}")
            else:
                print(f"   • {key}: {value}")
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("\n💡 解决方案:")
        print("   1. 确保 config/settings.py 文件存在")
        print("   2. 检查 .env 文件中的配置是否正确")
        return False
    
    # 3. 导入应用
    try:
        from api.survey_api import app
        print("✅ API应用加载成功")
    except Exception as e:
        print(f"❌ API应用加载失败: {e}")
        print(f"错误详情: {str(e)}")
        return False
    
    # 4. 启动服务器
    print("\n🌐 启动API服务器...")
    print(f"📖 API文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"🔒 安全模式: {'开发' if settings.DEBUG_MODE else '生产'}")
    print(f"🎯 日志级别: {settings.LOG_LEVEL}")
    print("\n按 Ctrl+C 停止服务器")
    
    try:
        import uvicorn
        
        uvicorn.run(
            app,
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=settings.DEBUG_MODE,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=settings.DEBUG_MODE
        )
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        return True
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        return False

def create_env_file():
    """创建示例环境变量文件"""
    env_example_path = project_root / ".env.example"
    env_path = project_root / ".env"
    
    if env_path.exists():
        print("✅ .env 文件已存在")
        return
    
    # 如果没有.env.example，创建一个基本的.env
    if not env_example_path.exists():
        print("📝 创建基本的 .env 文件...")
        basic_env_content = """# NewsAgent 环境变量配置
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./newsagent.db
API_HOST=0.0.0.0
API_PORT=8001
DEBUG_MODE=false
EVENTS_API_BASE_URL=https://techsum-server-production.up.railway.app
LOG_LEVEL=INFO
"""
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(basic_env_content)
        print(f"✅ 已创建 .env 文件: {env_path}")
        print("📝 请编辑其中的 GEMINI_API_KEY")
        return
    
    # 从示例文件复制
    try:
        with open(env_example_path, 'r', encoding='utf-8') as src:
            content = src.read()
        
        with open(env_path, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        print(f"✅ 已从模板创建 .env 文件")
        print(f"📝 请编辑 {env_path} 中的配置")
        
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")

def setup_project():
    """项目初始化设置"""
    print("🔧 NewsAgent项目初始化")
    print("=" * 30)
    
    # 1. 创建必要的目录
    directories = ["config", "logs", "data", "api"]
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ 目录创建: {directory}/")
    
    # 2. 创建环境变量文件
    create_env_file()
    
    # 3. 检查依赖
    print("\n📦 检查依赖包...")
    required_packages = [
        "fastapi", "uvicorn", "python-dotenv", 
        "requests", "pydantic"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n💡 安装缺失的依赖:")
        print(f"pip install {' '.join(missing_packages)}")
    
    print("\n🎉 项目初始化完成!")
    print("📝 下一步:")
    print("   1. 编辑 .env 文件，设置你的 GEMINI_API_KEY")
    print("   2. 运行 python app.py 启动服务")

def quick_test():
    """快速测试配置"""
    print("🧪 快速配置测试")
    print("=" * 20)
    
    # 加载环境变量
    load_dotenv()
    
    # 测试API密钥
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key.startswith("AIza") and len(api_key) > 30:
        masked = api_key[:8] + "*" * 8 + api_key[-4:]
        print(f"✅ API密钥配置正确: {masked}")
    else:
        print("❌ API密钥未正确配置")
        return False
    
    # 测试配置导入
    try:
        from config.settings import settings
        print("✅ 配置模块导入成功")
        
        if settings.validate():
            print("✅ 配置验证通过")
            return True
        else:
            print("❌ 配置验证失败")
            return False
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NewsAgent科技新闻推荐系统")
    parser.add_argument("--setup", action="store_true", help="初始化项目设置")
    parser.add_argument("--check", action="store_true", help="检查环境配置")
    parser.add_argument("--test", action="store_true", help="快速配置测试")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_project()
    elif args.check:
        load_dotenv()  # 确保加载环境变量
        errors, warnings = check_environment()
        print("🔍 环境检查结果:")
        for warning in warnings:
            print(f"⚠️  {warning}")
        for error in errors:
            print(f"❌ {error}")
        if not errors:
            print("✅ 环境配置正常")
    elif args.test:
        quick_test()
    else:
        success = main()
        if not success:
            print("\n💡 尝试运行: python app.py --setup")