# Claude TradingView Webhook App for Technical Market Analysis

Aplicação FastAPI que recebe alertas técnicos do TradingView e usa Claude AI para gerar análises de mercado profissionais.

## 🎯 Funcionalidades

- ✅ Webhook para receber alertas do TradingView
- ✅ Parsing inteligente de dados técnicos
- ✅ Análise com Claude AI em português
- ✅ Suporte a contexto adicional
- ✅ API RESTful completa com documentação Swagger
- ✅ Logging estruturado
- ✅ Tratamento robusto de erros

## 🚀 Início Rápido

### 1. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com sua chave do Anthropic:

```env
ANTHROPIC_API_KEY=sua_chave_aqui
APP_PORT=8000
APP_HOST=0.0.0.0
```

### 4. Iniciar o servidor

```bash
python run.py
```

### 5. Testar o endpoint

```bash
curl http://localhost:8000/
```

Ou envie um payload de teste:

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "BTCUSD",
    "close": 64200.50,
    "strategy": "Breakout",
    "indicator": "EMA 200 + Volume",
    "pattern": "Alta após consolidação",
    "exchange": "BINANCE",
    "timestamp": "2026-09-26T15:30:00Z"
  }'
```

## 📚 Documentação

Acesse:

```bash
http://localhost:8000/docs
```

## 🔗 Integração com TradingView

Use uma URL do tipo:

```bash
https://seu-ngrok-url.ngrok-free.app/webhook
```

ou em produção:

```bash
https://seu-dominio.com/webhook
```

## 🧪 Teste automatizado

```bash
python test_webhook.py
```

## Estrutura do projeto

```bash
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── alert_parser.py
│   ├── claude_client.py
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── test_webhook.py
└── venv/
```

## Observações

- Para usar Claude, configure a variável `ANTHROPIC_API_KEY` no arquivo `.env`.
- O projeto usa FastAPI e Anthropic SDK.
- O webhook aceita payloads do TradingView e retorna a análise do modelo em português.
