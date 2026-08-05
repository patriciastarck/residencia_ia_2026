from pathlib import Path

# Garante o caminho exato da pasta AULA_02
diretorio = Path(__file__).parent

# Artigo 1: Twitter/X
artigo_1 = """# O caso Twitter/X: algoritmo, espaço público e ultraliberalismo digital

**Autores:** Ettore Schimid Batalha, Jefferson Ribeiro da Silva, Bruno Daniel Vendruscolo Espinosa Velásquez  
**Periódico:** MEDIAÇÕES, Londrina, v. 30, p. 1-18, 2025 | e52669

## Resumo
Este artigo investiga a dinâmica das redes sociais na formação do debate público, com ênfase no Twitter (atualmente denominado X) e na influência dos algoritmos na regulação do conteúdo. Por meio de uma abordagem interdisciplinar que integra os conceitos da Sociologia Digital e das Ciências da Computação, o estudo analisa como os mecanismos de curadoria e moderação – operados por empresas privadas – afetam a construção dos discursos e a propagação das informações.

### Palavras-chave
redes sociais; espaço público; algoritmos; Twitter/X; desinformação.
"""

# Artigo 2: Escrita Acadêmica e IA
artigo_2 = """# Oficina de Escrita Acadêmica: Escrita acadêmica ética, responsável e humana com inteligência artificial

**Autor:** Rafael Cardoso Sampaio  
**Periódico:** Rev. Sociol. Polit., v. 33, e018, 2025

## Resumo
A rápida disseminação da inteligência artificial generativa (IAG) transformou práticas de escrita acadêmica, ampliando a eficiência, mas levantando preocupações sobre autoria, integridade, privacidade e desenvolvimento cognitivo. Este artigo busca preencher essa lacuna ao propor um método estruturado de uso ético, responsável e humano da IA.

### Palavras-chave
escrita acadêmica, integridade científica, Inteligência Artificial Generativa, autoria, revisão narrativa.
"""

# Artigo 3: Bioética e IA
artigo_3 = """# Entre o algoritmo e o Juramento de Hipócrates: bioética na era da inteligência artificial

**Autores:** Juracy Barbosa dos Santos, Guilhermina Rego, Rui Nunes  
**Periódico:** Rev. Bioét. vol.34 Brasília 2026

## Resumo
O avanço da inteligência artificial tem transformado profundamente a prática médica. De sistemas de apoio à decisão clínica a algoritmos de triagem e diagnóstico, a inteligência artificial tem demonstrado potencial para diagnósticos precoces, terapias personalizadas, otimização de recursos, redução de erros e ampliação do acesso a cuidados especializados.

### Palavras-chave
Bioética. Inteligência artificial. Ética médica. Autonomia pessoal.
"""

# Dicionário relacionando os nomes dos arquivos com o texto
documentos = {
    "artigo_twitter.md": artigo_1,
    "escrita_academica.md": artigo_2,
    "bioetica_ia.md": artigo_3
}

# Criando e escrevendo os arquivos na pasta AULA_02
for nome_arquivo, conteudo in documentos.items():
    caminho_completo = diretorio / nome_arquivo
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"✅ Arquivo gerado com sucesso: {nome_arquivo}")

print("\n🎉 Todos os 3 arquivos Markdown foram criados na pasta AULA_02!")