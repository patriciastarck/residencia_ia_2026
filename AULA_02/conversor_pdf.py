def extrair_metadados(caminho_ou_conteudo: str) -> dict:
    p = Path(caminho_ou_conteudo)
    if p.exists() and p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            conteudo = f.read()
    else:
        conteudo = caminho_ou_conteudo

    # Prompt instruindo o formato de saída JSON exato
    prompt_sistema = (
        "Você é um assistente acadêmico. Extraia os metadados do texto fornecido "
        "e responda EXCLUSIVAMENTE em formato JSON com o seguinte schema:\n"
        "{\n"
        '  "titulo": "string",\n'
        '  "autores": ["string"],\n'
        '  "ano": 2024\n'
        "}"
    )

    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "google/gemini-2.5-flash"),
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Texto do documento:\n\n{conteudo[:3000]}"}
        ],
        response_format={"type": "json_object"}
    )

    # Converte a resposta texto JSON em dicionário Python e valida com Pydantic
    conteudo_json = json.loads(completion.choices[0].message.content)
    metadados_validados = MetadadosArtigo(**conteudo_json)
    
    return metadados_validados.model_dump()