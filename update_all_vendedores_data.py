import os
import shutil
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_contracts_with_all_sellers():
    folder = r"C:\Users\valte\OneDrive\Área de Trabalho\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo"
    files = [f for f in os.listdir(folder) if f.startswith("Contrato Compromisso Compra e Venda") and not "BACKUP" in f and f.endswith(".docx")]
    if not files:
        print("Arquivo do contrato não encontrado!")
        return

    filepath = os.path.join(folder, files[0])
    backup_path = os.path.join(folder, "Contrato Compromisso Compra e Venda - Buona Vita - Reginaldo x João Roberto_BACKUP2.docx")
    shutil.copy2(filepath, backup_path)
    print(f"Backup de segurança criado em: {backup_path}")

    doc = docx.Document(filepath)

    # 1. Localizar o cabeçalho 'A – PROMITENTES VENDEDORES:' e parágrafos dos vendedores
    idx_header_vend = None
    idx_header_comp = None
    idx_promitentes_vend_sig = None
    idx_promissarios_comp_sig = None

    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip().upper()
        if "A – PROMITENTES VENDEDORES" in t or "A - PROMITENTES VENDEDORES" in t:
            idx_header_vend = i
        elif "B – PROMISSÁRIOS COMPRADORES" in t or "B - PROMISSÁRIOS COMPRADORES" in t:
            idx_header_comp = i
        elif t == "PROMITENTES VENDEDORES:":
            idx_promitentes_vend_sig = i
        elif t == "PROMISSÁRIOS COMPRADORES:" or t == "PROMISSARIOS COMPRADORES:":
            if idx_promitentes_vend_sig and i > idx_promitentes_vend_sig:
                idx_promissarios_comp_sig = i

    print(f"Header Vendedores: P{idx_header_vend}")
    print(f"Header Compradores: P{idx_header_comp}")
    print(f"Assinatura Vendedores: P{idx_promitentes_vend_sig}")
    print(f"Assinatura Compradores: P{idx_promissarios_comp_sig}")

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

    # 2. Reestruturar a qualificação dos Vendedores (P[idx_header_vend + 1])
    # Vamos atualizar o parágrafo existente para o Casal 1 (Ademir e Marilaine) e inserir um parágrafo para o Casal 2 (Weber e Patricia)
    p_v1 = doc.paragraphs[idx_header_vend + 1]
    p_v1.text = ""
    set_p_format(p_v1)

    add_run_custom(p_v1, "1. ADEMIR VENTURINI", bold=True)
    add_run_custom(p_v1, ", brasileiro, marceneiro, nascido aos 25 de julho de 1972 na cidade de Jales - SP, filho de Raymundo Venturini e Nair Bonin Venturini, portador da Cédula de Identidade RG nº 24.694.860 SSP/SP, inscrito no CPF/MF sob o nº 133.470.468-62, CNH Registro nº 01418205561 (DETRAN/SP), casado sob o regime da Comunhão Parcial de Bens na vigência da Lei Federal nº 6.515/77 (conforme Certidão de Casamento lavrada no Cartório de Registro Civil das Pessoas Naturais do 1º Subdistrito da Comarca de São José do Rio Preto - SP, Livro B nº 106, fls. 73, termo nº 12.678, celebrado em 15 de janeiro de 1994) com ")
    add_run_custom(p_v1, "MARILAINE OLIVEIRA SILVA VENTURINI", bold=True)
    add_run_custom(p_v1, ", brasileira, do lar, nascida aos 14 de outubro de 1974 na cidade de São José do Rio Preto - SP, filha de Eusebio Oliveira Silva e Maria Antonia Nunes Silva, portadora da Cédula de Identidade RG nº 25.067.901 SSP/SP, inscrita no CPF/MF sob o nº 121.790.318-66, CNH Registro nº 02130546417 (DETRAN/SP), ambos residentes e domiciliados à Rua Antonio Pirola, nº 123, Residencial Alto das Andorinhas, CEP 15046-231, na cidade de São José do Rio Preto - SP; e")

    # Inserir o parágrafo do Casal 2 logo abaixo de p_v1
    new_pv2 = docx.oxml.OxmlElement("w:p")
    p_v1._p.addnext(new_pv2)
    p_v2 = docx.text.paragraph.Paragraph(new_pv2, doc)
    set_p_format(p_v2)

    add_run_custom(p_v2, "2. WEBER REGINALDO DOS SANTOS", bold=True)
    add_run_custom(p_v2, ", brasileiro, empresário/comerciante, nascido aos 19 de julho de 1976 na cidade de Mauá - SP, filho de José Bonfim dos Santos e Clarice Venturini dos Santos, portador da Cédula de Identidade RG nº 22.806.400-4 SSP/SP e inscrito no CPF/MF sob o nº 151.990.938-19, casado sob o regime da Comunhão Universal de Bens (conforme Escritura Pública de Pacto Antenupcial lavrada perante o 4º Tabelião de Notas da Comarca de São José do Rio Preto - SP, Livro nº 0552, fls. 379, aos 15 de outubro de 2007; e assento de casamento sob Matrícula nº 115261 01 55 2007 3 00006 020 0001701 01 do 2º Oficial de Registro Civil das Pessoas Naturais de São José do Rio Preto - SP, Livro B-Aux nº 6, fls. 20, termo nº 1701, celebrado em 03 de novembro de 2007) com ")
    add_run_custom(p_v2, "PATRICIA FERNANDA DE MORAES BALDUINO DOS SANTOS", bold=True)
    add_run_custom(p_v2, ", brasileira, comerciante / do lar, nascida aos 06 de junho de 1980 na cidade de São José do Rio Preto - SP, filha de Orlando Balduino e Vera Lucia de Moraes Balduino, portadora da Cédula de Identidade RG nº 30.213.714-2 SSP/SP e inscrita no CPF/MF sob o nº 289.020.208-94, ambos residentes e domiciliados à Rua Direitos Humanos, nº 611, Bairro Residencial Ana Célia, CEP 15045-512, na cidade de São José do Rio Preto - SP.")

    # 3. Atualizar o bloco de assinaturas dos vendedores
    # Precisamos localizar novamente o parágrafo 'PROMITENTES VENDEDORES:' pois inserimos um parágrafo acima
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip().upper()
        if t == "PROMITENTES VENDEDORES:":
            idx_promitentes_vend_sig = i
        elif t == "PROMISSÁRIOS COMPRADORES:" or t == "PROMISSARIOS COMPRADORES:":
            if idx_promitentes_vend_sig and i > idx_promitentes_vend_sig:
                idx_promissarios_comp_sig = i
                break

    print(f"Novo índice Assinatura Vendedores: P{idx_promitentes_vend_sig}")
    print(f"Novo índice Assinatura Compradores: P{idx_promissarios_comp_sig}")

    # Entre idx_promitentes_vend_sig e idx_promissarios_comp_sig estão as linhas de assinatura anteriores.
    # Vamos limpar os parágrafos intermediários e reconstruir as assinaturas dos 4 vendedores.
    # Exemplo: doc.paragraphs[idx_promitentes_vend_sig + 1 ... idx_promissarios_comp_sig - 1]
    sig_paras = doc.paragraphs[idx_promitentes_vend_sig + 1 : idx_promissarios_comp_sig]
    print(f"Quantidade de parágrafos de assinatura a substituir: {len(sig_paras)}")

    # Vamos remover esses elementos do XML exceto o primeiro, ou reutilizar
    for p in sig_paras:
        p._p.getparent().remove(p._p)

    # Agora inserimos os 4 blocos de assinatura logo após 'PROMITENTES VENDEDORES:'
    p_anchor = doc.paragraphs[idx_promitentes_vend_sig]

    sellers_sigs = [
        ("ADEMIR VENTURINI", "133.470.468-62"),
        ("MARILAINE OLIVEIRA SILVA VENTURINI", "121.790.318-66"),
        ("WEBER REGINALDO DOS SANTOS", "151.990.938-19"),
        ("PATRICIA FERNANDA DE MORAES BALDUINO DOS SANTOS", "289.020.208-94")
    ]

    curr_p = p_anchor
    for name, cpf in sellers_sigs:
        # Linha
        np_line = docx.oxml.OxmlElement("w:p")
        curr_p._p.addnext(np_line)
        p_l = docx.text.paragraph.Paragraph(np_line, doc)
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.paragraph_format.space_before = Pt(12)
        p_l.paragraph_format.space_after = Pt(2)
        r = p_l.add_run("__________________________________________________")
        r.font.name = "Arial"
        curr_p = p_l

        # Nome
        np_name = docx.oxml.OxmlElement("w:p")
        curr_p._p.addnext(np_name)
        p_n = docx.text.paragraph.Paragraph(np_name, doc)
        p_n.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_n.paragraph_format.space_before = Pt(0)
        p_n.paragraph_format.space_after = Pt(2)
        r = p_n.add_run(name)
        r.bold = True
        r.font.name = "Arial"
        curr_p = p_n

        # CPF
        np_cpf = docx.oxml.OxmlElement("w:p")
        curr_p._p.addnext(np_cpf)
        p_c = docx.text.paragraph.Paragraph(np_cpf, doc)
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(14)
        r = p_c.add_run(f"CPF: {cpf}")
        r.font.name = "Arial"
        curr_p = p_c

    # 1. Salvar cópia atualizada completa com novo nome (para não conflitar se o Word estiver aberto)
    updated_name = "Contrato Compromisso Compra e Venda - Buona Vita - Reginaldo x João Roberto (Atualizado Completo).docx"
    updated_path = os.path.join(folder, updated_name)
    doc.save(updated_path)
    print(f"Contrato atualizado salvo em: {updated_path}")

    # 2. Espelhar cópias no Projeto e na pasta do Reginaldo
    proj_folder = r"c:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis"
    proj_target = os.path.join(proj_folder, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx")
    doc.save(proj_target)
    print(f"Cópia espelhada salva no Workspace: {proj_target}")

    reginaldo_mirror = os.path.join(folder, "Contrato_Compromisso_Compra_e_Venda_Buona_Vita_Ipe_da_Mata.docx")
    doc.save(reginaldo_mirror)
    print(f"Cópia espelhada salva na pasta Reginaldo: {reginaldo_mirror}")

    # 3. Tentar salvar no arquivo original se não estiver bloqueado pelo Word
    try:
        doc.save(filepath)
        print(f"Contrato oficial original sobrescrito com sucesso em: {filepath}")
    except PermissionError:
        print(f"Aviso: O arquivo original '{filepath}' está aberto no Word no momento. O arquivo '{updated_name}' foi salvo para visualização imediata!")

if __name__ == "__main__":
    update_contracts_with_all_sellers()
