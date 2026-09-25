import win32com.client
import os

html_path = os.path.abspath('Contrato_Locacao_Casa323.html')
docx_path = os.path.abspath('Contrato_Locacao_Casa323.docx')

try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(html_path)
    doc.SaveAs(docx_path, 16)
    doc.Close()
    word.Quit()
    print("Success")
except Exception as e:
    print("Error:", e)
    try:
        word.Quit()
    except:
        pass
