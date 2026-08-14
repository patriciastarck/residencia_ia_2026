import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# 1. Configuração do ambiente e cliente LLM/Embeddings
diretorio_atual = Path(__file__).parent
raiz_projeto = diretorio_atual.parent if (diretorio_atual.parent / ".env").exists() else diretorio_atual
load_dotenv(raiz_projeto / ".env")

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
)

# Modelo padrão de embeddings
MODELO_EMBEDDING = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_embedding(texto: str) -> list[float]:
    """Gera o vetor de embedding para uma string."""
    texto_limpo = texto.replace("\n", " ").strip()
    if not texto_limpo:
        return [0.0] * 1536  # Retorna vetor zerado se a string estiver vazia
        
    resposta = client.embeddings.create(
        model=MODELO_EMBEDDING,
        input=texto_limpo
    )
    return resposta.data[0].embedding


# 2. Funções de Distância e Similaridade Vetorial
def distancia_euclidiana(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula a Distância Euclidiana (norma L2 da diferença)."""
    return float(np.linalg.norm(vec1 - vec2))

def similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula a Similaridade de Cosseno entre dois vetores."""
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm_v1 * norm_v2))

def distancia_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula a Distância de Cosseno (1 - Similaridade de Cosseno)."""
    return float(1.0 - similaridade_cosseno(vec1, vec2))


# ==============================================================================
# PARTE 1: Testando com Palavras/Termos
# Termos: gato, felino, cachorro, carro, caminhão, moto, banana, maçã, goiaba
# ==============================================================================
def executar_parte_1_termos():
    print("==================================================")
    print("PARTE 1: Teste de Embeddings com Termos Específicos")
    print("==================================================\n")

    termos = ["gato", "felino", "cachorro", "carro", "caminhão", "moto", "banana", "maçã", "goiaba"]
    embeddings_termos = {termo: np.array(get_embedding(termo), dtype=np.float32) for termo in termos}

    # Testando comparações selecionadas
    pares_teste = [
        ("gato", "felino"),
        ("gato", "cachorro"),
        ("carro", "moto"),
        ("banana", "maçã"),
        ("gato", "carro")
    ]

    res = []
    for t1, t2 in pares_teste:
        v1, v2 = embeddings_termos[t1], embeddings_termos[t2]
        res.append({
            "Termo 1": t1,
            "Termo 2": t2,
            "Dist. Euclidiana": round(distancia_euclidiana(v1, v2), 4),
            "Sim. Cosseno": round(similaridade_cosseno(v1, v2), 4),
            "Dist. Cosseno": round(distancia_cosseno(v1, v2), 4)
        })

    df_termos = pd.DataFrame(res)
    print(df_termos.to_string(index=False))
    print("\n")


# ==============================================================================
# PARTE 2: Comparação de Frases com Âncora
# ==============================================================================
def executar_parte_2_frases():
    print("==================================================")
    print("PARTE 2: Comparação de Frases com Âncora")
    print("==================================================\n")

    frase_ancora = "O cachorro correu no parque e brincou com a bola."

    frases_comparacao = [
        ("Similar (mesmo sentido)", "Um cão estava correndo no jardim e brincando com seu brinquedo."),
        ("Relacionado (animais)", "O gato dormiu na almofada da sala durante toda a tarde."),
        ("Diferente (outro domínio)", "A taxa de juros do banco central subiu dois pontos percentuais."),
        ("Oposto/Negação", "Nenhum animal esteve no parque e o cão permaneceu preso em casa.")
    ]

    vec_ancora = np.array(get_embedding(frase_ancora), dtype=np.float32)

    resultados = []
    for categoria, texto in frases_comparacao:
        vec = np.array(get_embedding(texto), dtype=np.float32)
        resultados.append({
            "Categoria": categoria,
            "Texto": texto,
            "Dist. Euclidiana": round(distancia_euclidiana(vec_ancora, vec), 4),
            "Similaridade Cosseno": round(similaridade_cosseno(vec_ancora, vec), 4),
            "Distância Cosseno": round(distancia_cosseno(vec_ancora, vec), 4)
        })

    df_resultados = pd.DataFrame(resultados)
    print(df_resultados.to_string(index=False))
    print("\n")


# ==============================================================================
# PARTE 3: Busca Semântica Manual em Markdown (Linhas, Parágrafos e Arquivos)
# ==============================================================================
def realizar_busca_semantica(query: str, chunks: list[dict], top_k: int = 3):
    """Calcula a similaridade da query contra cada chunk e retorna o Top K."""
    vec_query = np.array(get_embedding(query), dtype=np.float32)

    scores = []
    for item in chunks:
        vec_chunk = item["embedding"]
        score = similaridade_cosseno(vec_query, vec_chunk)
        scores.append({
            "Arquivo": item["arquivo"],
            "Score": round(score, 4),
            "Trecho": item["texto"][:150] + ("..." if len(item["texto"]) > 150 else "")
        })

    # Ordena do maior score para o menor
    scores_ordenados = sorted(scores, key=lambda x: x["Score"], reverse=True)
    return pd.DataFrame(scores_ordenados[:top_k])


def executar_parte_3_busca_md():
    print("==================================================")
    print("PARTE 3: Busca Semântica com Granularidades Distintas")
    print("==================================================\n")

    arquivos_md = ["artigo_twitter.md", "escrita_academica.md", "bioetica_ia.md"]
    caminho_pasta = diretorio_atual

    # Carrega o conteúdo dos arquivos
    documentos = {}
    for nome in arquivos_md:
        p = caminho_pasta / nome
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                documentos[nome] = f.read()

    if not documentos:
        print("⚠️ Nenhum arquivo .md encontrado na pasta para a busca semântica.")
        return

    # --- 1. Granularidade: LINHA POR LINHA ---
    chunks_linhas = []
    for nome, conteudo in documentos.items():
        linhas = [l.strip() for l in conteudo.split("\n") if len(l.strip()) > 20] # filtra linhas curtas
        for linha in linhas:
            chunks_linhas.append({
                "arquivo": nome,
                "texto": linha,
                "embedding": np.array(get_embedding(linha), dtype=np.float32)
            })

    # --- 2. Granularidade: PARÁGRAFOS ---
    chunks_paragrafos = []
    for nome, conteudo in documentos.items():
        paragrafos = [p.strip() for p in conteudo.split("\n\n") if len(p.strip()) > 30]
        for para in paragrafos:
            chunks_paragrafos.append({
                "arquivo": nome,
                "texto": para,
                "embedding": np.array(get_embedding(para), dtype=np.float32)
            })

    # --- 3. Granularidade: ARQUIVO/CAPÍTULO COMPLETO ---
    chunks_capitulos = []
    for nome, conteudo in documentos.items():
        chunks_capitulos.append({
            "arquivo": nome,
            "texto": conteudo[:1000], # Amostra do arquivo
            "embedding": np.array(get_embedding(conteudo[:4000]), dtype=np.float32)
        })

    # Query de teste
    query_teste = "O que é autonomia e opacidade algorítmica?"
    print(f"🔍 Executando busca para a Query: '{query_teste}'\n")

    print("--- TOP 3 - Busca por LINHAS ---")
    df_linhas = realizar_busca_semantica(query_teste, chunks_linhas)
    print(df_linhas.to_string(index=False))
    print("\n")

    print("--- TOP 3 - Busca por PARÁGRAFOS ---")
    df_paragrafos = realizar_busca_semantica(query_teste, chunks_paragrafos)
    print(df_paragrafos.to_string(index=False))
    print("\n")

    print("--- TOP 3 - Busca por ARQUIVOS COMPLETOS ---")
    df_capitulos = realizar_busca_semantica(query_teste, chunks_capitulos)
    print(df_capitulos.to_string(index=False))


if __name__ == "__main__":
    executar_parte_1_termos()
    executar_parte_2_frases()
    executar_parte_3_busca_md()