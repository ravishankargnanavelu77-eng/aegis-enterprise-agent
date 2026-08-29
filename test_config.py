from app.core.config import get_settings

settings = get_settings()

print("Configuration loaded successfully")
print(f"Model: {settings.gemini_model}")
print(f"API key configured: {bool(settings.google_api_key)}")
