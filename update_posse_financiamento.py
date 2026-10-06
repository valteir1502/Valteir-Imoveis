import os
import shutil
import docx

FOLDER = r"C:\Users\valte\OneDrive\Área de Trabalho\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo"
PROJ = r"c:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis"

src = [f for f in os.listdir(FOLDER) if "15 dias" in f and f.endswith(".docx")][0]
src_path = os.path.join(FOLDER, src)
shutil.copy2(src_path, os.path.join(FOLDER, "Contrato Buona Vita_BACKUP4_antes_posse.docx"))

doc = docx.Document(src_path)

target = None
for p in doc.paragraphs:
    if p.text.strip().startswith("Parágrafo Segundo (Posse e Entrega"):
        target = p
        break
assert target is not None, "Parágrafo da posse não encontrado"

NEW_TEXT = (
    "Parágrafo Segundo (Posse e Entrega Simultânea das Chaves): As partes contratantes convencionam que "
    "a entrega das chaves e a respectiva imissão na posse de ambos os imóveis (tanto da residência no "
    "Condomínio Parque Buona Vita quanto do apartamento nº 74 no Edifício Ipê da Mata) ocorrerão de forma "
    "simultânea somente após a assinatura do contrato de financiamento imobiliário referente à 3ª Parcela "
    "(item 3 desta Cláusula) perante a Instituição Financeira escolhida pelos PROMISSÁRIOS COMPRADORES, "
    "mediante a constatação do adimplemento das obrigações pecuniárias previstas nos itens 1 e 2 desta Cláusula. "
    "Na hipótese de conversão do negócio para pagamento à vista, prevista no Parágrafo Quarto desta Cláusula, "
    "a entrega das chaves e a imissão na posse da residência ocorrerão após a quitação integral do saldo à vista."
)

runs = target.runs
runs[0].text = NEW_TEXT
for r in runs[1:]:
    r._r.getparent().remove(r._r)

print("Novo texto:\n", target.text)

out = src_path
try:
    doc.save(out)
    print(f"Salvo em: {src}")
except PermissionError:
    out = os.path.join(FOLDER, src.replace(".docx", " - posse financiamento.docx"))
    doc.save(out)
    print(f"Arquivo aberto no Word. Salvo como: {os.path.basename(out)}")

for t in [os.path.join(FOLDER, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx"),
          os.path.join(PROJ, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx")]:
    try:
        doc.save(t)
    except PermissionError:
        print(f"Espelho aberto no Word: {t}")
print("Espelhos atualizados.")
