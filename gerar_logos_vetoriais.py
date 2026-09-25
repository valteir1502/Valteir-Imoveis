import os
from PIL import Image

# 1. DESIGN VETORIAL PURO (SVG) - ALTA JOALHERIA & IMOBILIÁRIA DE LUXO
# Sem IA, sem borrão, pura geometria matemática e curvas perfeitas

svg_vertical = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <defs>
    <!-- Gradiente Ouro Escovado Puro -->
    <linearGradient id="goldPure" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F2D785" />
      <stop offset="30%" stop-color="#D4AF37" />
      <stop offset="70%" stop-color="#AA7C11" />
      <stop offset="100%" stop-color="#E2BA4B" />
    </linearGradient>

    <!-- Gradiente Titânio / Ônix Nobre -->
    <linearGradient id="titaniumPure" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2C2E38" />
      <stop offset="50%" stop-color="#14151B" />
      <stop offset="100%" stop-color="#050608" />
    </linearGradient>
  </defs>

  <!-- SÍMBOLO: Anel Oval Geométrico + Letra V em Proporção Áurea -->
  <g id="simbolo" transform="translate(500, 360)">
    <!-- Metade Esquerda do Anel Oval Dourado -->
    <path d="M -90,-180 C -190,-180 -190,180 -90,180 C -40,180 -15,145 -15,145 L -45,120 C -45,120 -60,140 -90,140 C -150,140 -150,-140 -90,-140 C -60,-140 -45,-120 -45,-120 L -15,-145 C -15,-145 -40,-180 -90,-180 Z" fill="url(#goldPure)" />
    
    <!-- Metade Direita do Anel Oval Dourado -->
    <path d="M 90,-180 C 190,-180 190,180 90,180 C 40,180 15,145 15,145 L 45,120 C 45,120 60,140 90,140 C 150,140 150,-140 90,-140 C 60,-140 45,-120 45,-120 L 15,-145 C 15,-145 40,-180 90,-180 Z" fill="url(#goldPure)" />

    <!-- Letra V em Titânio Ônix com Borda Ouro -->
    <!-- Haste Esquerda do V -->
    <polygon points="-125,-210 -70,-210 0,165 -35,165" fill="url(#titaniumPure)" stroke="url(#goldPure)" stroke-width="4" stroke-linejoin="round" />
    
    <!-- Haste Direita do V -->
    <polygon points="125,-210 70,-210 0,165 35,165" fill="url(#titaniumPure)" stroke="url(#goldPure)" stroke-width="4" stroke-linejoin="round" />
    
    <!-- Chanfro de Luz Dourado no V -->
    <polygon points="-70,-210 -90,-210 0,165 0,165" fill="url(#goldPure)" opacity="0.85" />
  </g>

  <!-- TIPOGRAFIA PURA & ELEGANTE -->
  <g id="texto" transform="translate(500, 710)" text-anchor="middle">
    <!-- VALTEIR -->
    <text x="0" y="0" font-family="'Cinzel', 'Trajan Pro', 'Cinzel Decorative', 'Georgia', serif" font-size="88" font-weight="700" letter-spacing="18" fill="url(#goldPure)">VALTEIR</text>
    
    <!-- DIVISOR DOURADO FINO -->
    <line x1="-160" y1="36" x2="160" y2="36" stroke="url(#goldPure)" stroke-width="2" opacity="0.6" />

    <!-- IMÓVEIS -->
    <text x="0" y="82" font-family="'Montserrat', 'Helvetica Neue', 'Arial', sans-serif" font-size="34" font-weight="500" letter-spacing="24" fill="#D4AF37">IMÓVEIS</text>
  </g>
</svg>"""

# 2. DESIGN VETORIAL HORIZONTAL (Perfeito para cabeçalho de site, cartão, fachada)
svg_horizontal = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 500" width="100%" height="100%">
  <defs>
    <linearGradient id="goldPureH" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F2D785" />
      <stop offset="30%" stop-color="#D4AF37" />
      <stop offset="70%" stop-color="#AA7C11" />
      <stop offset="100%" stop-color="#E2BA4B" />
    </linearGradient>
    <linearGradient id="titaniumPureH" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2C2E38" />
      <stop offset="50%" stop-color="#14151B" />
      <stop offset="100%" stop-color="#050608" />
    </linearGradient>
  </defs>

  <!-- SÍMBOLO À ESQUERDA -->
  <g id="simbolo" transform="translate(250, 250) scale(0.85)">
    <path d="M -90,-180 C -190,-180 -190,180 -90,180 C -40,180 -15,145 -15,145 L -45,120 C -45,120 -60,140 -90,140 C -150,140 -150,-140 -90,-140 C -60,-140 -45,-120 -45,-120 L -15,-145 C -15,-145 -40,-180 -90,-180 Z" fill="url(#goldPureH)" />
    <path d="M 90,-180 C 190,-180 190,180 90,180 C 40,180 15,145 15,145 L 45,120 C 45,120 60,140 90,140 C 150,140 150,-140 90,-140 C 60,-140 45,-120 45,-120 L 15,-145 C 15,-145 40,-180 90,-180 Z" fill="url(#goldPureH)" />
    <polygon points="-125,-210 -70,-210 0,165 -35,165" fill="url(#titaniumPureH)" stroke="url(#goldPureH)" stroke-width="4" stroke-linejoin="round" />
    <polygon points="125,-210 70,-210 0,165 35,165" fill="url(#titaniumPureH)" stroke="url(#goldPureH)" stroke-width="4" stroke-linejoin="round" />
    <polygon points="-70,-210 -90,-210 0,165 0,165" fill="url(#goldPureH)" opacity="0.85" />
  </g>

  <!-- TEXTO À DIREITA -->
  <g id="texto" transform="translate(500, 230)">
    <text x="0" y="20" font-family="'Cinzel', 'Trajan Pro', 'Georgia', serif" font-size="115" font-weight="700" letter-spacing="14" fill="url(#goldPureH)">VALTEIR</text>
    <line x1="5" y1="58" x2="680" y2="58" stroke="url(#goldPureH)" stroke-width="2.5" opacity="0.6" />
    <text x="5" y="110" font-family="'Montserrat', 'Helvetica Neue', sans-serif" font-size="44" font-weight="500" letter-spacing="28" fill="#D4AF37">IMÓVEIS</text>
  </g>
</svg>"""

# 3. DESIGN VETORIAL MONOGRAMA / ÍCONE 100x100 (Geometria Pura)
svg_icone = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" height="100%">
  <defs>
    <linearGradient id="goldPureIcon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F2D785" />
      <stop offset="30%" stop-color="#D4AF37" />
      <stop offset="70%" stop-color="#AA7C11" />
      <stop offset="100%" stop-color="#E2BA4B" />
    </linearGradient>
    <linearGradient id="titaniumPureIcon" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2C2E38" />
      <stop offset="50%" stop-color="#14151B" />
      <stop offset="100%" stop-color="#050608" />
    </linearGradient>
  </defs>

  <g id="simbolo" transform="translate(250, 250) scale(0.95)">
    <path d="M -90,-180 C -190,-180 -190,180 -90,180 C -40,180 -15,145 -15,145 L -45,120 C -45,120 -60,140 -90,140 C -150,140 -150,-140 -90,-140 C -60,-140 -45,-120 -45,-120 L -15,-145 C -15,-145 -40,-180 -90,-180 Z" fill="url(#goldPureIcon)" />
    <path d="M 90,-180 C 190,-180 190,180 90,180 C 40,180 15,145 15,145 L 45,120 C 45,120 60,140 90,140 C 150,140 150,-140 90,-140 C 60,-140 45,-120 45,-120 L 15,-145 C 15,-145 40,-180 90,-180 Z" fill="url(#goldPureIcon)" />
    <polygon points="-125,-210 -70,-210 0,165 -35,165" fill="url(#titaniumPureIcon)" stroke="url(#goldPureIcon)" stroke-width="4" stroke-linejoin="round" />
    <polygon points="125,-210 70,-210 0,165 35,165" fill="url(#titaniumPureIcon)" stroke="url(#goldPureIcon)" stroke-width="4" stroke-linejoin="round" />
    <polygon points="-70,-210 -90,-210 0,165 0,165" fill="url(#goldPureIcon)" opacity="0.85" />
  </g>
</svg>"""

out_dir = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis\Logos_Novas"
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "logo_valteir_vetorial_vertical.svg"), "w", encoding="utf-8") as f:
    f.write(svg_vertical)

with open(os.path.join(out_dir, "logo_valteir_vetorial_horizontal.svg"), "w", encoding="utf-8") as f:
    f.write(svg_horizontal)

with open(os.path.join(out_dir, "logo_valteir_vetorial_icone.svg"), "w", encoding="utf-8") as f:
    f.write(svg_icone)

print("Todos os SVGs vetoriais profissionais foram gerados com sucesso!")
