import os
import re
import json
import numpy as np
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 1. Configuração do ambiente e diretórios
diretorio_aula = Path(__file__).parent if "__file__" in locals() else Path.cwd()
pasta_raiz = diretorio_aula.parent if diretorio_aula.name == "AULA_04" else diretorio_aula
load_dotenv(pasta_raiz / ".env")

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)

MODELO_EMBEDDING = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


# 2. Funções de Chunking (10 Estratégias)
def chunk_fixo(texto: str, tamanho: int, overlap: int = 0) -> list[str]:
    chunks = []
    inicio = 0
    passo = tamanho - overlap
    while inicio < len(texto):
        fim = inicio + tamanho
        chunk = texto[inicio:fim].strip()
        if chunk:
            chunks.append(chunk)
        inicio += passo
    return chunks

def chunk_por_paragrafo(texto: str) -> list[str]:
    return [p.strip() for p in texto.split("\n\n") if p.strip()]

def chunk_por_sentencas(texto: str, grupo_tamanho: int = 3) -> list[str]:
    sentencas = re.split(r'(?<=[.!?])\s+', texto)
    sentencas = [s.strip() for s in sentencas if s.strip()]
    return [" ".join(sentencas[i:i + grupo_tamanho]) for i in range(0, len(sentencas), grupo_tamanho)]

def chunk_recursivo(texto: str, tamanho_maximo: int = 500) -> list[str]:
    separadores = ["\n\n", "\n", ". ", " "]
    def dividir(txt: str, sep_idx: int) -> list[str]:
        if len(txt) <= tamanho_maximo or sep_idx >= len(separadores):
            return [txt.strip()] if txt.strip() else []
        sep = separadores[sep_idx]
        partes = txt.split(sep)
        resultado, acumulador = [], ""
        for p in partes:
            item = p + (sep if sep != " " else " ")
            if len(acumulador) + len(item) <= tamanho_maximo:
                acumulador += item
            else:
                if acumulador: resultado.append(acumulador.strip())
                if len(item) > tamanho_maximo: resultado.extend(dividir(item, sep_idx + 1))
                else: acumulador = item
        if acumulador: resultado.append(acumulador.strip())
        return resultado
    return dividir(texto, 0)

def chunk_por_heading_markdown(texto: str) -> list[str]:
    return [s.strip() for s in re.split(r'\n(?=#+\s)', texto) if s.strip()]


# 3. Mapeamento das 10 Estratégias
ESTRATEGIAS = [
    {"test_id": 1, "strategy": "fixed", "chunk_size": 200, "chunk_overlap": 0, "func": lambda t: chunk_fixo(t, 200, 0)},
    {"test_id": 2, "strategy": "fixed", "chunk_size": 500, "chunk_overlap": 0, "func": lambda t: chunk_fixo(t, 500, 0)},
    {"test_id": 3, "strategy": "fixed", "chunk_size": 1000, "chunk_overlap": 0, "func": lambda t: chunk_fixo(t, 1000, 0)},
    {"test_id": 4, "strategy": "fixed", "chunk_size": 2000, "chunk_overlap": 0, "func": lambda t: chunk_fixo(t, 2000, 0)},
    {"test_id": 5, "strategy": "fixed", "chunk_size": 500, "chunk_overlap": 50, "func": lambda t: chunk_fixo(t, 500, 50)},
    {"test_id": 6, "strategy": "fixed", "chunk_size": 500, "chunk_overlap": 200, "func": lambda t: chunk_fixo(t, 500, 200)},
    {"test_id": 7, "strategy": "paragraph", "chunk_size": None, "chunk_overlap": 0, "func": chunk_por_paragrafo},
    {"test_id": 8, "strategy": "sentence_group_3", "chunk_size": None, "chunk_overlap": 0, "func": chunk_por_sentencas},
    {"test_id": 9, "strategy": "recursive", "chunk_size": 500, "chunk_overlap": 0, "func": chunk_recursivo},
    {"test_id": 10, "strategy": "markdown_heading", "chunk_size": None, "chunk_overlap": 0, "func": chunk_por_heading_markdown},
]


def obter_dimensao_embedding(texto_amostra: str) -> int:
    """Obtém a dimensão do vetor retornada pelo modelo."""
    try:
        resposta = client.embeddings.create(model=MODELO_EMBEDDING, input=texto_amostra[:100])
        return len(resposta.data[0].embedding)
    except Exception:
        return 1536  # Valor padrão do text-embedding-3-small


if __name__ == "__main__":
    nome_arquivo = "artigo_twitter.md"
    caminho_md = pasta_raiz / "AULA_02" / nome_arquivo

    if not caminho_md.exists():
        caminho_md = diretorio_aula / nome_arquivo

    if caminho_md.exists():
        with open(caminho_md, "r", encoding="utf-8") as f:
            conteudo = f.read()

        dimensao_emb = obter_dimensao_embedding(conteudo)
        experimentos = []

        print("⏳ Executando os 10 experimentos de chunking...")

        for est in ESTRATEGIAS:
            chunks = est["func"](conteudo)
            num_chunks = len(chunks)
            avg_size = round(float(np.mean([len(c) for c in chunks])), 1) if chunks else 0.0

            experimento_data = {
                "test_id": est["test_id"],
                "strategy": est["strategy"],
                "chunk_size": est["chunk_size"],
                "chunk_overlap": est["chunk_overlap"],
                "num_chunks": num_chunks,
                "avg_chunk_size": avg_size,
                "embedding_dimension": dimensao_emb
            }
            experimentos.append(experimento_data)

        # Monta a estrutura final do JSON
        summary_data = {
            "document": nome_arquivo,
            "experiments": experimentos
        }

        # Salva o resumo comparativo em summary.json
        caminho_saida = diretorio_aula / "summary.json"
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Arquivo '{caminho_saida.name}' gerado com sucesso!")
        print(json.dumps(summary_data, indent=2, ensure_ascii=False))

    else:
        print(f"⚠️ Arquivo {nome_arquivo} não encontrado para processamento.")