import os
import json
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

# Garante a busca do arquivo .env na raiz do projeto
diretorio_aula = Path(__file__).parent
raiz_projeto = diretorio_aula.parent
caminho_env = raiz_projeto / ".env"

if caminho_env.exists():
    load_dotenv(caminho_env)
else:
    load_dotenv()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "❌ Chave de API não encontrada no arquivo .env!"
    )

# Configurado para OpenRouter com base no seu .env
client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)

# 1. Esquema Pydantic para Structured Output
class MetadadosArtigo(BaseModel):
    titulo: str = Field(description="Título principal e completo do trabalho")
    autores: List[str] = Field(description="Lista com os nomes dos autores do trabalho")
    ano: int = Field(description="Ano de publicação (4 dígitos inteiros)")

# 2. Função de extração
def extrair_metadados(caminho_ou_conteudo: str) -> dict:
    p = Path(caminho_ou_conteudo)
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            conteudo = f.read()
    else:
        conteudo = caminho_ou_conteudo

    # Chamada de Structured Output usando o formato de resposta estrito
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "google/gemini-2.5-flash"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente acadêmico. Extraia os metadados do texto fornecido "
                    "e responda EXCLUSIVAMENTE em formato JSON no schema:\n"
                    '{"titulo": "string", "autores": ["string"], "ano": 2024}'
                )
            },
            {
                "role": "user",
                "content": f"Extraia o título, autores e ano do texto:\n\n{conteudo[:3000]}"
            }
        ],
        response_format={"type": "json_object"}
    )

    # Converte o retorno em JSON e valida com o modelo Pydantic
    dados_brutos = json.loads(completion.choices[0].message.content)
    metadados_validados = MetadadosArtigo(**dados_brutos)
    
    return metadados_validados.model_dump()


if __name__ == "__main__":
    # Nomes exatos dos seus arquivos .md na pasta AULA_02
    arquivos_md = [
        "artigo_twitter.md",
        "escrita_academica.md",
        "bioetica_ia.md"
    ]
    resultados = []

    for nome_arquivo in arquivos_md:
        caminho_completo = diretorio_aula / nome_arquivo
        
        if caminho_completo.exists():
            print(f"⏳ Processando {nome_arquivo}...")
            metadados = extrair_metadados(str(caminho_completo))
            resultados.append(metadados)
            
            print(json.dumps(metadados, indent=2, ensure_ascii=False))
            print("-" * 40)
        else:
            print(f"⚠️ Arquivo {nome_arquivo} não encontrado na pasta AULA_02.")

    caminho_saida_json = diretorio_aula / "metadados_consolidados.json"
    with open(caminho_saida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Metadados salvos com sucesso em: {caminho_saida_json.name}")