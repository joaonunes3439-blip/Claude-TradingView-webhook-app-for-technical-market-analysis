"""
FastAPI application - TradingView webhook handler
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import APP_HOST, APP_PORT
from app.models import AnalysisResponse
from app.alert_parser import normalize_alert
from app.claude_client import analyze_market, analyze_market_with_context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Claude TradingView Webhook",
    description="Analyze TradingView alerts with Claude AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Claude TradingView Webhook API running",
        "version": "1.0.0"
    }

@app.post("/webhook", tags=["Webhook"])
async def webhook(request: Request):
    """
    Main webhook endpoint for TradingView alerts
    
    Receives TradingView alert data and returns Claude analysis
    """
    try:
        logger.info("Received webhook request")
        payload = await request.json()
        logger.info(f"Payload: {payload}")
        alert = normalize_alert(payload)
        logger.info(f"Alert normalized: {alert.symbol} @ {alert.price}")
        analysis = analyze_market(alert)
        logger.info("Analysis completed successfully")
        response = AnalysisResponse(
            status="success",
            alert=alert,
            analysis=analysis
        )
        return response.model_dump()
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Erro ao processar alerta: {str(e)}",
                "code": "PROCESSING_ERROR"
            }
        )

@app.post("/webhook/with-context", tags=["Webhook"])
async def webhook_with_context(request: Request):
    """
    Webhook endpoint with additional context
    
    Allows sending extra market context for more detailed analysis
    """
    try:
        logger.info("Received webhook request with context")
        payload = await request.json()
        context = payload.pop("context", "")
        alert = normalize_alert(payload)
        analysis = analyze_market_with_context(alert, context)
        response = AnalysisResponse(
            status="success",
            alert=alert,
            analysis=analysis
        )
        return response.model_dump()
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Erro ao processar alerta: {str(e)}",
                "code": "PROCESSING_ERROR"
            }
        )

@app.get("/test", tags=["Testing"])
async def test_endpoint():
    """Test endpoint - returns sample webhook payload"""
    return {
        "description": "Envie este payload para /webhook para testar",
        "payload": {
            "ticker": "BTCUSD",
            "close": 64200.50,
            "strategy": "Breakout",
            "indicator": "EMA 200 + Volume",
            "pattern": "Alta após consolidação",
            "exchange": "BINANCE",
            "timestamp": "2026-09-26T15:30:00Z"
        },
        "curl_example": """curl -X POST http://localhost:8000/webhook \\
  -H "Content-Type: application/json" \\
  -d '{
    "ticker": "BTCUSD",
    "close": 64200.50,
    "strategy": "Breakout",
    "indicator": "EMA 200 + Volume",
    "pattern": "Alta após consolidação",
    "exchange": "BINANCE",
    "timestamp": "2026-09-26T15:30:00Z"
  }'"""
    }

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {APP_HOST}:{APP_PORT}")
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
