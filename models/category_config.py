# category_config.py - Unified news classification configuration

# News category definitions
CATEGORIES = {
    "ai_ml": "Artificial Intelligence/Machine Learning",
    "programming": "Programming/Software Engineering", 
    "web3_crypto": "Blockchain/Cryptocurrency/Web3",
    "startup_venture": "Startup/Venture Investment",
    "hardware_chips": "Hardware/Semiconductor",
    "consumer_tech": "Consumer Electronics/Digital Products",
    "enterprise_saas": "Enterprise Services/SaaS/Cloud Computing",
    "social_media": "Social Media/Content Platforms"
}

# Detailed keyword library - for keyword classification and Gemini fallback
CATEGORY_KEYWORDS = {
    "ai_ml": [
        # Core AI/ML terms
        "ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural network", "neural networks",
        "transformer", "attention mechanism", "generative ai", "artificial general intelligence", "agi",
        
        # Major AI models and companies
        "chatgpt", "gpt", "gpt-3", "gpt-4", "gpt-5", "claude", "gemini", "bard", "llama", "alpaca",
        "openai", "anthropic", "deepmind", "stability ai", "midjourney", "runway", "character.ai",
        
        # AI applications and concepts
        "llm", "large language model", "foundation model", "diffusion model", "computer vision", "cv",
        "natural language processing", "nlp", "speech recognition", "text-to-speech", "tts",
        "image generation", "text-to-image", "dall-e", "stable diffusion", "ai agent", "autonomous agent",
        "reinforcement learning", "supervised learning", "unsupervised learning", "transfer learning",
        "fine-tuning", "prompt engineering", "rag", "retrieval augmented generation", "embedding",
        "vector database", "ai safety", "alignment", "bias", "hallucination", "ai ethics",
        
        # Technical AI terms
        "pytorch", "tensorflow", "hugging face", "langchain", "vectorization", "tokenization",
        "backpropagation", "gradient descent", "convolutional", "recurrent", "lstm", "gru",
        "autoencoder", "gan", "generative adversarial network", "reinforcement", "q-learning",
        "multimodal", "cross-modal", "zero-shot", "few-shot", "in-context learning"
    ],
    
    "startup_venture": [
        # Funding and investment
        "startup", "funding", "investment", "venture capital", "vc", "angel investment", "angel investor",
        "seed funding", "pre-seed", "series a", "series b", "series c", "series d", "bridge round",
        "convertible note", "safe", "equity", "valuation", "pre-money", "post-money", "dilution",
        "liquidation preference", "anti-dilution", "down round", "flat round", "up round",
        
        # Exit strategies
        "ipo", "initial public offering", "spac", "acquisition", "merger", "exit", "buyout",
        "strategic acquisition", "acqui-hire", "public offering", "direct listing",
        
        # Startup ecosystem
        "unicorn", "decacorn", "hectocorn", "soonicorn", "startup unicorn", "billion dollar startup",
        "yc", "ycombinator", "y combinator", "techstars", "500 startups", "accelerator", "incubator",
        "demo day", "pitch deck", "term sheet", "due diligence", "cap table", "vesting",
        
        # Business metrics and growth
        "mvp", "minimum viable product", "product market fit", "pmf", "traction", "runway",
        "burn rate", "monthly recurring revenue", "mrr", "annual recurring revenue", "arr",
        "customer acquisition cost", "cac", "lifetime value", "ltv", "churn rate", "gross margin",
        "unit economics", "growth hacking", "viral coefficient", "network effect",
        
        # Entrepreneurship
        "founder", "co-founder", "entrepreneurship", "bootstrapping", "lean startup", "pivot",
        "stealth mode", "product launch", "go-to-market", "gtm", "business model", "revenue model",
        "freemium", "saas metrics", "b2b", "b2c", "b2b2c", "marketplace", "platform business"
    ],
    
    "web3_crypto": [
        # Core blockchain and crypto
        "blockchain", "bitcoin", "btc", "ethereum", "eth", "cryptocurrency", "crypto", "digital currency",
        "altcoin", "stablecoin", "memecoin", "shitcoin", "satoshi", "wei", "gwei",
        
        # Major cryptocurrencies
        "solana", "sol", "cardano", "ada", "polygon", "matic", "avalanche", "avax", "chainlink", "link",
        "polkadot", "dot", "binance coin", "bnb", "ripple", "xrp", "dogecoin", "doge", "shiba inu", "shib",
        "litecoin", "ltc", "bitcoin cash", "bch", "monero", "xmr", "tether", "usdt", "usdc", "dai",
        
        # DeFi (Decentralized Finance)
        "defi", "decentralized finance", "yield farming", "liquidity mining", "liquidity pool",
        "automated market maker", "amm", "dex", "decentralized exchange", "uniswap", "sushiswap",
        "compound", "aave", "makerdao", "curve", "balancer", "pancakeswap", "1inch",
        "flash loan", "impermanent loss", "slippage", "arbitrage", "governance token",
        
        # NFTs and Digital Assets
        "nft", "non-fungible token", "opensea", "rarible", "superrare", "foundation", "async art",
        "cryptopunks", "bored ape", "bayc", "pfp", "avatar", "digital art", "collectible",
        "metadata", "ipfs", "royalty", "mint", "drop", "floor price", "blue chip nft",
        
        # Web3 and Metaverse
        "web3", "web 3.0", "metaverse", "virtual world", "virtual reality", "vr", "augmented reality", "ar",
        "mixed reality", "mr", "digital twin", "avatar", "virtual land", "sandbox", "decentraland",
        "axie infinity", "play-to-earn", "p2e", "gamefi", "blockchain gaming",
        
        # Technical blockchain terms
        "smart contract", "dapp", "decentralized application", "dao", "decentralized autonomous organization",
        "consensus", "proof of work", "pow", "proof of stake", "pos", "mining", "staking", "validator",
        "node", "full node", "light node", "hash", "hash rate", "merkle tree", "block height",
        "transaction fee", "gas", "gas fee", "layer 1", "layer 2", "l1", "l2", "scaling solution",
        "sidechain", "rollup", "optimistic rollup", "zk-rollup", "zero knowledge", "zk-snark", "zk-stark",
        
        # Trading and exchanges
        "hodl", "diamond hands", "paper hands", "whale", "pump", "dump", "rug pull", "exit scam",
        "to the moon", "lambo", "fud", "fomo", "dyor", "centralized exchange", "cex", "coinbase",
        "binance", "kraken", "ftx", "kucoin", "huobi", "okex", "cold wallet", "hot wallet",
        "hardware wallet", "ledger", "trezor", "metamask", "walletconnect", "seed phrase", "private key"
    ],
    
    "programming": [
        # Programming languages
        "programming", "coding", "software development", "code", "developer", "software engineer",
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "swift",
        "kotlin", "php", "ruby", "scala", "clojure", "haskell", "erlang", "elixir", "dart", "r",
        "matlab", "julia", "perl", "bash", "shell scripting", "powershell", "lua", "assembly",
        
        # Web development
        "frontend", "backend", "full-stack", "web development", "html", "css", "sass", "scss", "less",
        "react", "reactjs", "vue", "vuejs", "angular", "angularjs", "svelte", "nextjs", "nuxtjs",
        "express", "nodejs", "node.js", "deno", "bun", "django", "flask", "fastapi", "spring boot",
        "laravel", "symfony", "rails", "ruby on rails", "asp.net", "blazor",
        
        # Mobile development
        "mobile development", "ios development", "android development", "react native", "flutter",
        "xamarin", "ionic", "cordova", "phonegap", "swift ui", "jetpack compose", "kotlin multiplatform",
        
        # Databases and data
        "database", "sql", "nosql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "firebase", "supabase", "prisma", "orm", "query optimization",
        "data modeling", "data warehouse", "etl", "data pipeline", "big data", "hadoop", "spark",
        
        # DevOps and infrastructure
        "devops", "ci/cd", "continuous integration", "continuous deployment", "docker", "kubernetes", "k8s",
        "containerization", "microservices", "serverless", "aws", "azure", "gcp", "google cloud",
        "terraform", "ansible", "jenkins", "github actions", "gitlab ci", "circleci", "travis ci",
        "monitoring", "logging", "prometheus", "grafana", "elk stack", "observability",
        
        # Version control and collaboration
        "git", "github", "gitlab", "bitbucket", "version control", "pull request", "merge request",
        "code review", "branching", "gitflow", "open source", "contribution", "maintainer",
        "repository", "commit", "push", "pull", "fork", "clone",
        
        # Software architecture and patterns
        "software architecture", "design patterns", "mvc", "mvvm", "clean architecture", "solid principles",
        "dry principle", "kiss principle", "microservices", "monolith", "api design", "rest api",
        "graphql", "grpc", "websocket", "event-driven", "pub-sub", "message queue", "caching",
        
        # Testing and quality
        "testing", "unit testing", "integration testing", "e2e testing", "test-driven development", "tdd",
        "behavior-driven development", "bdd", "jest", "mocha", "pytest", "junit", "selenium", "cypress",
        "code quality", "static analysis", "linting", "eslint", "prettier", "sonarqube",
        
        # Emerging technologies
        "edge computing", "webassembly", "wasm", "progressive web app", "pwa", "jamstack",
        "headless cms", "low-code", "no-code", "automation", "rpa", "api-first"
    ],
    
    "hardware_chips": [
        # Processors and chips
        "chip", "processor", "cpu", "central processing unit", "gpu", "graphics processing unit",
        "apu", "accelerated processing unit", "soc", "system on chip", "fpga", "asic",
        "microprocessor", "microcontroller", "embedded processor", "arm processor", "x86", "x64",
        
        # Major chip companies
        "nvidia", "amd", "intel", "qualcomm", "broadcom", "mediatek", "apple silicon", "m1", "m2", "m3", "m4",
        "tsmc", "taiwan semiconductor", "samsung semiconductor", "sk hynix", "micron", "western digital",
        "texas instruments", "analog devices", "infineon", "nxp", "marvell", "xilinx", "altera",
        
        # Semiconductor technology
        "semiconductor", "silicon", "wafer", "fabrication", "fab", "foundry", "lithography", "etching",
        "nanometer", "nm", "process node", "7nm", "5nm", "3nm", "2nm", "1nm", "angstrom",
        "euv", "extreme ultraviolet", "photolithography", "mask", "yield", "defect density",
        
        # Computing architecture
        "architecture", "instruction set", "risc", "cisc", "arm", "x86_64", "risc-v", "mips",
        "pipeline", "superscalar", "out-of-order execution", "branch prediction", "cache", "l1 cache",
        "l2 cache", "l3 cache", "memory hierarchy", "virtual memory", "mmu", "memory management unit",
        
        # Memory technologies
        "memory", "ram", "ddr", "ddr4", "ddr5", "gddr", "hbm", "high bandwidth memory",
        "flash memory", "nand flash", "nor flash", "ssd", "solid state drive", "nvme", "emmc", "ufs",
        "storage", "hard drive", "hdd", "hybrid drive", "optane", "3d xpoint",
        
        # Specialized processors
        "gpu computing", "cuda", "opencl", "tensor processing unit", "tpu", "neural processing unit", "npu",
        "ai accelerator", "ai chip", "machine learning accelerator", "data center gpu", "edge ai",
        "quantum processor", "quantum chip", "quantum computing", "qubit", "quantum supremacy",
        
        # Performance and benchmarks
        "performance", "benchmark", "flops", "teraflops", "petaflops", "tops", "tera operations per second",
        "clock speed", "frequency", "overclocking", "thermal design power", "tdp", "power efficiency",
        "performance per watt", "single-threaded", "multi-threaded", "parallel processing",
        
        # 新兴技术
        "chiplet", "heterogeneous computing", "neuromorphic", "photonic computing", "optical computing",
        "dna computing", "molecular computing", "carbon nanotube", "graphene", "spintronics",
        "memristor", "phase change memory", "pcm", "resistive ram", "rram", "magnetoresistive ram", "mram"
    ],
    
    "consumer_tech": [
        # Mobile devices
        "smartphone", "mobile phone", "iphone", "android", "samsung galaxy", "pixel", "oneplus",
        "xiaomi", "huawei", "oppo", "vivo", "realme", "honor", "nothing phone", "fairphone",
        "foldable phone", "flip phone", "5g phone", "wireless charging", "fast charging", "magsafe",
        
        # Apple ecosystem
        "apple", "ios", "ipad", "macbook", "imac", "mac studio", "mac pro", "apple watch", "airpods",
        "apple tv", "homepod", "airtag", "apple pencil", "magic keyboard", "apple silicon", "m-series",
        "app store", "icloud", "facetime", "siri", "carplay", "apple fitness", "apple music",
        
        # Wearables and health tech
        "smartwatch", "fitness tracker", "apple watch", "galaxy watch", "wear os", "fitbit", "garmin",
        "amazfit", "mi band", "health monitoring", "heart rate", "blood oxygen", "ecg", "sleep tracking",
        "step counter", "smart ring", "oura ring", "smart glasses", "ar glasses", "vr headset",
        
        # Audio and entertainment
        "headphones", "earbuds", "true wireless", "tws", "noise cancellation", "anc", "transparency mode",
        "spatial audio", "hi-res audio", "bluetooth", "wireless audio", "gaming headset", "audiophile",
        "smart speaker", "alexa", "google assistant", "echo", "nest", "sonos", "bose", "sony", "sennheiser",
        
        # Electric vehicles and transportation
        "electric vehicle", "ev", "tesla", "model s", "model 3", "model x", "model y", "cybertruck",
        "rivian", "lucid air", "ford lightning", "gm ultium", "volkswagen id", "bmw ix", "mercedes eqc",
        "autonomous driving", "self-driving", "autopilot", "fsd", "lidar", "radar", "computer vision",
        "charging station", "supercharger", "fast charging", "battery technology", "solid state battery",
        
        # Smart home and IoT
        "smart home", "iot", "internet of things", "smart bulb", "smart switch", "smart thermostat",
        "nest thermostat", "ecobee", "smart lock", "video doorbell", "ring", "nest hello", "security camera",
        "home automation", "alexa", "google home", "siri", "homekit", "smartthings", "zigbee", "z-wave",
        "matter", "thread", "wifi 6", "mesh network", "smart plug", "smart sensor",
        
        # Gaming and VR/AR
        "gaming", "console", "playstation", "ps5", "xbox", "series x", "series s", "nintendo switch",
        "steam deck", "gaming laptop", "gaming desktop", "graphics card", "rtx", "radeon", "ray tracing",
        "virtual reality", "vr", "oculus", "meta quest", "pico", "htc vive", "valve index", "psvr",
        "augmented reality", "ar", "mixed reality", "mr", "hololens", "magic leap", "apple vision pro",
        
        # Computing devices
        "laptop", "ultrabook", "2-in-1", "convertible", "chromebook", "macbook", "surface", "thinkpad",
        "gaming laptop", "tablet", "e-reader", "kindle", "kobo", "smart display", "all-in-one", "mini pc",
        "raspberry pi", "single board computer", "maker board", "arduino", "microcontroller",
        
        # Display technology
        "display", "monitor", "oled", "qled", "mini led", "micro led", "hdr", "4k", "8k", "120hz", "144hz",
        "refresh rate", "response time", "color gamut", "brightness", "contrast ratio", "viewing angle",
        "curved display", "ultrawide", "gaming monitor", "professional monitor", "color accuracy"
    ],
    
    "enterprise_saas": [
        # Cloud platforms
        "cloud computing", "saas", "software as a service", "paas", "platform as a service",
        "iaas", "infrastructure as a service", "aws", "amazon web services", "microsoft azure", "azure",
        "google cloud", "gcp", "google cloud platform", "alibaba cloud", "oracle cloud", "ibm cloud",
        "hybrid cloud", "multi-cloud", "public cloud", "private cloud", "edge computing",
        
        # Major enterprise software
        "microsoft", "office 365", "microsoft 365", "teams", "outlook", "sharepoint", "onedrive",
        "power platform", "power bi", "dynamics 365", "windows server", "active directory",
        "salesforce", "crm", "customer relationship management", "hubspot", "pipedrive", "zendesk",
        "servicenow", "jira", "confluence", "atlassian", "slack", "discord", "zoom", "webex",
        
        # Productivity and collaboration
        "collaboration", "productivity", "project management", "task management", "workflow",
        "notion", "obsidian", "roam research", "airtable", "monday.com", "asana", "trello", "clickup",
        "basecamp", "wrike", "smartsheet", "miro", "figma", "canva", "adobe creative cloud",
        "google workspace", "gmail", "google drive", "google docs", "google sheets", "google slides",
        
        # Business intelligence and analytics
        "business intelligence", "bi", "analytics", "data visualization", "dashboard", "reporting",
        "power bi", "tableau", "qlik", "looker", "datastudio", "metabase", "grafana", "elastic",
        "splunk", "datadog", "new relic", "amplitude", "mixpanel", "segment", "snowflake", "databricks",
        
        # Enterprise resource planning
        "erp", "enterprise resource planning", "sap", "oracle", "netsuite", "workday", "peoplesoft",
        "supply chain management", "scm", "inventory management", "procurement", "financial planning",
        "human resources", "hr", "payroll", "talent management", "recruiting", "onboarding",
        
        # Communication and marketing
        "email marketing", "marketing automation", "mailchimp", "constant contact", "campaign monitor",
        "social media management", "hootsuite", "buffer", "sprout social", "content management",
        "cms", "wordpress", "drupal", "webflow", "squarespace", "wix", "shopify", "magento",
        
        # Security and compliance
        "cybersecurity", "information security", "endpoint protection", "antivirus", "firewall",
        "vpn", "zero trust", "identity management", "single sign-on", "sso", "multi-factor authentication",
        "mfa", "privileged access management", "pam", "security monitoring", "siem", "compliance",
        "gdpr", "hipaa", "sox", "pci dss", "data privacy", "encryption", "backup", "disaster recovery",
        
        # Development and IT operations
        "devops", "continuous integration", "continuous deployment", "ci/cd", "containerization",
        "docker", "kubernetes", "microservices", "api management", "monitoring", "logging",
        "infrastructure monitoring", "application performance monitoring", "apm", "incident management",
        "change management", "configuration management", "automation", "orchestration",
        
        # Emerging enterprise tech
        "robotic process automation", "rpa", "intelligent automation", "low-code", "no-code",
        "citizen development", "digital transformation", "digital workplace", "remote work",
        "hybrid work", "employee experience", "customer experience", "cx", "digital adoption"
    ],
    
    "social_media": [
        # Major platforms
        "social media", "social network", "social platform", "facebook", "meta", "instagram",
        "twitter", "x", "linkedin", "tiktok", "youtube", "snapchat", "pinterest", "reddit",
        "discord", "telegram", "whatsapp", "wechat", "line", "kakao talk", "clubhouse", "mastodon",
        
        # Content creation and streaming
        "content creation", "content creator", "influencer", "social media influencer", "youtuber",
        "tiktoker", "instagrammer", "streamer", "live streaming", "twitch", "youtube live",
        "facebook live", "instagram live", "tiktok live", "podcast", "podcasting", "spotify",
        "apple podcasts", "google podcasts", "anchor", "substack", "medium", "ghost", "wordpress",
        
        # Social commerce and monetization
        "social commerce", "social shopping", "influencer marketing", "affiliate marketing",
        "sponsored content", "brand partnership", "monetization", "creator economy", "creator fund",
        "patreon", "onlyfans", "ko-fi", "buy me a coffee", "gumroad", "etsy", "depop", "poshmark",
        "facebook marketplace", "instagram shopping", "tiktok shop", "pinterest shopping",
        
        # Features and functionality
        "feed", "timeline", "stories", "reels", "shorts", "igtv", "live video", "video call",
        "voice chat", "group chat", "direct message", "dm", "hashtag", "trending", "viral",
        "algorithm", "recommendation", "personalization", "engagement", "like", "share", "comment",
        "follow", "unfollow", "block", "mute", "report", "verification", "blue check", "premium",
        
        # Social media marketing
        "social media marketing", "smm", "social media advertising", "facebook ads", "instagram ads",
        "twitter ads", "linkedin ads", "tiktok ads", "youtube ads", "google ads", "social media analytics",
        "engagement rate", "reach", "impressions", "click-through rate", "ctr", "conversion rate",
        "social listening", "sentiment analysis", "brand monitoring", "crisis management",
        
        # Community and forums
        "community", "online community", "forum", "discussion board", "reddit", "discord server",
        "facebook group", "linkedin group", "subreddit", "moderator", "admin", "user-generated content",
        "ugc", "crowdsourcing", "collaboration", "wiki", "knowledge base", "q&a", "stack overflow",
        
        # Privacy and safety
        "privacy", "data privacy", "privacy settings", "content moderation", "community guidelines",
        "terms of service", "cyberbullying", "online harassment", "hate speech", "misinformation",
        "fact checking", "content warning", "age restriction", "parental controls", "digital wellbeing",
        "screen time", "social media addiction", "mental health", "fomo", "social comparison",
        
        # Emerging trends
        "metaverse", "virtual reality", "vr", "augmented reality", "ar", "avatar", "digital identity",
        "nft profile picture", "social token", "decentralized social", "web3 social", "creator coin",
        "social audio", "voice social", "ephemeral content", "disappearing messages", "stories format",
        "short-form video", "vertical video", "mobile-first", "generation z", "gen z", "millennial",
        "digital native", "social media literacy", "digital citizenship"
    ]
}

# Simplified keyword library - for Gemini classification semantic matching
CORE_KEYWORDS = {
    "ai_ml": [
        "ai", "artificial intelligence", "machine learning", "chatgpt", "gpt", "gemini", "claude", 
        "neural", "deep learning", "llm", "openai", "anthropic", "computer vision", "nlp"
    ],
    "programming": [
        "programming", "code", "software", "developer", "python", "javascript", "github", 
        "react", "vue", "typescript", "web development", "api", "database"
    ],
    "web3_crypto": [
        "blockchain", "bitcoin", "ethereum", "crypto", "cryptocurrency", "defi", "nft", 
        "web3", "solana", "polygon", "smart contract", "dao"
    ],
    "startup_venture": [
        "startup", "funding", "investment", "vc", "venture capital", "ipo", "unicorn", 
        "series a", "series b", "founder", "entrepreneurship"
    ],
    "hardware_chips": [
        "chip", "processor", "gpu", "cpu", "nvidia", "amd", "semiconductor", "intel", 
        "quantum", "silicon", "tsmc", "ai chip"
    ],
    "consumer_tech": [
        "iphone", "android", "smartphone", "tesla", "apple", "mobile", "device", 
        "samsung", "xiaomi", "electric vehicle", "smartwatch"
    ],
    "enterprise_saas": [
        "saas", "enterprise", "cloud", "aws", "azure", "microsoft", "salesforce", 
        "slack", "notion", "crm", "business intelligence"
    ],
    "social_media": [
        "twitter", "instagram", "tiktok", "youtube", "facebook", "linkedin", 
        "social media", "content creator", "influencer", "streaming"
    ]
}

# Chinese category name mapping
CHINESE_CATEGORIES = {
    "ai_ml": "人工智能",
    "programming": "编程开发", 
    "web3_crypto": "区块链",
    "startup_venture": "创业投资",
    "hardware_chips": "硬件芯片",
    "consumer_tech": "消费科技",
    "enterprise_saas": "企业服务",
    "social_media": "社交媒体"
}

def get_category_display_name(category_key: str, language: str = "zh") -> str:
    """Get category display name"""
    if language == "zh":
        return CHINESE_CATEGORIES.get(category_key, category_key)
    else:
        return CATEGORIES.get(category_key, category_key)

def get_all_categories() -> dict:
    """Get all categories"""
    return CATEGORIES.copy()

def get_category_keywords(category: str, detailed: bool = True) -> list:
    """Get keywords for specified category"""
    if detailed:
        return CATEGORY_KEYWORDS.get(category, [])
    else:
        return CORE_KEYWORDS.get(category, [])