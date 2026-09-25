import os
from PIL import Image, ImageFilter
import numpy as np

def create_watermark_logos():
    """
    Gera logos da Valteir Imóveis com fundo transparente e fundo neutro
    para uso como marca d'água em fotos de imóveis.
    """
    src = r"C:\Users\valte\.gemini\antigravity-ide\brain\c1dd3128-9b0d-45cd-8486-eaee7277ab5a\logo_gold_transparent_1789930939402.jpg"
    out_dir = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis\Logos_Novas"
    out_root = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis"
    os.makedirs(out_dir, exist_ok=True)

    im = Image.open(src).convert("RGB")
    arr = np.array(im, dtype=np.float32)

    # 1. FUNDO NEUTRO ESCURO (cinza escuro #2C2C2C) - Para fundos claros ou uso direto
    # O fundo original já é ~(44, 44, 44) - próximo de um cinza carvão elegante
    # Vamos recortar apenas a área com a logo (remover excesso de margem)
    gray = np.mean(arr, axis=2)
    bg_val = 44.0
    
    # Detectar bounding box da logo (pixels significativamente diferentes do fundo)
    diff = np.abs(gray - bg_val)
    mask = diff > 12  # Tolerância para detectar elementos da logo
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)
    
    # Adicionar margem proporcional elegante
    margin_x = int((x1 - x0) * 0.08)
    margin_y = int((y1 - y0) * 0.12)
    x0 = max(0, x0 - margin_x)
    y0 = max(0, y0 - margin_y)
    x1 = min(im.width, x1 + margin_x)
    y1 = min(im.height, y1 + margin_y)
    
    logo_crop = im.crop((x0, y0, x1 + 1, y1 + 1))
    crop_arr = np.array(logo_crop, dtype=np.float32)
    
    print(f"Logo crop: {logo_crop.size} (from bounding box [{x0},{y0}] to [{x1},{y1}])")
    
    # 2. VERSÃO COM FUNDO TRANSPARENTE (PNG RGBA)
    # Extrair alfa: pixels do fundo são ~(44,44,44), logo é dourada/clara
    crop_gray = np.mean(crop_arr, axis=2)
    
    # Calcular diferença de cor em relação ao fundo neutro
    bg_color = np.array([44.0, 44.0, 44.0])
    color_diff = np.sqrt(np.sum((crop_arr - bg_color) ** 2, axis=2))
    
    # Normalizar: diferença máxima possível é sqrt(3 * (255-44)^2) ≈ 365
    max_diff = np.sqrt(3 * (255.0 - 44.0) ** 2)
    alpha = color_diff / max_diff
    alpha = np.clip(alpha, 0.0, 1.0)
    
    # Suavizar transições e remover ruído
    alpha[alpha < 0.06] = 0.0
    
    # Aplicar curva suave para melhores bordas
    alpha = np.power(alpha, 0.85)
    alpha = np.clip(alpha, 0.0, 1.0)
    
    h, w = crop_gray.shape
    
    # Versão transparente mantendo as cores originais da logo
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 0] = np.clip(crop_arr[..., 0], 0, 255).astype(np.uint8)
    rgba[..., 1] = np.clip(crop_arr[..., 1], 0, 255).astype(np.uint8)
    rgba[..., 2] = np.clip(crop_arr[..., 2], 0, 255).astype(np.uint8)
    rgba[..., 3] = (alpha * 255).astype(np.uint8)
    
    img_transparent = Image.fromarray(rgba, "RGBA")
    
    # 3. SALVAR VERSÕES
    sizes = {
        # Para marca d'água em fotos (tamanho grande, alta resolução)
        "logo_valteir_marca_dagua_transparente.png": None,  # Tamanho original recortado
        # Para site (400x100)
        "logo_valteir_dourada_400x100_transparente.png": (400, 100),
        # Para site (200x200)
        "logo_valteir_dourada_200x200_transparente.png": (200, 200),
        # Para redes sociais (800x200 HD)
        "logo_valteir_dourada_800x200_hd_transparente.png": (800, 200),
        # Ícone quadrado (500x500)
        "logo_valteir_dourada_500x500_transparente.png": (500, 500),
    }
    
    generated = []
    
    for fname, target_size in sizes.items():
        if target_size is None:
            # Salvar no tamanho original recortado
            img_transparent.save(os.path.join(out_dir, fname), "PNG", optimize=True)
            img_transparent.save(os.path.join(out_root, fname), "PNG", optimize=True)
            generated.append((fname, f"{img_transparent.size[0]}x{img_transparent.size[1]}px (Original HD)"))
        else:
            tw, th = target_size
            canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            
            # Calcular redimensionamento proporcional
            aspect = img_transparent.width / img_transparent.height
            
            if tw / th > aspect:
                # Canvas mais largo que a logo
                fit_h = int(th * 0.85)
                fit_w = int(fit_h * aspect)
            else:
                # Canvas mais alto que a logo
                fit_w = int(tw * 0.92)
                fit_h = int(fit_w / aspect)
            
            resized = img_transparent.resize((fit_w, fit_h), Image.Resampling.LANCZOS)
            ox = (tw - fit_w) // 2
            oy = (th - fit_h) // 2
            canvas.paste(resized, (ox, oy), resized)
            
            canvas.save(os.path.join(out_dir, fname), "PNG", optimize=True)
            canvas.save(os.path.join(out_root, fname), "PNG", optimize=True)
            generated.append((fname, f"{tw}x{th}px"))
    
    # 4. VERSÃO COM FUNDO NEUTRO ESCURO (para uso direto sem transparência)
    # Fundo cinza carvão elegante #2B2B2B
    for bg_name, bg_color_rgb in [("escuro", (43, 43, 43)), ("preto", (0, 0, 0))]:
        canvas_bg = Image.new("RGBA", img_transparent.size, (*bg_color_rgb, 255))
        canvas_bg = Image.alpha_composite(canvas_bg, img_transparent)
        canvas_bg_rgb = canvas_bg.convert("RGB")
        
        fname_bg = f"logo_valteir_dourada_fundo_{bg_name}.png"
        canvas_bg_rgb.save(os.path.join(out_dir, fname_bg), "PNG", optimize=True)
        canvas_bg_rgb.save(os.path.join(out_root, fname_bg), "PNG", optimize=True)
        generated.append((fname_bg, f"Fundo {bg_name} sólido"))
    
    print("\n[OK] Logos geradas com sucesso!\n")
    for fname, desc in generated:
        print(f"  > {fname}  ({desc})")

if __name__ == "__main__":
    create_watermark_logos()
