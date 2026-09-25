import re

def md_to_html(md_text):
    html = md_text
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
    # Headers
    html = re.sub(r'(?m)^# (.*?)$', r'<h1>\1</h1>', html)
    # Paragraphs
    paragraphs = html.split('\n\n')
    html = ''.join([f'<p>{p}</p>' if not p.startswith('<h') else p for p in paragraphs])
    return f"<html><head><meta charset='utf-8'></head><body>{html}</body></html>"

with open('Contrato_Locacao_Casa323.md', 'r', encoding='utf-8') as f:
    md = f.read()

html = md_to_html(md)

with open('Contrato_Locacao_Casa323.html', 'w', encoding='utf-8') as f:
    f.write(html)
