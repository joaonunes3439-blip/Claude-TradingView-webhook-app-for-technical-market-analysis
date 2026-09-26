"""
Configuration and environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
APP_PORT = int(os.getenv("APP_PORT", 8000))
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
WEBHOOK_SECRET = os.getenv("TRADINGVIEW_WEBHOOK_SECRET", None)

# Validation
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY não definida no .env")

print(f"✓ Configuração carregada - Porta: {APP_PORT}, Host: {APP_HOST}")
