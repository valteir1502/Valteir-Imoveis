import os
import PyPDF2
import docx

def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text

def read_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for p in doc.paragraphs:
            text += p.text + "\n"
    except Exception as e:
        text = f"Error reading DOCX: {e}"
    return text

base_path = r"D:\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo"

compradores_path = os.path.join(base_path, "Compradores")

print("--- LENDO COMPRADORES ---")
for file in os.listdir(compradores_path):
    if file.endswith(".pdf"):
        full_path = os.path.join(compradores_path, file)
        print(f"--- Arquivo: {file} ---")
        print(read_pdf(full_path)[:500]) # Print first 500 chars to avoid huge output

print("\n--- LENDO CONTRATO ATUAL ---")
contract_path = os.path.join(base_path, "Contrato_Compromisso_Compra_e_Venda_Ipe_da_Mata.docx")
print(read_docx(contract_path)[:2000]) # Print first 2000 chars of contract
