import os
from PIL import Image, ImageDraw, ImageFont

def create_luxury_ad():
    # Canvas dimensions
    canvas_w, canvas_h = 1080, 1350
    
    # Create canvas and draw gradient background (Matte Luxury Black)
    base = Image.new('RGB', (canvas_w, canvas_h), '#080808')
    draw = ImageDraw.Draw(base)
    
    # Smooth vertical gradient (matte luxury black)
    for y in range(canvas_h):
        r = int(18 - (13 * y / canvas_h))
        g = int(18 - (13 * y / canvas_h))
        b = int(18 - (13 * y / canvas_h))
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
        font_eyebrow = ImageFont.truetype(font_path_sans_bold, 13)
        font_title = ImageFont.truetype(font_path_serif, 58)
        font_section_title = ImageFont.truetype(font_path_sans_bold, 15)
        font_feature = ImageFont.truetype(font_path_sans, 19)
        font_price_lbl = ImageFont.truetype(font_path_sans_bold, 12)
        font_price = ImageFont.truetype(font_path_serif, 48)
        font_price_fees = ImageFont.truetype(font_path_sans, 15)
        font_broker_name = ImageFont.truetype(font_path_serif, 24)
        font_broker_creci = ImageFont.truetype(font_path_sans, 13)
        font_broker_phone = ImageFont.truetype(font_path_sans_bold, 32)
        font_broker_web = ImageFont.truetype(font_path_sans, 15)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        font_eyebrow = font_title = font_section_title = font_feature = font_price_lbl = font_price = font_price_fees = font_broker_name = font_broker_creci = font_broker_phone = font_broker_web = ImageFont.load_default()

    # Premium Color Palette (Understated Luxury: Pure White, Platinum Grey, Champagne Accent)
    color_white = (255, 255, 255)
    color_platinum = (220, 220, 220)
    color_grey_muted = (140, 140, 140)
    color_champagne = (220, 203, 163) # Subtle champagne gold tone for small details
    
    # NO OUTER BORDER - Keep it completely borderless and clean
    
    # --- HEADER ---
    # Centered or clean left-aligned. Let's do a very clean left-aligned layout with generous margins (80px)
    margin_x = 80
    
    draw.text((margin_x, 65), "APRESENTAMOS", fill=color_champagne, font=font_eyebrow)
    draw.text((margin_x, 90), "ALTOS DE IBORUNA", fill=color_white, font=font_title)
    
    # --- LEFT COLUMN: BUILDING PHOTO ---
    # Width: 460px, Height: 760px. Located at x=80, y=180.
    bldg_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna\Altos_Iboruna_Fachada.jpg"
    if os.path.exists(bldg_path):
        bldg_img = Image.open(bldg_path)
        bldg_w, bldg_h = 460, 818
        bldg_img_resized = bldg_img.resize((bldg_w, bldg_h), Image.Resampling.LANCZOS)
        # Crop to exactly 460x760 (keep the bottom details, remove top 35px)
        bldg_cropped = bldg_img_resized.crop((0, 35, 460, 795))
        
        base.paste(bldg_cropped, (margin_x, 180))
        # Clean, borderless layout (NO border around the image)
    else:
        draw.rectangle([(margin_x, 180), (margin_x + 460, 940)], fill=(25,25,25))
        
    # --- RIGHT COLUMN: SOPHISTICATED DETAILS ---
    col2_x = 590
    
    # Section 1: O Imóvel
    draw.text((col2_x, 180), "O APARTAMENTO", fill=color_champagne, font=font_section_title)
    
    apt_details = [
        "02 dormitórios, sendo 1 suíte de alto padrão",
        "Living amplo integrado para dois ambientes",
        "Sacada privativa com vista livre",
        "Cozinha integrada com planejados",
        "Piso refinado em porcelanato",
        "01 vaga de garagem"
    ]
    
    y_offset = 215
    for text in apt_details:
        # Instead of bullet points, use a very elegant, clean layout with high line-height
        # Draw a tiny elegant vertical line or just text
        draw.text((col2_x, y_offset), text, fill=color_platinum, font=font_feature)
        y_offset += 34
        
    # Section 2: O Lazer
    y_offset += 25
    draw.text((col2_x, y_offset), "LAZER E CONVENIÊNCIA", fill=color_champagne, font=font_section_title)
    
    condo_details = [
        "Piscina, academia e quiosque gourmet",
        "Salão de festas e brinquedoteca",
        "Área verde preservada e mercadinho",
        "Segurança corporativa com portaria 24h"
    ]
    
    y_offset += 35
    for text in condo_details:
        draw.text((col2_x, y_offset), text, fill=color_platinum, font=font_feature)
        y_offset += 34
        
    # Section 3: Investimento
    y_offset += 35
    draw.text((col2_x, y_offset), "INVESTIMENTO EXCLUSIVO", fill=color_grey_muted, font=font_price_lbl)
    
    y_offset += 15
    draw.text((col2_x, y_offset), "R$ 400.000,00", fill=color_white, font=font_price)
    
    y_offset += 60
    fees_text = "Condomínio: R$ 430,00  •  IPTU: R$ 60,00 / mês"
    draw.text((col2_x, y_offset), fees_text, fill=color_grey_muted, font=font_price_fees)
    
    # --- FOOTER: SEPARATOR (Very subtle, dark line) ---
    draw.line([(margin_x, 980), (1000, 980)], fill=(38, 38, 38), width=1)
    
    # --- FOOTER: BROKER AND CONTACTS (USING OPTION 4 PHOTO) ---
    broker_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Fotos"
    broker_photo = "Foto com a mão na perna.jpg" # Option 4
    broker_path = os.path.join(broker_dir, broker_photo)
    
    broker_x, broker_y = margin_x, 1010
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
        
        # Platinum/Grey circle outline (very thin and subtle, no gold)
        draw.ellipse(
            [(broker_x - 1, broker_y - 1), (broker_x + broker_size + 1, broker_y + broker_size + 1)],
            outline=(50, 50, 50),
            width=1
        )
    else:
        draw.ellipse([(broker_x, broker_y), (broker_x + broker_size, broker_y + broker_size)], fill=(30,30,30))
        
    # Broker Info
    text_x = broker_x + broker_size + 30
    draw.text((text_x, broker_y + 15), "VALTEIR DE OLIVEIRA", fill=color_white, font=font_broker_name)
    draw.text((text_x, broker_y + 47), "Assessoria Imobiliária de Alto Padrão  |  CRECI 214072-F", fill=color_grey_muted, font=font_broker_creci)
    
    phone_text = "(17) 99172-6078"
    draw.text((text_x, broker_y + 75), phone_text, fill=color_white, font=font_broker_phone)
    
    # WhatsApp indicator (subtle champagne gold dot, very elegant)
    draw.ellipse([(text_x, broker_y + 122), (text_x + 8, broker_y + 130)], fill=color_champagne)
    draw.text((text_x + 16, broker_y + 116), "Atendimento online via WhatsApp", fill=color_grey_muted, font=font_broker_web)
    
    draw.text((text_x, broker_y + 145), "www.valteir.com.br", fill=color_champagne, font=font_broker_web)
    
    # Transparent Logo (No white card)
    logo_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Desing System\Logotipo_Valteir_Oliveira_Sem_Fundo.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_w, logo_h = 220, 100
        logo_x, logo_y = 780, 1050
        
        logo_img_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        # Paste with transparent mask
        base.paste(logo_img_resized, (logo_x, logo_y), mask=logo_img_resized)
        
    # Save output
    output_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna"
    output_path = os.path.join(output_dir, "anuncio_altos_iboruna_luxo.png")
    base.save(output_path, 'PNG')
    print(f"Luxury ad generated successfully: {output_path}")

if __name__ == "__main__":
    create_luxury_ad()
