"""
Entry point to run the FastAPI application
"""
import uvicorn
from app.config import APP_HOST, APP_PORT

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("Claude TradingView Webhook App")
    print(f"{'='*60}")
    print(f"🚀 Starting server on http://{APP_HOST}:{APP_PORT}")
    print(f"📚 Docs available at http://localhost:{APP_PORT}/docs")
    print(f"🧪 Test endpoint at http://localhost:{APP_PORT}/test")
    print(f"{'='*60}\n")
    uvicorn.run(
        "app.main:app",
        host=APP_HOST,
        port=APP_PORT,
        reload=True,
        log_level="info"
    )
