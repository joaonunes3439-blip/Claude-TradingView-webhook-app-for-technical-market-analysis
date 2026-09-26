"""
Test script to simulate TradingView webhook
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

TEST_PAYLOADS = [
    {
        "name": "Bitcoin Breakout",
        "payload": {
            "ticker": "BTCUSD",
            "close": 64200.50,
            "strategy": "Breakout",
            "indicator": "EMA 200 + Volume",
            "pattern": "Alta após consolidação",
            "exchange": "BINANCE",
            "timestamp": datetime.now().isoformat(),
            "volume": 25000000
        }
    },
    {
        "name": "Ethereum Reversal",
        "payload": {
            "symbol": "ETHUSD",
            "price": 3520.75,
            "signal": "Reversal",
            "indicators": "RSI divergence + Support hold",
            "setup": "Possível inversão de tendência",
            "exchange": "COINBASE",
            "time": datetime.now().isoformat(),
            "volume": 12000000
        }
    }
]

def test_health():
    print("\n📋 Testando health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def test_webhook(payload, name):
    print(f"\n🎯 Testando webhook: {name}")
    print(f"📤 Enviando payload: {json.dumps(payload, indent=2)}")
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=payload, timeout=30)
        print(f"✓ Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Alerta: {result['alert']['symbol']} @ {result['alert']['price']}")
            print(f"\n📊 ANÁLISE DO CLAUDE:\n{result['analysis']}")
            print("\n" + "="*60)
            return True
        print(f"✗ Erro: {response.text}")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("TESTE DO WEBHOOK - CLAUDE TRADINGVIEW")
    print("="*60)
    if not test_health():
        print("\n✗ Servidor não está disponível em http://localhost:8000")
        print("  Inicie o servidor com: python run.py")
        return
    success_count = 0
    for test in TEST_PAYLOADS:
        if test_webhook(test["payload"], test["name"]):
            success_count += 1
    print(f"\n" + "="*60)
    print(f"📊 RESUMO: {success_count} testes bem-sucedidos")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
