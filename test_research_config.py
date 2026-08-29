from app.core.config import get_settings

settings = get_settings()

print("Google API key configured:", bool(settings.google_api_key))
print("Tavily API key configured:", bool(settings.tavily_api_key))
