import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Instancia o cliente redirecionando o ponto de acesso (base_url) para o OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)

model_name = os.getenv("OPENAI_MODEL", "meta-llama/llama-3.2-3b-instruct:free")

try:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Você é um assistente prestativo."},
            {"role": "user", "content": "Diga 'Ambiente configurado com sucesso!' em português."}
        ]
    )

    print("\n--- Resposta via OpenRouter ---")
    print(response.choices[0].message.content)
    print("--------------------------------\n")

except Exception as e:
    print(f"\n❌ Erro ao conectar com a API: {e}\n")