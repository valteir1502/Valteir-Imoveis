import os
from PIL import Image, ImageDraw, ImageFont

def create_sophisticated_ad():
    # Canvas dimensions
    canvas_w, canvas_h = 1080, 1350
    
    # Create canvas and draw gradient background
    base = Image.new('RGB', (canvas_w, canvas_h), '#0a0a0a')
    draw = ImageDraw.Draw(base)
    
    for y in range(canvas_h):
        # Premium dark gradient: from #181818 (24, 24, 24) to #0c0c0c (12, 12, 12)
        r = int(24 - (12 * y / canvas_h))
        g = int(24 - (12 * y / canvas_h))
        b = int(24 - (12 * y / canvas_h))
        draw.line([(0, y), (canvas_w, y)], fill=(r, g, b))
        
    # Fonts
    font_path_serif = r"C:\Windows\Fonts\georgiab.ttf"
    font_path_sans = r"C:\Windows\Fonts\calibri.ttf"
    font_path_sans_bold = r"C:\Windows\Fonts\calibrib.ttf"
    
    if not os.path.exists(font_path_serif): font_path_serif = "arial.ttf"
    if not os.path.exists(font_path_sans): font_path_sans = "arial.ttf"
    if not os.path.exists(font_path_sans_bold): font_path_sans_bold = "arial.ttf"
    
    # Load fonts
    try:
        font_eyebrow = ImageFont.truetype(font_path_sans_bold, 14)
        font_title = ImageFont.truetype(font_path_serif, 56)
        font_section_title = ImageFont.truetype(font_path_sans_bold, 16)
        font_feature = ImageFont.truetype(font_path_sans, 18)
        font_price_lbl = ImageFont.truetype(font_path_sans_bold, 13)
        font_price = ImageFont.truetype(font_path_serif, 46)
        font_price_fees = ImageFont.truetype(font_path_sans, 15)
        font_broker_name = ImageFont.truetype(font_path_serif, 24)
        font_broker_creci = ImageFont.truetype(font_path_sans, 13)
        font_broker_phone = ImageFont.truetype(font_path_sans_bold, 32)
        font_broker_web = ImageFont.truetype(font_path_sans, 15)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        font_eyebrow = font_title = font_section_title = font_feature = font_price_lbl = font_price = font_price_fees = font_broker_name = font_broker_creci = font_broker_phone = font_broker_web = ImageFont.load_default()

    # Colors
    color_gold = (201, 168, 76)      # #C9A84C
    color_gold_light = (229, 201, 115) # #E5C973
    color_white = (255, 255, 255)
    color_grey = (160, 160, 160)
    
    # Draw double gold border (Very premium luxury style)
    # Outer border
    draw.rectangle([(25, 25), (canvas_w - 25, canvas_h - 25)], outline=color_gold, width=2)
    # Inner border
    draw.rectangle([(32, 32), (canvas_w - 32, canvas_h - 32)], outline=color_gold, width=1)
    
    # --- HEADER ---
    draw.text((65, 60), "OPORTUNIDADE EXCLUSIVA", fill=color_gold, font=font_eyebrow)
    draw.text((65, 85), "ALTOS DE IBORUNA", fill=color_white, font=font_title)
    
    # --- LEFT COLUMN: BUILDING PHOTO ---
    bldg_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna\Altos_Iboruna_Fachada.jpg"
    if os.path.exists(bldg_path):
        bldg_img = Image.open(bldg_path)
        # Resize to fit a slightly wider frame: 470 width, 760 height
        bldg_w, bldg_h = 470, 836
        bldg_img_resized = bldg_img.resize((bldg_w, bldg_h), Image.Resampling.LANCZOS)
        # Crop from (0, 38) to (470, 798) to get exactly 470x760
        bldg_cropped = bldg_img_resized.crop((0, 38, 470, 798))
        
        base.paste(bldg_cropped, (65, 170))
        # Gold frame around building photo
        draw.rectangle([(65, 170), (535, 930)], outline=color_gold, width=2)
    else:
        draw.rectangle([(65, 170), (535, 930)], fill=(40,40,40), outline=color_gold, width=2)
        
    # --- RIGHT COLUMN: SOPIHSTICATED DETAILS ---
    col2_x = 575
    
    # Section 1: O Apartamento
    draw.text((col2_x, 170), "O APARTAMENTO", fill=color_gold, font=font_section_title)
    
    apt_details = [
        "02 Dormitórios (sendo 1 Suíte)",
        "Sala ampla para 2 ambientes com sacada",
        "Cozinha com armários planejados",
        "Acabamento refinado em porcelanato",
        "01 Vaga de garagem coberta"
    ]
    
    y_offset = 205
    for text in apt_details:
        # Draw a small elegant dash instead of a heavy box
        draw.line([(col2_x, y_offset + 11), (col2_x + 8, y_offset + 11)], fill=color_gold, width=2)
        draw.text((col2_x + 18, y_offset), text, fill=color_white, font=font_feature)
        y_offset += 34
        
    # Section 2: O Condomínio
    y_offset += 25
    draw.text((col2_x, y_offset), "LIFESTYLE E LAZER", fill=color_gold, font=font_section_title)
    
    condo_details = [
        "Piscina, academia e quiosque gourmet",
        "Brinquedoteca e salão de festas",
        "Área verde integrada e mercadinho",
        "Portaria com segurança 24h"
    ]
    
    y_offset += 35
    for text in condo_details:
        draw.line([(col2_x, y_offset + 11), (col2_x + 8, y_offset + 11)], fill=color_gold, width=2)
        draw.text((col2_x + 18, y_offset), text, fill=color_white, font=font_feature)
        y_offset += 34
        
    # Section 3: Investimento
    y_offset += 35
    draw.text((col2_x, y_offset), "INVESTIMENTO", fill=color_gold, font=font_price_lbl)
    
    y_offset += 20
    draw.text((col2_x, y_offset), "R$ 400.000,00", fill=color_gold_light, font=font_price)
    
    y_offset += 60
    fees_text = "Condomínio: R$ 430,00  •  IPTU: R$ 60,00/mês"
    draw.text((col2_x, y_offset), fees_text, fill=color_grey, font=font_price_fees)
    
    # --- FOOTER: SEPARATOR ---
    draw.line([(65, 965), (1015, 965)], fill=color_gold, width=1)
    
    # --- FOOTER: BROKER AND CONTACTS (USING OPTION 4 PHOTO) ---
    broker_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Fotos"
    broker_photo = "Foto com a mão na perna.jpg" # Option 4
    broker_path = os.path.join(broker_dir, broker_photo)
    
    broker_x, broker_y = 65, 985
    broker_size = 180
    
    if os.path.exists(broker_path):
        br_img = Image.open(broker_path)
        br_w, br_h = br_img.size
        # Upper body crop for "Foto com a mão na perna"
        crop_box = (900, 300, 2700, 2100)
        
        br_cropped = br_img.crop(crop_box)
        br_cropped = br_cropped.resize((broker_size, broker_size), Image.Resampling.LANCZOS)
        
        # Circle mask
        mask = Image.new('L', (broker_size, broker_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, broker_size, broker_size), fill=255)
        
        avatar = Image.new('RGBA', (broker_size, broker_size), (0,0,0,0))
        avatar.paste(br_cropped, (0, 0), mask=mask)
        
        base.paste(avatar, (broker_x, broker_y), mask=avatar)
        
        # Gold circle outline
        draw.ellipse(
            [(broker_x - 1, broker_y - 1), (broker_x + broker_size + 1, broker_y + broker_size + 1)],
            outline=color_gold,
            width=2
        )
    else:
        draw.ellipse([(broker_x, broker_y), (broker_x + broker_size, broker_y + broker_size)], fill=(40,40,40), outline=color_gold, width=2)
        
    # Broker Info
    text_x = broker_x + broker_size + 30
    draw.text((text_x, broker_y + 15), "VALTEIR DE OLIVEIRA", fill=color_gold, font=font_broker_name)
    draw.text((text_x, broker_y + 47), "Assessoria Imobiliária  |  CRECI 214072-F", fill=color_grey, font=font_broker_creci)
    
    phone_text = "(17) 99172-6078"
    draw.text((text_x, broker_y + 75), phone_text, fill=color_white, font=font_broker_phone)
    
    # WhatsApp indicator
    draw.rectangle([(text_x, broker_y + 120), (text_x + 10, broker_y + 130)], fill=(37, 211, 102))
    draw.text((text_x + 18, broker_y + 115), "Atendimento online via WhatsApp", fill=(37, 211, 102), font=font_broker_web)
    
    draw.text((text_x, broker_y + 145), "www.valteir.com.br", fill=color_gold, font=font_broker_web)
    
    # Logo card
    logo_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Desing System\Logotipo Valteir Oliveira 2.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        card_w, card_h = 220, 100
        card_x, card_y = 765, 1025
        
        # White card for logo
        draw.rectangle(
            [(card_x, card_y), (card_x + card_w, card_y + card_h)],
            fill=(255, 255, 255),
            outline=color_gold,
            width=2
        )
        
        logo_w, logo_h = card_w - 20, card_h - 20
        logo_img_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        base.paste(logo_img_resized, (card_x + 10, card_y + 10))
        
    # Save output
    output_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna"
    output_path = os.path.join(output_dir, "anuncio_altos_iboruna_sofisticado.png")
    base.save(output_path, 'PNG')
    print(f"Sophisticated ad generated successfully: {output_path}")

if __name__ == "__main__":
    create_sophisticated_ad()
