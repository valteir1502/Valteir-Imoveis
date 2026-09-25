import os
from PIL import Image, ImageDraw, ImageFont

def create_rental_ad():
    # Canvas dimensions
    canvas_w, canvas_h = 1080, 1350
    
    # Create canvas and draw gradient background (Matte Luxury Black)
    base = Image.new('RGB', (canvas_w, canvas_h), '#080808')
    draw = ImageDraw.Draw(base)
    
    # Smooth vertical gradient
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
        font_title = ImageFont.truetype(font_path_serif, 48)
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

    # Colors
    color_white = (255, 255, 255)
    color_platinum = (220, 220, 220)
    color_grey_muted = (140, 140, 140)
    color_champagne = (220, 203, 163) # Champagne gold tone
    
    # Margin
    margin_x = 80
    
    # --- HEADER ---
    draw.text((margin_x, 65), "CASA EM CONDOMÍNIO PARA LOCAÇÃO", fill=color_champagne, font=font_eyebrow)
    draw.text((margin_x, 90), "PARQUE DA LIBERDADE II", fill=color_white, font=font_title)
    
    # --- LEFT COLUMN: INTERNAL PROPERTY PHOTO ---
    photo_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Locacao_Premium\Locacao_Interna.jpg"
    if os.path.exists(photo_path):
        img = Image.open(photo_path)
        img_w, img_h = 460, 818
        img_resized = img.resize((img_w, img_h), Image.Resampling.LANCZOS)
        # Crop to exactly 460x760 (removes 29px from top and bottom)
        cropped = img_resized.crop((0, 29, 460, 789))
        
        base.paste(cropped, (margin_x, 180))
        # Clean, borderless frame
    else:
        draw.rectangle([(margin_x, 180), (margin_x + 460, 940)], fill=(25,25,25))
        
    # --- RIGHT COLUMN: DETAILS ---
    col2_x = 590
    
    # Section 1: O Imóvel
    draw.text((col2_x, 180), "O APARTAMENTO / CASA", fill=color_champagne, font=font_section_title)
    
    details = [
        "03 Dormitórios, sendo 1 suíte",
        "Todos equipados com armários",
        "Ar condicionado instalado nos quartos",
        "Sala de estar e recepção ampla",
        "Cozinha com armários modernos",
        "Espaço gourmet integrado e privativo"
    ]
    
    y_offset = 215
    for text in details:
        draw.text((col2_x, y_offset), text, fill=color_platinum, font=font_feature)
        y_offset += 34
        
    # Section 2: O Condomínio
    y_offset += 25
    draw.text((col2_x, y_offset), "CONFORTO E SEGURANÇA", fill=color_champagne, font=font_section_title)
    
    condo_details = [
        "Localização exclusiva e privilegiada",
        "Condomínio com área de lazer",
        "Portaria e segurança 24h"
    ]
    
    y_offset += 35
    for text in condo_details:
        draw.text((col2_x, y_offset), text, fill=color_platinum, font=font_feature)
        y_offset += 34
        
    # Section 3: Preço
    y_offset += 45
    draw.text((col2_x, y_offset), "VALOR MENSAL (PACOTE COMPLETO)", fill=color_grey_muted, font=font_price_lbl)
    
    y_offset += 15
    draw.text((col2_x, y_offset), "R$ 2.500,00", fill=color_white, font=font_price)
    
    y_offset += 60
    draw.text((col2_x, y_offset), "Incluso: Aluguel + Condomínio + IPTU", fill=color_grey_muted, font=font_price_fees)
    
    # --- FOOTER: SEPARATOR ---
    draw.line([(margin_x, 980), (1000, 980)], fill=(38, 38, 38), width=1)
    
    # --- FOOTER: BROKER AND CONTACTS (USING OPTION 4 PHOTO) ---
    broker_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Fotos"
    broker_photo = "Foto com a mão na perna.jpg" # Option 4
    broker_path = os.path.join(broker_dir, broker_photo)
    
    broker_x, broker_y = margin_x, 1010
    broker_size = 180
    
    if os.path.exists(broker_path):
        br_img = Image.open(broker_path)
        crop_box = (900, 300, 2700, 2100)
        
        br_cropped = br_img.crop(crop_box)
        br_cropped = br_cropped.resize((broker_size, broker_size), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (broker_size, broker_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, broker_size, broker_size), fill=255)
        
        avatar = Image.new('RGBA', (broker_size, broker_size), (0,0,0,0))
        avatar.paste(br_cropped, (0, 0), mask=mask)
        base.paste(avatar, (broker_x, broker_y), mask=avatar)
        
        # Subtle border around avatar
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
    
    # WhatsApp dot
    draw.ellipse([(text_x, broker_y + 122), (text_x + 8, broker_y + 130)], fill=color_champagne)
    draw.text((text_x + 16, broker_y + 116), "Atendimento online via WhatsApp", fill=color_grey_muted, font=font_broker_web)
    
    draw.text((text_x, broker_y + 145), "www.valteir.com.br", fill=color_champagne, font=font_broker_web)
    
    # Logo (Transparent logo)
    logo_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Desing System\Logotipo_Valteir_Oliveira_Sem_Fundo.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_w, logo_h = 220, 100
        card_x, card_y = 780, 1050
        
        # Transparent logo paste directly
        logo_img_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        base.paste(logo_img_resized, (card_x, card_y), mask=logo_img_resized)
        
    # Save output
    output_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Locacao_Premium"
    output_path = os.path.join(output_dir, "anuncio_locacao_premium.png")
    base.save(output_path, 'PNG')
    print(f"Rental ad generated successfully: {output_path}")

if __name__ == "__main__":
    create_rental_ad()
