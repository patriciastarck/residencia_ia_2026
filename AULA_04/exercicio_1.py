import json
from langchain_core.documents import Document


# 1 — Criando Documents manualmente

documentos = [
    Document(
        page_content="Embeddings transformam textos em vetores numéricos contínuos, preservando similaridade semântica.",
        metadata={
            "fonte": "modulo_embeddings.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "embeddings"
        }
    ),
    Document(
        page_content="O chunking por sentenças agrupa frases completas para evitar o corte abrupto de pensamentos e ideias.",
        metadata={
            "fonte": "modulo_chunking.md",
            "pagina": 3,
            "tipo": "teoria",
            "tema": "chunking"
        }
    ),
    Document(
        page_content="A técnica de overlap mantém uma quantidade de caracteres ou tokens repetidos entre blocos adjacentes.",
        metadata={
            "fonte": "modulo_chunking.md",
            "pagina": 4,
            "tipo": "pratica",
            "tema": "chunking"
        }
    ),
    Document(
        page_content="Sistemas de RAG utilizam vector stores para buscar contexto relevante antes de consultar a LLM.",
        metadata={
            "fonte": "modulo_rag.md",
            "pagina": 2,
            "tipo": "teoria",
            "tema": "rag"
        }
    ),
    Document(
        page_content="A tokenização com Byte-Pair Encoding (BPE) decompõe palavras raras em subpalavras frequentes.",
        metadata={
            "fonte": "modulo_tokenizacao.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "tokenizacao"
        }
    )
]

# 2. Print de cada documento
print("=== EXERCÍCIO 1: LISTAGEM DOS DOCUMENTOS ===")
for idx, doc in enumerate(documentos, start=1):
    print(f"\n[Documento {idx}]")
    print(f"page_content : {doc.page_content}")
    print(f"metadata     : {doc.metadata}")

# 3. Resultado de len
print("\n" + "=" * 35)
print(f"Total de documentos: {len(documentos)}")
print("=" * 35)

# EXERCÍCIO 2 — Exemplo de Chunk em JSON

chunk_exemplo = {
    "page_content": "A busca semântica utiliza a similaridade por cosseno entre o vetor da query e os vetores dos chunks armazenados na vector store.",
    "metadata": {
        "fonte": "artigo_twitter.md",
        "documento_id": "doc_twitter_01",
        "chunk_index": 3,
        "estrategia": "recursive",
        "chunk_size": 500,
        "chunk_overlap": 50,
        "n_caracteres": 141,
        "secao": "Busca Semântica e Similaridade",
        "total_chunks": 12,
        "token_count": 28
    }
}

print("\n=== EXERCÍCIO 2: EXEMPLO DE CHUNK EM JSON ===")
print(json.dumps(chunk_exemplo, indent=2, ensure_ascii=False))

"""

Resposta 1:

No Document do LangChain, metadata é um dict padrão do Python que aceita qualquer tipo. 

Se criarmos um Document sem passar metadata, o LangChain inicializa o campo metadata automaticamente como um dicionário vazio ({}).

Resposta 2:


   fonte           str     Nome do arquivo .md de origem
   documento_id    str     Identificador único do documento
   chunk_index     int     Posição sequencial do chunk no documento
   estrategia      str     Estratégia de chunking usada (ex: 'recursive')
   chunk_size      int     Tamanho configurado no splitter
   chunk_overlap   int     Overlap configurado no splitter
   n_caracteres    int     Tamanho real em caracteres do chunk
   secao           str     [Próprio] Nome da seção/cabeçalho Markdown de origem
   total_chunks    int     [Próprio] Total de chunks gerados para o documento
   token_count     int     [Próprio] Quantidade estimada de tokens do chunk
   

Justificativa dos 3 campos próprios:
   - secao: Responde "a qual subtópico este trecho pertence?", permitindo filtrar buscas por assunto específico.
   - total_chunks: Responde "em que ponto relativo do documento este trecho está?", ajudando a identificar início, meio ou fim.
   - token_count: Responde "quantos tokens este trecho consome na janela da LLM?", permitindo gerenciar o limite de contexto do prompt.

Campo para citação da fonte:
   - 'fonte_citacao' ou 'url_origem', contendo uma referência legível (ex: "Artigo Twitter, Seção 2, pág. 3").

Por que chunk_index é útil:
   - Permite recupeerar os blocos do mesmo documento caso o trecho retornado esteja cortado no meio de uma frase ou raciocínio.
"""