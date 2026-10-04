import os
import shutil
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_reginaldo_contract():
    folder = r"C:\Users\valte\OneDrive\Área de Trabalho\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo"
    files = [f for f in os.listdir(folder) if f.startswith("Contrato Compromisso Compra e Venda") and f.endswith(".docx") and not "BACKUP" in f]
    if not files:
        print("Arquivo de contrato não encontrado!")
        return
    
    filename = files[0]
    filepath = os.path.join(folder, filename)
    backup_path = os.path.join(folder, "Contrato Compromisso Compra e Venda - Buona Vita - Reginaldo x João Roberto_BACKUP.docx")
    
    shutil.copy2(filepath, backup_path)
    print(f"Backup criado com sucesso em: {backup_path}")
    
    doc = docx.Document(filepath)
    
    # Localizar parágrafos-chave
    p_clausula_2 = None
    p_paragrafo_2_clausula_2 = None
    p_clausula_3 = None
    p_clausula_5 = None
    p_p1_clausula_5 = None
    p_p2_clausula_5 = None
    p_p3_clausula_5 = None
    p_clausula_6 = None
    p_p1_clausula_7 = None
    p_clausula_8_text = None
    
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if "CLÁUSULA SEGUNDA – DO PREÇO" in t.upper() or "CLÁUSULA SEGUNDA - DO PREÇO" in t.upper():
            p_clausula_2 = (i, p)
        elif p_clausula_2 and "PARÁGRAFO SEGUNDO (POSSE" in t.upper():
            p_paragrafo_2_clausula_2 = (i, p)
        elif "CLÁUSULA TERCEIRA" in t.upper():
            p_clausula_3 = (i, p)
        elif "CLÁUSULA QUINTA" in t.upper():
            p_clausula_5 = (i, p)
        elif p_clausula_5 and not p_clausula_6 and "PARÁGRAFO PRIMEIRO" in t.upper():
            p_p1_clausula_5 = (i, p)
        elif p_clausula_5 and not p_clausula_6 and "PARÁGRAFO SEGUNDO" in t.upper():
            p_p2_clausula_5 = (i, p)
        elif p_clausula_5 and not p_clausula_6 and "PARÁGRAFO TERCEIRO" in t.upper():
            p_p3_clausula_5 = (i, p)
        elif "CLÁUSULA SEXTA" in t.upper():
            p_clausula_6 = (i, p)
        elif "PARÁGRAFO PRIMEIRO (DA PROCURAÇÃO" in t.upper():
            p_p1_clausula_7 = (i, p)
        elif "MULTA PENAL COMPENSATÓRIA DE 10%" in t.upper() or "DA CLÁUSULA PENAL COMPENSATÓRIA" in t.upper():
            if "MULTA PENAL" in t.upper():
                p_clausula_8_text = (i, p)

    print(f"Cláusula 2: P{p_clausula_2[0] if p_clausula_2 else 'None'}")
    print(f"Parágrafo Segundo Cláusula 2: P{p_paragrafo_2_clausula_2[0] if p_paragrafo_2_clausula_2 else 'None'}")
    print(f"Cláusula 5: P{p_clausula_5[0] if p_clausula_5 else 'None'}")
    print(f"Cláusula 6: P{p_clausula_6[0] if p_clausula_6 else 'None'}")

    # 1. ATUALIZAR / INSERIR PARÁGRAFOS NA CLÁUSULA SEGUNDA
    # Criar Parágrafo Terceiro e Quarto após o Parágrafo Segundo da Cláusula Segunda
    p_ancora = p_paragrafo_2_clausula_2[1]
    
    # Função auxiliar para configurar formato padrão
    def set_p_format(p):
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15

    def add_run_custom(p, text, bold=False):
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10.5)
        r.bold = bold
        return r

    # Inserir Parágrafo Quarto (inserido primeiro em relação à âncora, ou inserido depois)
    # Criamos novo elemento w:p
    new_p3 = docx.oxml.OxmlElement("w:p")
    p_ancora._p.addnext(new_p3)
    para3 = docx.text.paragraph.Paragraph(new_p3, doc)
    set_p_format(para3)
    
    add_run_custom(para3, "- Parágrafo Terceiro (Do Prazo de 20 Dias Úteis para Venda do Apartamento e Consolidação da Permuta): ", bold=True)
    add_run_custom(para3, "Fica expressamente estabelecido e convencionado entre os contratantes que os ")
    add_run_custom(para3, "PROMISSÁRIOS COMPRADORES", bold=True)
    add_run_custom(para3, " terão o prazo improrrogável de até ")
    add_run_custom(para3, "20 (vinte) dias úteis", bold=True)
    add_run_custom(para3, ", contados rigorosamente a partir da data de assinatura deste contrato, para buscar e concretizar a venda do ")
    add_run_custom(para3, "Apartamento nº 74 do Condomínio Edifício Ipê da Mata", bold=True)
    add_run_custom(para3, " perante terceiros adquirentes no mercado imobiliário. Caso a referida venda a terceiros não venha a ser efetivamente concluída e formalizada dentro do mencionado prazo estipulado de 20 (vinte) dias úteis, a dação em pagamento / permuta imobiliária se consolidará de pleno direito e em caráter definitivo, irrevogável e irretratável, passando o referido apartamento a ser de legítima, plena e exclusiva propriedade dos ")
    add_run_custom(para3, "PROMITENTES VENDEDORES", bold=True)
    add_run_custom(para3, " pelo valor de avaliação de ")
    add_run_custom(para3, "R$ 1.610.000,00 (um milhão, seiscentos e dez mil reais)", bold=True)
    add_run_custom(para3, ", mantendo-se inalterados o valor total da transação de ")
    add_run_custom(para3, "R$ 2.390.000,00 (dois milhões, trezentos e noventa mil reais)", bold=True)
    add_run_custom(para3, " e a obrigação dos vendedores referente à instalação dos aparelhos de ar-condicionado na residência do Buona Vita prevista na Cláusula Quinta deste instrumento.")

    new_p4 = docx.oxml.OxmlElement("w:p")
    para3._p.addnext(new_p4)
    para4 = docx.text.paragraph.Paragraph(new_p4, doc)
    set_p_format(para4)

    add_run_custom(para4, "- Parágrafo Quarto (Da Venda do Apartamento, Repactuação do Valor para R$ 2.250.000,00 À Vista e Exoneração dos Ares-Condicionados): ", bold=True)
    add_run_custom(para4, "Na hipótese de os ")
    add_run_custom(para4, "PROMISSÁRIOS COMPRADORES", bold=True)
    add_run_custom(para4, " concretizarem com êxito a venda do Apartamento nº 74 do Edifício Ipê da Mata a terceiros dentro do aludido prazo de 20 (vinte) dias úteis, as partes estipulam que vigorarão de forma imediata e automática as seguintes condições especiais:\n")
    add_run_custom(para4, "a) O valor total da presente negociação da residência unifamiliar no Condomínio Parque Buona Vita será repactuado e passará a ser de ")
    add_run_custom(para4, "R$ 2.250.000,00 (dois milhões, duzentos e cinquenta mil reais)", bold=True)
    add_run_custom(para4, ";\n")
    add_run_custom(para4, "b) A forma de pagamento passará a ser na modalidade integralmente ")
    add_run_custom(para4, "À VISTA", bold=True)
    add_run_custom(para4, ", computando-se e deduzindo-se o sinal de R$ 200.000,00 (duzentos mil reais) pago no ato da assinatura deste instrumento e quitando-se integralmente o saldo remanescente de ")
    add_run_custom(para4, "R$ 2.050.000,00 (dois milhões e cinquenta mil reais)", bold=True)
    add_run_custom(para4, " na data da formalização da escritura/contrato de venda do apartamento a terceiros e correspondente liberação financeira dos recursos;\n")
    add_run_custom(para4, "c) ")
    add_run_custom(para4, "Exoneração Total dos Vendedores quanto aos Ares-Condicionados: ", bold=True)
    add_run_custom(para4, "Ocorrendo a venda do apartamento a terceiros e a fixação do preço com desconto à vista de R$ 2.250.000,00, ")
    add_run_custom(para4, "os PROMITENTES VENDEDORES ficarão formal e expressamente exonerados e desobrigados de adquirir, fornecer e instalar quaisquer aparelhos de ar-condicionado", bold=True)
    add_run_custom(para4, " na residência do Condomínio Parque Buona Vita (ficando desobrigados tanto dos 05 aparelhos individuais quanto do ar-condicionado modelo Cassette do espaço gourmet), sendo a residência entregue sem os referidos aparelhos, permanecendo outrossim inalterada a supressão da lareira conforme acordo comercial prévio.")

    # 2. ATUALIZAR CLÁUSULA QUINTA
    # Parágrafo Primeiro
    p_p1 = p_p1_clausula_5[1]
    p_p1.text = ""
    add_run_custom(p_p1, "- Parágrafo Primeiro (Equipamentos no Apartamento Ipê da Mata - Permuta): ", bold=True)
    add_run_custom(p_p1, "Na hipótese de consolidação da permuta tratada na Cláusula Segunda deste contrato, fica expressamente convencionado que permanecerão instalados e serão entregues pelos PROMISSÁRIOS COMPRADORES no Apartamento nº 74 do Condomínio Edifício Ipê da Mata o total de ")
    add_run_custom(p_p1, "05 (cinco) aparelhos de ar-condicionado", bold=True)
    add_run_custom(p_p1, " no estado de conservação e perfeito funcionamento em que se encontram, com todas as suas tubulações, fiações, condensadoras, evaporadoras e respectivos controles remotos, os quais são transferidos aos PROMITENTES VENDEDORES sem qualquer custo adicional.")

    # Parágrafo Segundo
    p_p2 = p_p2_clausula_5[1]
    p_p2.text = ""
    add_run_custom(p_p2, "- Parágrafo Segundo (Instalação dos Aparelhos de Ar-Condicionado na Casa do Buona Vita pelos Vendedores): ", bold=True)
    add_run_custom(p_p2, "Ressalvada a hipótese de venda à vista tratada no Parágrafo Quarto da Cláusula Segunda, os PROMITENTES VENDEDORES assumem a responsabilidade e obrigação de adquirir, fornecer e instalar, por sua conta e ônus exclusivo, na residência do Condomínio Parque Buona Vita, o total de ")
    add_run_custom(p_p2, "05 (cinco) aparelhos de ar-condicionado", bold=True)
    add_run_custom(p_p2, ", novos e em perfeito estado de funcionamento, rigorosamente nas seguintes potências e especificações técnicas:\n")
    add_run_custom(p_p2, "I. 03 (três) aparelhos de ar-condicionado com capacidade de 12.000 BTUs;\n", bold=True)
    add_run_custom(p_p2, "II. 01 (um) aparelho de ar-condicionado com capacidade de 18.000 BTUs;\n", bold=True)
    add_run_custom(p_p2, "III. 01 (um) aparelho de ar-condicionado com capacidade de 24.000 BTUs;\n", bold=True)
    add_run_custom(p_p2, "IV. ALÉM de 01 (um) aparelho de ar-condicionado modelo Cassette com capacidade de 60.000 BTUs, ", bold=True)
    add_run_custom(p_p2, "a ser devidamente instalado, embutido no teto e testado no ambiente do Espaço Gourmet.")

    # Parágrafo Terceiro
    p_p3 = p_p3_clausula_5[1]
    p_p3.text = ""
    add_run_custom(p_p3, "- Parágrafo Terceiro (Supressão da Lareira e Substituição pelo Ar-Condicionado Cassette de 60.000 BTUs): ", bold=True)
    add_run_custom(p_p3, "Fica expressamente salientado e acordado que na residência do Condomínio Parque Buona Vita ")
    add_run_custom(p_p3, "NÃO será instalada a lareira", bold=True)
    add_run_custom(p_p3, " que constava originalmente do projeto da área de lazer (fire place), por ter sido objeto de expresso e livre acordo comercial entre as partes, tendo sido a referida lareira substituída em definitivo pelo fornecimento e instalação do aparelho de ")
    add_run_custom(p_p3, "ar-condicionado modelo Cassette de 60.000 BTUs no Espaço Gourmet", bold=True)
    add_run_custom(p_p3, " a cargo exclusivo dos PROMITENTES VENDEDORES, dando os contratantes mútua, plena e irrevogável quitação quanto a este item.")

    # Inserir Parágrafo Quarto da Cláusula Quinta
    new_p5_4 = docx.oxml.OxmlElement("w:p")
    p_p3._p.addnext(new_p5_4)
    para5_4 = docx.text.paragraph.Paragraph(new_p5_4, doc)
    set_p_format(para5_4)
    add_run_custom(para5_4, "- Parágrafo Quarto (Da Desoneração dos Vendedores em Caso de Venda do Apartamento à Vista): ", bold=True)
    add_run_custom(para5_4, "Conforme estabelecido no Parágrafo Quarto da Cláusula Segunda, caso os PROMISSÁRIOS COMPRADORES concretizem a venda do apartamento a terceiros dentro do prazo de 20 (vinte) dias úteis e o negócio da residência no Condomínio Buona Vita seja liquidado pelo valor de R$ 2.250.000,00 à vista, as obrigações dos PROMITENTES VENDEDORES estipuladas no Parágrafo Segundo desta Cláusula (instalação dos 05 aparelhos de ar-condicionado e do Cassette de 60.000 BTUs) ")
    add_run_custom(para5_4, "ficarão plena e automaticamente extintas e sem efeito", bold=True)
    add_run_custom(para5_4, ", não sendo instalado nenhum aparelho de ar-condicionado pelos vendedores na referida residência, mantendo-se igualmente a supressão da lareira.")

    # 3. ATUALIZAR CLÁUSULA SÉTIMA (PROCURAÇÃO APÓS OS 20 DIAS ÚTEIS)
    if p_p1_clausula_7:
        p_c7 = p_p1_clausula_7[1]
        p_c7.text = ""
        add_run_custom(p_c7, "- Parágrafo Primeiro (Da Procuração Pública do Imóvel em Permuta): ", bold=True)
        add_run_custom(p_c7, "Especificamente em relação ao imóvel dado em permuta (Apartamento nº 74 do Condomínio Ipê da Mata - Matrícula nº 117.310 do 2º ORI), ")
        add_run_custom(p_c7, "decorrido o prazo de 20 (vinte) dias úteis previsto no Parágrafo Terceiro da Cláusula Segunda sem a concretização da venda a terceiros, consolidando-se a permuta", bold=True)
        add_run_custom(p_c7, ", os PROMISSÁRIOS COMPRADORES obrigam-se formalmente a outorgar em favor dos PROMITENTES VENDEDORES (ou de pessoa física/jurídica por estes expressamente indicada), no prazo improrrogável de até 05 (cinco) dias úteis subsequentes, Instrumento Público de Procuração lavrado em Tabelionato de Notas competente.")

    # 4. ATUALIZAR CLÁUSULA OITAVA (CLÁUSULA PENAL)
    if p_clausula_8_text:
        p_c8 = p_clausula_8_text[1]
        p_c8.text = ""
        add_run_custom(p_c8, "A parte que descumprir, retardar ou obstaculizar a execução de qualquer das cláusulas ou obrigações assumidas neste contrato pagará à parte inocente a multa penal compensatória de 10% (dez por cento), calculada sobre o valor total da transação (")
        add_run_custom(p_c8, "R$ 2.390.000,00, ou R$ 2.250.000,00 na hipótese de conversão para venda à vista", bold=True)
        add_run_custom(p_c8, "), devidamente atualizada pelo índice oficial do IPCA/IBGE desde a data da assinatura até a efetiva liquidação, respondendo ainda por eventuais perdas e danos e honorários advocatícios fixados no patamar de 20% (vinte por cento) em caso de cobrança judicial.")

    # Salvar o documento oficial atualizado
    doc.save(filepath)
    print(f"Documento oficial atualizado e salvo em: {filepath}")

    # Salvar cópia no Workspace do Projeto também
    proj_folder = r"c:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis"
    proj_target = os.path.join(proj_folder, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx")
    doc.save(proj_target)
    print(f"Cópia espelhada salva no Workspace: {proj_target}")

    reginaldo_mirror = os.path.join(folder, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx")
    doc.save(reginaldo_mirror)
    print(f"Cópia espelhada salva na pasta Reginaldo: {reginaldo_mirror}")

if __name__ == "__main__":
    update_reginaldo_contract()
