import os
import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from docling.document_converter import DocumentConverter

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
    raise ValueError("❌ Chave de API não encontrada no arquivo .env!")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)

# 1. NOVO MODELO EXPANDIDO AQUI
class MetadadosArtigoCompleto(BaseModel):
    # Campos básicos (Tarefa 2)
    titulo: str = Field(description="Título exato e completo do trabalho")
    autores: List[str] = Field(description="Lista com os nomes dos autores")
    ano: int = Field(description="Ano de publicação (4 dígitos)")
    
    # Campos complementares
    resumo: str = Field(description="Breve resumo ou abstract do artigo")
    palavras_chave: List[str] = Field(description="Lista de palavras-chave do documento")
    area_conhecimento: str = Field(description="Área principal do conhecimento (ex: IA, Sociologia, Bioética)")
    metodologia: str = Field(description="Tipo de estudo (estudo de caso, revisão teórica, etc.)")
    principais_conclusoes: List[str] = Field(description="Lista com 2 a 3 conclusões principais do trabalho")


# 2. Função de extração atualizada
def extrair_metadados(caminho_ou_conteudo: str) -> dict:
    p = Path(caminho_ou_conteudo)
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            conteudo = f.read()
    else:
        conteudo = caminho_ou_conteudo

    # Prompt atualizado para orientar a extração completa
    prompt_sistema = (
        "Você é um assistente acadêmico especialista em extração de dados. "
        "Analise o texto fornecido e extraia todos os metadados solicitados. "
        "Responda EXCLUSIVAMENTE em formato JSON respeitando a seguinte estrutura:\n"
        "{\n"
        '  "titulo": "string",\n'
        '  "autores": ["string"],\n'
        '  "ano": 2024,\n'
        '  "resumo": "string",\n'
        '  "palavras_chave": ["string"],\n'
        '  "area_conhecimento": "string",\n'
        '  "metodologia": "string",\n'
        '  "principais_conclusoes": ["string"]\n'
        "}"
    )

    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "google/gemini-2.5-flash"),
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Texto do documento:\n\n{conteudo[:4000]}"}
        ],
        response_format={"type": "json_object"}
    )

    # Validação do JSON com a nova classe Pydantic
    dados_brutos = json.loads(completion.choices[0].message.content)
    metadados_validados = MetadadosArtigoCompleto(**dados_brutos)
    
    return metadados_validados.model_dump()


if __name__ == "__main__":
    arquivos_md = [
        "artigo_twitter.md",
        "escrita_academica.md",
        "bioetica_ia.md",
        "instruct_gpt.pdf"
    ]
    resultados = []

    for nome_arquivo in arquivos_md:
        caminho_completo = diretorio_aula / nome_arquivo
        
        if caminho_completo.exists():
            print(f"⏳ Processando metadados completos de {nome_arquivo}...")
            metadados = extrair_metadados(str(caminho_completo))
            resultados.append(metadados)
            
            print(json.dumps(metadados, indent=2, ensure_ascii=False))
            print("-" * 50)
        else:
            print(f"⚠️ Arquivo {nome_arquivo} não encontrado na pasta AULA_02.")

    caminho_saida_json = diretorio_aula / "metadados_consolidados.json"
    with open(caminho_saida_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
        
    print(f"\n✅ Metadados salvos em: {caminho_saida_json.name}")