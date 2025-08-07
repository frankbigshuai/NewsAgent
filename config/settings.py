# config/settings.py - 安全配置管理
import os
import logging
from typing import Optional, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings:
    """NewsAgent应用配置管理"""
    
    def __init__(self):
        # ===================================
        # API密钥配置
        # ===================================
        self.GEMINI_API_KEY: str = self._get_required_env("GEMINI_API_KEY")
        
        # ===================================
        # 数据库配置
        # ===================================
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./newsagent.db")
        
        # ===================================
        # API服务配置
        # ===================================
        self.API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
        self.API_PORT: int = int(os.getenv("API_PORT", "8001"))
        self.DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
        
        # ===================================
        # 外部API配置
        # ===================================
        self.EVENTS_API_BASE_URL: str = os.getenv(
            "EVENTS_API_BASE_URL", 
            "https://techsum-server-production.up.railway.app"
        )
        
        # ===================================
        # 缓存配置
        # ===================================
        self.CACHE_TTL: int = int(os.getenv("CACHE_TTL", "1800"))
        self.REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
        
        # ===================================
        # 安全配置
        # ===================================
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.ALLOWED_HOSTS: List[str] = os.getenv("ALLOWED_HOSTS", "*").split(",")
        
        # ===================================
        # 日志配置
        # ===================================
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
        
        # 配置验证
        self._validate_config()
        
        # 设置日志
        self._setup_logging()
    
    def _get_required_env(self, key: str) -> str:
        """获取必需的环境变量"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"🔒 环境变量 {key} 是必需的，但未设置。请检查 .env 文件")
        return value
    
    def _validate_config(self) -> None:
        """验证配置完整性"""
        errors = []
        
        # 验证API密钥格式
        if not self.GEMINI_API_KEY.startswith('AIza'):
            errors.append("无效的Gemini API密钥格式")
        
        # 验证端口范围
        if not (1000 <= self.API_PORT <= 65535):
            errors.append(f"无效的API端口: {self.API_PORT}")
        
        # 验证数据库URL
        if not self.DATABASE_URL:
            errors.append("数据库URL不能为空")
        
        if errors:
            raise ValueError(f"配置验证失败:\n" + "\n".join(f"- {error}" for error in errors))
    
    def _setup_logging(self) -> None:
        """设置日志配置"""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        logging_config = {
            'level': getattr(logging, self.LOG_LEVEL.upper()),
            'format': log_format,
        }
        
        if self.LOG_FILE:
            # 确保日志目录存在
            log_dir = os.path.dirname(self.LOG_FILE)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            logging_config['filename'] = self.LOG_FILE
        
        logging.basicConfig(**logging_config)
    
    def validate(self) -> bool:
        """运行时配置验证"""
        try:
            # 检查必需配置
            required_configs = [
                self.GEMINI_API_KEY,
                self.DATABASE_URL,
            ]
            
            for config in required_configs:
                if not config:
                    return False
            
            return True
        except Exception as e:
            logging.error(f"配置验证失败: {e}")
            return False
    
    def get_safe_summary(self) -> dict:
        """获取安全的配置摘要（隐藏敏感信息）"""
        return {
            "api_host": self.API_HOST,
            "api_port": self.API_PORT,
            "debug_mode": self.DEBUG_MODE,
            "database_type": "sqlite" if "sqlite" in self.DATABASE_URL else "other",
            "events_api_configured": bool(self.EVENTS_API_BASE_URL),
            "redis_configured": bool(self.REDIS_URL),
            "gemini_api_configured": bool(self.GEMINI_API_KEY),
            "log_level": self.LOG_LEVEL
        }

# 创建全局配置实例
try:
    settings = Settings()
    logging.info("✅ NewsAgent配置加载成功")
    logging.info(f"📊 配置摘要: {settings.get_safe_summary()}")
except Exception as e:
    logging.error(f"❌ NewsAgent配置加载失败: {e}")
    raise

# 配置最终验证
if not settings.validate():
    raise RuntimeError("🔒 配置验证失败，请检查环境变量设置")