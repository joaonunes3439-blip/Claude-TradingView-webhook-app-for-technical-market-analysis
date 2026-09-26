"""
Parse and normalize TradingView webhook alerts
"""
from app.models import TradingViewAlert, NormalizedAlert

def normalize_alert(payload: dict) -> NormalizedAlert:
    """
    Convert raw TradingView payload to normalized alert format
    
    Args:
        payload: Raw JSON from TradingView webhook
        
    Returns:
        NormalizedAlert with standardized fields
    """
    # Parse as TradingViewAlert first
    alert = TradingViewAlert(**payload)
    
    # Extract values with fallbacks
    symbol = alert.ticker or alert.symbol or "N/A"
    price = str(alert.close or alert.price or "N/A")
    signal = alert.signal or alert.strategy or "N/A"
    indicators = alert.indicators or alert.indicator or "N/A"
    pattern = alert.pattern or alert.setup or "N/A"
    exchange = alert.exchange or "N/A"
    timestamp = alert.timestamp or alert.time or "N/A"
    volume = str(alert.volume) if alert.volume else None
    
    return NormalizedAlert(
        symbol=symbol,
        price=price,
        signal=signal,
        indicators=indicators,
        pattern=pattern,
        exchange=exchange,
        timestamp=timestamp,
        volume=volume,
        raw_data=payload
    )

def format_alert_for_claude(alert: NormalizedAlert) -> str:
    """
    Format normalized alert into readable text for Claude prompt
    
    Args:
        alert: NormalizedAlert object
        
    Returns:
        Formatted string for Claude analysis
    """
    volume_info = f"\n- Volume: {alert.volume}" if alert.volume else ""
    
    return f"""
ALERTA TÉCNICO DO TRADINGVIEW:

- **Símbolo/Ativo**: {alert.symbol}
- **Preço Atual**: {alert.price}
- **Tipo de Sinal**: {alert.signal}
- **Indicadores**: {alert.indicators}
- **Padrão/Setup**: {alert.pattern}
- **Exchange/Mercado**: {alert.exchange}
- **Timestamp**: {alert.timestamp}{volume_info}
""".strip()
