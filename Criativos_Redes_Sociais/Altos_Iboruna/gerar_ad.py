import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

def create_ad(broker_photo_name, output_name):
    # Canvas properties
    canvas_w, canvas_h = 1080, 1350
    
    # Create main canvas
    # Background: Elegant gradient dark grey to black
    base = Image.new('RGB', (canvas_w, canvas_h), '#0a0a0a')
    draw = ImageDraw.Draw(base)
    
    # Draw horizontal gradient manually
    # Let's make a beautiful linear gradient from top to bottom
    for y in range(canvas_h):
        # Interpolate color from #1a1a1a (26,26,26) to #0d0d0d (13,13,13)
        r = int(26 - (13 * y / canvas_h))
        g = int(26 - (13 * y / canvas_h))
        b = int(26 - (13 * y / canvas_h))
        draw.line([(0, y), (canvas_w, y)], fill=(r, g, b))
        
    # Fonts
    font_path_serif = r"C:\Windows\Fonts\georgiab.ttf"
    font_path_sans = r"C:\Windows\Fonts\calibri.ttf"
    font_path_sans_bold = r"C:\Windows\Fonts\calibrib.ttf"
    
    # Fallbacks if fonts don't exist
    if not os.path.exists(font_path_serif): font_path_serif = "arial.ttf"
    if not os.path.exists(font_path_sans): font_path_sans = "arial.ttf"
    if not os.path.exists(font_path_sans_bold): font_path_sans_bold = "arial.ttf"
    
    # Load fonts
    try:
        font_eyebrow = ImageFont.truetype(font_path_sans_bold, 15)
        font_title = ImageFont.truetype(font_path_serif, 52)
        font_section_title = ImageFont.truetype(font_path_sans_bold, 17)
        font_feature = ImageFont.truetype(font_path_sans, 19)
        font_price_lbl = ImageFont.truetype(font_path_sans_bold, 13)
        font_price = ImageFont.truetype(font_path_sans_bold, 44)
        font_price_fees = ImageFont.truetype(font_path_sans, 15)
        font_broker_name = ImageFont.truetype(font_path_serif, 24)
        font_broker_creci = ImageFont.truetype(font_path_sans, 14)
        font_broker_phone = ImageFont.truetype(font_path_sans_bold, 32)
        font_broker_web = ImageFont.truetype(font_path_sans, 16)
    except Exception as e:
        print(f"Error loading fonts: {e}. Using default PIL font.")
        font_eyebrow = font_title = font_section_title = font_feature = font_price_lbl = font_price = font_price_fees = font_broker_name = font_broker_creci = font_broker_phone = font_broker_web = ImageFont.load_default()

    # Brand Colors
    color_gold = (201, 168, 76)      # #C9A84C
    color_gold_light = (229, 201, 115) # #E5C973
    color_white = (255, 255, 255)
    color_grey = (170, 170, 170)
    
    # Draw outer gold border (2px)
    border_offset = 25
    draw.rectangle(
        [(border_offset, border_offset), (canvas_w - border_offset, canvas_h - border_offset)],
        outline=color_gold,
        width=2
    )
    
    # --- HEADER ---
    draw.text((60, 55), "OPORTUNIDADE EM SÃO JOSÉ DO RIO PRETO", fill=color_gold, font=font_eyebrow)
    draw.text((60, 80), "ALTOS DE IBORUNA", fill=color_white, font=font_title)
    
    # --- LEFT COLUMN: BUILDING PHOTO ---
    # Load and scale building photo
    bldg_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna\Altos_Iboruna_Fachada.jpg"
    if os.path.exists(bldg_path):
        bldg_img = Image.open(bldg_path)
        # Original is 576x1024. We want to place it at x=60, y=165. Width=450, Height=760.
        # Let's crop it to have width=450, height=760.
        # First resize it so width matches 450 (keep aspect ratio: height becomes 450 * 1024 / 576 = 800)
        bldg_w, bldg_h = 450, 800
        bldg_img_resized = bldg_img.resize((bldg_w, bldg_h), Image.Resampling.LANCZOS)
        # Now crop from (0, 40) to (450, 800) to get a height of 760 (removes top 40px to preserve bottom sign)
        bldg_cropped = bldg_img_resized.crop((0, 40, 450, 800))
        
        # Paste building photo
        base.paste(bldg_cropped, (60, 165))
        # Draw border around building photo
        draw.rectangle([(60, 165), (510, 925)], outline=color_gold, width=2)
    else:
        print("Warning: Building photo not found.")
        draw.rectangle([(60, 165), (510, 925)], fill=(40,40,40), outline=color_gold, width=2)
        draw.text((150, 500), "[Foto do Imóvel]", fill=color_grey, font=font_section_title)

    # --- RIGHT COLUMN: DETAILS ---
    col2_x = 550
    
    # Property details
    draw.text((col2_x, 165), "DETALHES DO IMÓVEL", fill=color_gold, font=font_section_title)
    
    features = [
        "02 Dormitórios (sendo 1 suíte)",
        "Sala ampla p/ 2 ambientes",
        "Sacada com vista livre",
        "Banheiro social",
        "Cozinha com armários",
        "Piso em porcelanato",
        "01 vaga de garagem"
    ]
    
    y_offset = 200
    for feat in features:
        # Draw a custom gold bullet point (small square)
        draw.rectangle([(col2_x, y_offset + 6), (col2_x + 6, y_offset + 12)], fill=color_gold)
        draw.text((col2_x + 18, y_offset), feat, fill=color_white, font=font_feature)
        y_offset += 32
        
    # Condominium details
    y_offset += 15
    draw.text((col2_x, y_offset), "O CONDOMÍNIO OFERECE:", fill=color_gold, font=font_section_title)
    
    condo_features = [
        "Mercado interno & Portaria 24h",
        "Piscina & Academia equipada",
        "Quiosque de churrasqueira",
        "Salão de festas & Brinquedoteca",
        "Excelente área verde integrada"
    ]
    
    y_offset += 35
    for feat in condo_features:
        draw.rectangle([(col2_x, y_offset + 6), (col2_x + 6, y_offset + 12)], fill=color_gold)
        draw.text((col2_x + 18, y_offset), feat, fill=color_white, font=font_feature)
        y_offset += 32
        
    # Investment section
    y_offset += 25
    draw.text((col2_x, y_offset), "VALOR DE VENDA", fill=color_gold, font=font_price_lbl)
    
    y_offset += 20
    draw.text((col2_x, y_offset), "R$ 400.000,00", fill=color_gold_light, font=font_price)
    
    y_offset += 55
    fees_text = "Condomínio: R$ 430,00  |  IPTU: R$ 60,00/mês"
    draw.text((col2_x, y_offset), fees_text, fill=color_grey, font=font_price_fees)

    # --- FOOTER: SEPARATOR LINE ---
    draw.line([(60, 960), (1020, 960)], fill=color_gold, width=1)
    
    # --- FOOTER: BROKER AND CONTACTS ---
    broker_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Fotos"
    broker_path = os.path.join(broker_dir, broker_photo_name)
    
    broker_x, broker_y = 60, 985
    broker_size = 180
    
    if os.path.exists(broker_path):
        # Load broker image
        br_img = Image.open(broker_path)
        br_w, br_h = br_img.size
        
        # We crop the head/shoulders
        if "Segurando paleto" in broker_photo_name:
            crop_box = (949, 328, 2699, 2079)
        elif "Foto de lado" in broker_photo_name:
            crop_box = (900, 300, 2700, 2100)
        elif "Foto segurando a gravata" in broker_photo_name:
            crop_box = (800, 250, 2600, 2050)
        elif "Foto com a mão na perna" in broker_photo_name:
            crop_box = (900, 300, 2700, 2100)
        else:
            # Fallback to centering
            cx = br_w // 2
            crop_box = (cx - int(br_h * 0.16), int(br_h * 0.06), cx + int(br_h * 0.16), int(br_h * 0.38))
            
        br_cropped = br_img.crop(crop_box)
        br_cropped = br_cropped.resize((broker_size, broker_size), Image.Resampling.LANCZOS)
        
        # Create a circle mask
        mask = Image.new('L', (broker_size, broker_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, broker_size, broker_size), fill=255)
        
        # Prepare transparent image for avatar
        avatar = Image.new('RGBA', (broker_size, broker_size), (0, 0, 0, 0))
        avatar.paste(br_cropped, (0, 0), mask=mask)
        
        # Paste avatar on canvas
        base.paste(avatar, (broker_x, broker_y), mask=avatar)
        
        # Draw a gold circle outline around the avatar
        draw.ellipse(
            [(broker_x - 1, broker_y - 1), (broker_x + broker_size + 1, broker_y + broker_size + 1)],
            outline=color_gold,
            width=2
        )
    else:
        # Fallback placeholder
        draw.ellipse([(broker_x, broker_y), (broker_x + broker_size, broker_y + broker_size)], fill=(40,40,40), outline=color_gold, width=2)
        draw.text((broker_x + 40, broker_y + 80), "CORRETOR", fill=color_grey, font=font_section_title)

    # Broker text info (aligned to the right of avatar)
    text_x = broker_x + broker_size + 30
    
    draw.text((text_x, broker_y + 15), "VALTEIR DE OLIVEIRA", fill=color_gold, font=font_broker_name)
    draw.text((text_x, broker_y + 47), "Assessoria Imobiliária  |  CRECI 214072-F", fill=color_grey, font=font_broker_creci)
    
    # Draw phone with green whatsapp indicator
    phone_text = "(17) 99172-6078"
    draw.text((text_x, broker_y + 75), phone_text, fill=color_white, font=font_broker_phone)
    
    # Draw small green dot/rectangle next to the phone or text as whatsapp indicator
    draw.rectangle([(text_x, broker_y + 120), (text_x + 10, broker_y + 130)], fill=(37, 211, 102))
    draw.text((text_x + 18, broker_y + 115), "Atendimento online via WhatsApp", fill=(37, 211, 102), font=font_broker_web)
    
    draw.text((text_x, broker_y + 145), "www.valteir.com.br", fill=color_gold, font=font_broker_web)

    # --- BRAND LOGO ---
    logo_path = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Desing System\Logotipo Valteir Oliveira 2.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        # Original is 2237 x 1026. Aspect ratio ~2.18
        # Card bounds: width=220, height=100. Position: x=770, y=1020
        card_w, card_h = 220, 100
        card_x, card_y = 770, 1025
        
        # Draw white card with gold border
        draw.rectangle(
            [(card_x, card_y), (card_x + card_w, card_y + card_h)],
            fill=(255, 255, 255),
            outline=color_gold,
            width=2
        )
        
        # Resize logo to fit card (with 10px margin)
        logo_w, logo_h = card_w - 20, card_h - 20
        logo_img_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        # Paste logo on card
        base.paste(logo_img_resized, (card_x + 10, card_y + 10))
    else:
        print("Warning: Logo not found.")

    # Save output
    output_dir = r"C:\Users\valte\.gemini\antigravity\scratch\Valteir-Imoveis\Criativos_Redes_Sociais\Altos_Iboruna"
    final_output_path = os.path.join(output_dir, output_name)
    base.save(final_output_path, 'PNG')
    print(f"Ad generated successfully: {final_output_path}")

if __name__ == "__main__":
    # Generate versions for different broker photos
    photos = [
        ("Foto com a mão na perna.jpg", "anuncio_altos_iboruna_mao_perna.png"),
        ("Foto de lado.jpg", "anuncio_altos_iboruna_lado.png"),
        ("Foto segurando a gravata.jpg", "anuncio_altos_iboruna_gravata.png"),
        ("Segurando paleto.jpg", "anuncio_altos_iboruna_paleto.png")
    ]
    
    for photo, name in photos:
        try:
            create_ad(photo, name)
        except Exception as e:
            print(f"Error generating for {photo}: {e}")
