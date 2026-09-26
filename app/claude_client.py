"""
Claude API client for technical market analysis
"""
from anthropic import Anthropic
from app.config import ANTHROPIC_API_KEY
from app.models import NormalizedAlert
from app.alert_parser import format_alert_for_claude

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Você é um analista técnico experiente de mercados financeiros.

Suas responsabilidades:
1. Analisar alertas técnicos do TradingView com profundidade
2. Interpretar indicadores e padrões de preço
3. Fornecer insights acionáveis em português
4. Ser objetivo, profissional e claro
5. Usar linguagem apropriada para traders

Estruture sua análise em seções claras e bem organizadas.
Sempre inclua risco/recompensa quando possível.
Seja conciso mas completo."""

def analyze_market(alert: NormalizedAlert) -> str:
    """
    Analyze TradingView alert using Claude AI
    
    Args:
        alert: Normalized alert data
        
    Returns:
        Analysis text from Claude
    """
    
    # Format alert for the prompt
    formatted_alert = format_alert_for_claude(alert)
    
    # Create user prompt
    user_prompt = f"""{formatted_alert}

Por favor, analise este alerta técnico e forneça uma análise completa seguindo esta estrutura:

1. **INTERPRETAÇÃO TÉCNICA**: O que o sinal/padrão indica?
2. **CONTEXTO DE MERCADO**: Em que contexto este sinal ocorre?
3. **RISCO/OPORTUNIDADE**: Qual é o risco e qual é a oportunidade?
4. **PRÓXIMOS NÍVEIS**: Onde fica a resistência/suporte?
5. **RECOMENDAÇÃO**: Qual a ação recomendada?
6. **OBSERVAÇÕES IMPORTANTES**: Pontos críticos a considerar

Seja claro, profissional e acionável."""

    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Extract and return analysis
        analysis = response.content[0].text
        return analysis
        
    except Exception as e:
        raise Exception(f"Erro ao chamar Claude API: {str(e)}")

def analyze_market_with_context(alert: NormalizedAlert, additional_context: str = "") -> str:
    """
    Analyze market with additional context from user
    
    Args:
        alert: Normalized alert data
        additional_context: Extra information for analysis
        
    Returns:
        Analysis text from Claude
    """
    
    formatted_alert = format_alert_for_claude(alert)
    
    context_section = f"\n\nCONTEXTO ADICIONAL:\n{additional_context}" if additional_context else ""
    
    user_prompt = f"""{formatted_alert}{context_section}

Por favor, analise este alerta técnico considerando o contexto fornecido.

Estruture a resposta em:
1. **INTERPRETAÇÃO TÉCNICA**
2. **CONTEXTO DE MERCADO**
3. **RISCO/OPORTUNIDADE**
4. **PRÓXIMOS NÍVEIS**
5. **RECOMENDAÇÃO**
6. **OBSERVAÇÕES IMPORTANTES**"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        raise Exception(f"Erro ao chamar Claude API: {str(e)}")
