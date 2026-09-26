"""
Data models for webhook payloads and responses
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class TradingViewAlert(BaseModel):
    """Base model for TradingView webhook data"""
    ticker: Optional[str] = None
    symbol: Optional[str] = None
    close: Optional[float] = None
    price: Optional[float] = None
    signal: Optional[str] = None
    strategy: Optional[str] = None
    indicators: Optional[str] = None
    indicator: Optional[str] = None
    pattern: Optional[str] = None
    setup: Optional[str] = None
    exchange: Optional[str] = None
    timestamp: Optional[str] = None
    time: Optional[str] = None
    volume: Optional[float] = None
    message: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from TradingView

class NormalizedAlert(BaseModel):
    """Normalized alert data for Claude analysis"""
    symbol: str
    price: str
    signal: str
    indicators: str
    pattern: str
    exchange: str
    timestamp: str
    volume: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    """Response with analysis from Claude"""
    status: str
    alert: NormalizedAlert
    analysis: str
    model: str = "claude-3-5-sonnet-20241022"
    
class ErrorResponse(BaseModel):
    """Error response"""
    status: str = "error"
    message: str
    code: Optional[str] = None
