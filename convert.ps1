$word = New-Object -ComObject Word.Application
$word.Visible = $false
$htmlPath = "$PSScriptRoot\Contrato_Locacao_Casa323.html"
$docxPath = "$PSScriptRoot\Contrato_Locacao_Casa323.docx"
$doc = $word.Documents.Open($htmlPath)
$doc.SaveAs2($docxPath, 16)
$doc.Close()
$word.Quit()
