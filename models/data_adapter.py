import requests
from typing import List, Dict, Optional
from datetime import datetime
import uuid

# Import Gemini classifier
try:
    from .gemini_classifier import GeminiNewsClassifier
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Gemini classifier not available, using keyword classification")

# Import unified configuration
from .category_config import CATEGORIES, CATEGORY_KEYWORDS

# ==============================================
# 📁 data_adapter.py - Events API data adapter with Gemini classification
# ==============================================

class DataAdapter:
    """Events API-based data adapter with intelligent classification"""
    
    def __init__(self):
        # EZ API configuration - Events API only
        self.base_url = "https://techsum-server-production.up.railway.app"
        self.events_endpoint = f"{self.base_url}/techsum/api/v2/events"
        
        # Use unified configuration
        self.categories = CATEGORIES
        self.category_keywords = CATEGORY_KEYWORDS
        
        # Test API connection status
        self.api_status = self._test_events_connection()
        
        # Initialize Gemini classifier
        self.use_gemini = False
        if GEMINI_AVAILABLE:
            try:
                self.gemini_classifier = GeminiNewsClassifier()
                self.use_gemini = True
                print("✅ Gemini classifier initialized successfully")
            except Exception as e:
                print(f"⚠️ Gemini classifier initialization failed: {e}")
                self.use_gemini = False
    
    def _test_events_connection(self) -> bool:
        """Test Events API connection status - 修复版本"""
        try:
            print(f"🔍 Testing Events API: {self.events_endpoint}")
            
            # 增加超时时间，因为API响应需要约2秒
            response = requests.get(self.events_endpoint, timeout=30)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📏 Response Size: {len(response.content)} bytes")
            print(f"⏱️ URL: {self.events_endpoint}")
            
            is_success = response.status_code == 200
            
            if is_success:
                # 检查返回的数据格式
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"✅ Events API connection successful - Got {len(data)} events")
                        # 检查第一个事件的结构
                        first_event = data[0]
                        required_fields = ['group_title', 'group_summary', 'importance']
                        missing_fields = [field for field in required_fields if field not in first_event]
                        
                        if missing_fields:
                            print(f"⚠️ Missing required fields: {missing_fields}")
                            return False
                        else:
                            print(f"✅ Event structure validated - all required fields present")
                            return True
                    else:
                        print(f"⚠️ API returned empty data or wrong format")
                        return False
                except Exception as e:
                    print(f"⚠️ Failed to parse JSON response: {e}")
                    return False
            else:
                print(f"⚠️ Events API response abnormal: {response.status_code}")
                print(f"📄 Error content: {response.text[:200]}")
                return False
            
        except requests.exceptions.Timeout:
            print(f"⏰ Events API timeout (>30s) - server might be slow")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"🔌 Events API connection error: {e}")
            return False
        except Exception as e:
            print(f"❌ Events API connection failed: {e}")
            return False
    
    def get_news_data(self) -> List[Dict]:
        """
        Get news data - fetch from Events API only
        """
        # 重新测试API状态，因为可能之前测试时API还没准备好
        if not self.api_status:
            print("⏳ Retrying Events API connection...")
            self.api_status = self._test_events_connection()
        
        if not self.api_status:
            print("⚠️ Events API unavailable, using Mock data")
            return self.get_mock_data()
        
        try:
            # Get events data with longer timeout
            print("📡 Fetching real events data...")
            response = requests.get(self.events_endpoint, timeout=30)
            
            if response.status_code == 200:
                events_data = response.json()
                print(f"📅 Retrieved {len(events_data)} event groups from Events API")
                
                # Process events data
                processed_news = self._process_events_data(events_data)
                
                # Deduplicate and sort
                unique_news = self._deduplicate_news(processed_news)
                unique_news.sort(key=lambda x: x["hot_score"], reverse=True)
                
                print(f"📰 Processed and got {len(unique_news)} valid news items")
                return unique_news
                
            else:
                print(f"❌ Events API response error: {response.status_code}")
                return self.get_mock_data()
                
        except Exception as e:
            print(f"❌ Failed to get news data: {e}")
            return self.get_mock_data()
    
    def _process_events_data(self, events_data: List[Dict]) -> List[Dict]:
        """
        Process events data, convert to standardized news entries
        """
        processed_news = []
        
        for event_group in events_data:
            try:
                # Extract event group information
                group_title = event_group.get("group_title", "").strip()
                group_summary = event_group.get("group_summary", "").strip()
                importance = event_group.get("importance", 0)
                earliest_published = event_group.get("earliest_published", "")
                articles = event_group.get("articles", [])
                feeds = event_group.get("feeds", [])
                
                if not group_title:
                    continue
                
                # Create main news entry
                main_news = {
                    "id": f"event_{uuid.uuid4().hex[:8]}",
                    "title": group_title,
                    "summary": group_summary,
                    "content": self._build_content_from_articles(articles),
                    "category": self._classify_news_category(group_title, group_summary),
                    "source": "TechSum Events",
                    "publish_time": earliest_published or datetime.now().isoformat(),
                    "url": articles[0].get("link", "") if articles else "",
                    "image_url": "",  # Events API usually doesn't contain images
                    "hot_score": self._calculate_importance_score(importance),
                    "data_source": "ez_events",
                    "article_count": len(articles),
                    "feeds": feeds,
                    "importance": importance
                }
                
                processed_news.append(main_news)
                
                # If event group contains multiple important articles, extract top few as related news
                if len(articles) > 1 and importance > 50:  # Only extract related articles for important events
                    for i, article in enumerate(articles[:3]):  # Extract at most 3 related articles
                        if article.get("title") and article.get("title").strip():
                            article_news = {
                                "id": f"article_{uuid.uuid4().hex[:8]}",
                                "title": article.get("title", "").strip(),
                                "summary": f"From event: {group_title}",
                                "content": "",
                                "category": self._classify_news_category(article.get("title", ""), ""),
                                "source": article.get("feed", "Unknown"),
                                "publish_time": article.get("published", ""),
                                "url": article.get("link", ""),
                                "image_url": "",
                                "hot_score": self._calculate_importance_score(importance) * 0.7,  # Related articles have slightly lower heat
                                "data_source": "ez_events_article",
                                "parent_event": group_title,
                                "importance": importance
                            }
                            processed_news.append(article_news)
                
            except Exception as e:
                print(f"⚠️ Failed to process event group: {e}")
                continue
        
        return processed_news
    
    def _build_content_from_articles(self, articles: List[Dict]) -> str:
        """Build content summary from article list"""
        if not articles:
            return ""
        
        content_parts = []
        for article in articles[:5]:  # Use at most 5 articles
            title = article.get("title", "").strip()
            feed = article.get("feed", "").strip()
            if title:
                content_parts.append(f"• {title} ({feed})")
        
        return "\n".join(content_parts)
    
    def _classify_news_category(self, title: str, summary: str) -> str:
        """
        Intelligent news classification algorithm
        """
        # Use Gemini classification if available
        if self.use_gemini:
            try:
                category = self.gemini_classifier.classify_news(title, summary)
                return category
            except Exception as e:
                print(f"⚠️ Gemini classification failed, fallback to keywords: {e}")
        
        # Fallback to keyword classification
        return self._classify_with_keywords(title, summary)
    
    def _classify_with_keywords(self, title: str, summary: str) -> str:
        """
        Keyword-based news classification (fallback method)
        """
        # Combine title and summary for classification
        text = f"{title} {summary}".lower()
        
        # Calculate match score for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Keywords in title have higher weight
                    if keyword in title.lower():
                        score += 2
                    else:
                        score += 1
            category_scores[category] = score
        
        # Return category with highest score
        if category_scores and max(category_scores.values()) > 0:
            best_category = max(category_scores, key=category_scores.get)
            return best_category
        
        return "programming"  # Default category
    
    def _calculate_importance_score(self, importance: int) -> float:
        """Calculate heat score based on importance"""
        if importance <= 0:
            return 0.3
        
        # importance is usually 0-100 integer, convert to 0.3-1.0 float
        # Use logarithm to make score distribution more reasonable
        import math
        normalized = min(importance / 100.0, 1.0)
        
        # Apply logarithmic transformation to make importance differences more obvious
        log_score = math.log(normalized * 9 + 1) / math.log(10)  # Map [0,1] to [0,1]
        
        # Ensure score is within 0.3-1.0 range
        final_score = 0.3 + (log_score * 0.7)
        
        return max(0.3, min(1.0, final_score))
    
    def _deduplicate_news(self, news_list: List[Dict]) -> List[Dict]:
        """Deduplicate news"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            title = news.get("title", "").strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news
    
    def get_news_by_category(self, category: str, limit: int = 10) -> List[Dict]:
        """
        Get news by category
        """
        all_news = self.get_news_data()
        
        # Filter news of specified category
        category_news = [news for news in all_news if news["category"] == category]
        
        # Sort by heat score
        category_news.sort(key=lambda x: x["hot_score"], reverse=True)
        
        return category_news[:limit]
    
    def get_news_statistics(self) -> Dict:
        """
        Get news statistics
        """
        all_news = self.get_news_data()
        
        if not all_news:
            return {
                "error": "Unable to get news data",
                "api_status": self.api_status,
                "gemini_status": self.use_gemini
            }
        
        # Statistics for each category news count
        category_counts = {}
        importance_distribution = {}
        total_hot_score = 0
        
        for news in all_news:
            category = news["category"]
            importance = news.get("importance", 0)
            
            category_counts[category] = category_counts.get(category, 0) + 1
            total_hot_score += news["hot_score"]
            
            # Importance distribution statistics
            if importance >= 80:
                importance_level = "high"
            elif importance >= 50:
                importance_level = "medium"
            else:
                importance_level = "low"
            
            importance_distribution[importance_level] = importance_distribution.get(importance_level, 0) + 1
        
        # Add Gemini classifier statistics if available
        gemini_stats = {}
        if self.use_gemini:
            gemini_stats = self.gemini_classifier.get_statistics()
        
        return {
            "total_news": len(all_news),
            "category_distribution": category_counts,
            "importance_distribution": importance_distribution,
            "average_hot_score": total_hot_score / len(all_news) if all_news else 0,
            "api_status": self.api_status,
            "gemini_status": self.use_gemini,
            "gemini_stats": gemini_stats,
            "data_source": "events_with_gemini" if self.use_gemini else "events_only",
            "top_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def get_high_importance_news(self, min_importance: int = 70, limit: int = 10) -> List[Dict]:
        """
        Get high importance news
        """
        all_news = self.get_news_data()
        
        # Filter high importance news
        high_importance_news = [
            news for news in all_news 
            if news.get("importance", 0) >= min_importance
        ]
        
        # Sort by importance
        high_importance_news.sort(key=lambda x: x.get("importance", 0), reverse=True)
        
        return high_importance_news[:limit]
    
    def get_recent_news(self, hours: int = 24, limit: int = 10) -> List[Dict]:
        """
        Get recent hours news
        """
        all_news = self.get_news_data()
        
        from datetime import datetime, timedelta
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_news = []
        for news in all_news:
            try:
                publish_time = news.get("publish_time", "")
                if publish_time:
                    pub_time = datetime.fromisoformat(publish_time.replace('Z', ''))
                    if pub_time > cutoff_time:
                        recent_news.append(news)
            except:
                continue
        
        # Sort by time
        recent_news.sort(key=lambda x: x.get("publish_time", ""), reverse=True)
        
        return recent_news[:limit]
    
    def get_mock_data(self) -> List[Dict]:
        """
        Mock data - used when Events API is unavailable
        """
        return [
            {
                "id": "mock_event_1",
                "title": "OpenAI Releases GPT-5 Model with Significantly Enhanced Reasoning Capabilities",
                "summary": "OpenAI officially released GPT-5, showing excellent performance in mathematical reasoning, code generation, and multimodal understanding, with significant improvements over GPT-4 in multiple benchmark tests.",
                "content": "• OpenAI GPT-5 launch event livestream (OpenAI Blog)\n• GPT-5 technical details analysis (TechCrunch)\n• Industry expert commentary on GPT-5 impact (The Verge)",
                "category": "ai_ml",
                "source": "TechSum Events",
                "publish_time": "2025-07-17T10:00:00Z",
                "url": "https://openai.com/gpt-5",
                "image_url": "",
                "hot_score": 0.95,
                "data_source": "mock",
                "article_count": 3,
                "feeds": ["OpenAI Blog", "TechCrunch", "The Verge"],
                "importance": 85
            },
            {
                "id": "mock_event_2",
                "title": "YC Demo Day 2025 Summer Batch Sets Investment Records",
                "summary": "Y Combinator's 2025 Summer Batch Demo Day was held, with 200 startups presenting, total valuation exceeding $10 billion, and AI-related companies accounting for 40%.",
                "content": "• YC Demo Day live coverage (YC Blog)\n• Top 10 companies investors are most interested in (TechCrunch)\n• Demo Day highlight project analysis (VentureBeat)",
                "category": "startup_venture",
                "source": "TechSum Events",
                "publish_time": "2025-07-16T14:30:00Z",
                "url": "https://ycombinator.com/demo-day",
                "image_url": "",
                "hot_score": 0.82,
                "data_source": "mock",
                "article_count": 3,
                "feeds": ["YC Blog", "TechCrunch", "VentureBeat"],
                "importance": 78
            },
            {
                "id": "mock_event_3",
                "title": "GitHub Launches New AI-Assisted Programming Features",
                "summary": "GitHub Copilot upgraded with new code review and automated test generation features, expected to improve developer productivity by 30%.",
                "content": "• GitHub Copilot new features introduction (GitHub Blog)\n• Developer experience report (Stack Overflow)\n• AI programming tools comparison analysis (Developer Tools)",
                "category": "programming",
                "source": "TechSum Events",
                "publish_time": "2025-07-17T08:15:00Z",
                "url": "https://github.com/features/copilot",
                "image_url": "",
                "hot_score": 0.76,
                "data_source": "mock",
                "article_count": 3,
                "feeds": ["GitHub Blog", "Stack Overflow", "Developer Tools"],
                "importance": 72
            },
            {
                "id": "mock_event_4",
                "title": "Bitcoin Price Breaks All-Time High",
                "summary": "Bitcoin price first breaks through $100,000, with institutional investors entering in large numbers, cryptocurrency market cap reaches all-time high.",
                "content": "• Bitcoin price analysis (CoinDesk)\n• Institutional investment trend report (Bloomberg)\n• Crypto market impact analysis (Crypto News)",
                "category": "web3_crypto",
                "source": "TechSum Events",
                "publish_time": "2025-07-17T06:45:00Z",
                "url": "https://coindesk.com/bitcoin-100k",
                "image_url": "",
                "hot_score": 0.88,
                "data_source": "mock",
                "article_count": 3,
                "feeds": ["CoinDesk", "Bloomberg", "Crypto News"],
                "importance": 80
            },
            {
                "id": "mock_event_5",
                "title": "Apple Releases M4 Chip with Significant Performance Improvements",
                "summary": "Apple released M4 chip using 3nm process, CPU performance improved by 25%, GPU performance improved by 30%, power consumption reduced by 20%.",
                "content": "• Apple M4 chip launch event (Apple Newsroom)\n• M4 performance test report (AnandTech)\n• Chip market impact analysis (Semiconductor Industry)",
                "category": "hardware_chips",
                "source": "TechSum Events",
                "publish_time": "2025-07-16T20:00:00Z",
                "url": "https://apple.com/m4-chip",
                "image_url": "",
                "hot_score": 0.79,
                "data_source": "mock",
                "article_count": 3,
                "feeds": ["Apple Newsroom", "AnandTech", "Semiconductor Industry"],
                "importance": 75
            }
        ]