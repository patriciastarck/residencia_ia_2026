import os
import sys
from pathlib import Path

# 1. Desativa a compilação do PyTorch Inductor no Windows antes de importar o Docling
os.environ["TORCHINDUCTOR_DISABLE"] = "1"
os.environ["TORCH_COMPILE_DISABLE"] = "1"

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

pasta_aula_04 = Path(__file__).resolve().parent
print(f"📁 Pasta de trabalho: {pasta_aula_04}")

# 2. Configura opções leves para evitar aceleração C++
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False
pipeline_options.do_table_structure = False

converter = DocumentConverter(
    format_options={
        "pdf": PdfFormatOption(pipeline_options=pipeline_options)
    }
)

def converter_todos():
    arquivos_pdf = sorted(list(pasta_aula_04.glob("*.pdf")))
    
    if not arquivos_pdf:
        print(f"⚠️ Nenhum arquivo .pdf encontrado em: {pasta_aula_04}")
        return

    print(f"📂 Encontrados {len(arquivos_pdf)} arquivos PDF para conversão com Docling.\n")

    for i, caminho_pdf in enumerate(arquivos_pdf, start=1):
        caminho_md_saida = pasta_aula_04 / f"{caminho_pdf.stem}.md"
        print(f"[{i}/{len(arquivos_pdf)}] ⏳ Convertendo: {caminho_pdf.name}...")
        
        try:
            resultado = converter.convert(caminho_pdf)
            conteudo_markdown = resultado.document.export_to_markdown()

            with open(caminho_md_saida, "w", encoding="utf-8") as f:
                f.write(conteudo_markdown)
                
            print(f"    ✅ Salvo: {caminho_md_saida.name}")
        except Exception as e:
            print(f"    ❌ Erro ao converter {caminho_pdf.name}: {e}")

    print("\n🎉 Todas as conversões foram finalizadas!")

if __name__ == "__main__":
    converter_todos()