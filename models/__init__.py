# models/__init__.py
"""
NewsAgent Models Package

This package contains all the core models and data processing components
for the NewsAgent news classification system.
"""

from .category_config import (
    CATEGORIES,
    CATEGORY_KEYWORDS, 
    CORE_KEYWORDS,
    CHINESE_CATEGORIES,
    get_category_display_name,
    get_all_categories,
    get_category_keywords
)

from .gemini_classifier import GeminiNewsClassifier
from .data_adapter import DataAdapter

__all__ = [
    'CATEGORIES',
    'CATEGORY_KEYWORDS',
    'CORE_KEYWORDS', 
    'CHINESE_CATEGORIES',
    'get_category_display_name',
    'get_all_categories',
    'get_category_keywords',
    'GeminiNewsClassifier',
    'DataAdapter'
]

__version__ = '1.0.0'