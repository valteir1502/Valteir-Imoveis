import os
from PIL import Image, ImageDraw, ImageFont

base_dir = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis\Logos_Novas"
os.makedirs(base_dir, exist_ok=True)

# 1. CORES DE GRADIENTE DOURADO REAL
def get_gold_color(t):
    if t < 0.35:
        sub_t = t / 0.35
        r = int(246 + sub_t * (212 - 246))
        g = int(229 + sub_t * (175 - 229))
        b = int(156 + sub_t * (55 - 156))
    elif t < 0.7:
        sub_t = (t - 0.35) / 0.35
        r = int(212 + sub_t * (154 - 212))
        g = int(175 + sub_t * (110 - 175))
        b = int(55 + sub_t * (22 - 55))
    else:
        sub_t = (t - 0.7) / 0.3
        r = int(154 + sub_t * (232 - 154))
        g = int(110 + sub_t * (200 - 110))
        b = int(22 + sub_t * (98 - 22))
    return (r, g, b, 255)

# 2. DESENHO DO MONOGRAMA (ÍCONE)
def draw_symbol(w, h, cx, cy, rx, ry, thickness):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Máscara do Anel Oval
    mask_ring = Image.new("L", (w, h), 0)
    draw_ring = ImageDraw.Draw(mask_ring)

    draw_ring.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    draw_ring.ellipse((cx - (rx - thickness), cy - (ry - thickness), cx + (rx - thickness), cy + (ry - thickness)), fill=0)

    gap_w = int(rx * 0.40)
    draw_ring.rectangle((cx - gap_w, cy - ry - 10, cx + gap_w, cy - ry + thickness + 10), fill=0)
    draw_ring.rectangle((cx - gap_w, cy + ry - thickness - 10, cx + gap_w, cy + ry + 10), fill=0)

    ring_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        col = get_gold_color(y / h)
        line_draw = ImageDraw.Draw(ring_img)
        line_draw.line((0, y, w, y), fill=col)

    img.paste(ring_img, (0, 0), mask_ring)

    # Letra V
    v_top_y = cy - int(ry * 1.16)
    v_bot_y = cy + int(ry * 0.90)
    v_width = int(rx * 1.1)
    v_thick = int(thickness * 1.05)

    left_poly = [
        (cx - v_width, v_top_y),
        (cx - v_width + v_thick, v_top_y),
        (cx, v_bot_y),
        (cx - int(v_thick * 0.6), v_bot_y)
    ]
    right_poly = [
        (cx + v_width, v_top_y),
        (cx + v_width - v_thick, v_top_y),
        (cx, v_bot_y),
        (cx + int(v_thick * 0.6), v_bot_y)
    ]
    bevel_poly = [
        (cx - v_width + v_thick, v_top_y),
        (cx - v_width + int(v_thick * 1.35), v_top_y),
        (cx, v_bot_y),
        (cx, v_bot_y)
    ]

    draw.polygon(left_poly, fill=(28, 30, 38, 255), outline=(212, 175, 55, 255))
    draw.polygon(right_poly, fill=(20, 21, 26, 255), outline=(212, 175, 55, 255))
    draw.polygon(bevel_poly, fill=(242, 215, 133, 240))

    return img

# 3. GERAR COMPOSIÇÃO HORIZONTAL
def draw_horizontal_logo():
    scale = 4
    w = 2400 * scale
    h = 800 * scale
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # Símbolo à esquerda
    sym = draw_symbol(w, h, 400 * scale, 400 * scale, 240 * scale, 310 * scale, 45 * scale)
    img.paste(sym, (0, 0), sym)

    draw = ImageDraw.Draw(img)
    font_valteir = ImageFont.truetype(r"C:\Windows\Fonts\georgiab.ttf", 190 * scale)
    font_imoveis = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 70 * scale)

    # Texto VALTEIR
    # Letter spacing manual
    text_valteir = "VALTEIR"
    start_x = 750 * scale
    y_valteir = 230 * scale
    x = start_x
    for char in text_valteir:
        draw.text((x, y_valteir), char, font=font_valteir, fill=(212, 175, 55, 255))
        # Adicionar espaçamento nobre
        bbox = draw.textbbox((x, y_valteir), char, font=font_valteir)
        x += (bbox[2] - bbox[0]) + (35 * scale)

    # Linha divisória dourada
    draw.line((start_x, 465 * scale, x - 35 * scale, 465 * scale), fill=(212, 175, 55, 180), width=4 * scale)

    # Texto IMÓVEIS
    text_imoveis = "I M Ó V E I S"
    draw.text((start_x + 5 * scale, 490 * scale), text_imoveis, font=font_imoveis, fill=(235, 210, 130, 255))

    # Redimensionar para tamanho final HD
    final_hd = img.resize((2400, 800), Image.Resampling.LANCZOS)
    final_hd.save(os.path.join(base_dir, "logo_valteir_vetorial_horizontal_puro_HD.png"), "PNG")
    print("Horizontal HD gerado com sucesso!")

draw_horizontal_logo()
