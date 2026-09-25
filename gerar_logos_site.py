import os
from PIL import Image
import numpy as np

def generate_site_logos():
    # 1. Caminho da imagem de origem
    src_path = r"C:\Users\valte\.gemini\antigravity-ide\brain\c1dd3128-9b0d-45cd-8486-eaee7277ab5a\.user_uploaded\media_1789829104260.png"
    out_dir_root = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis"
    out_dir_logos = os.path.join(out_dir_root, "Logos_Novas")
    os.makedirs(out_dir_logos, exist_ok=True)

    # 2. Carrega imagem e extrai máscara alfa matematicamente perfeita
    im = Image.open(src_path).convert("RGB")
    arr = np.array(im, dtype=np.float32)

    # Fundo original escuro do print é RGB(32, 32, 32)
    bg = 32.0
    gray = np.mean(arr, axis=2)
    alpha = (gray - bg) / (255.0 - bg)
    alpha = np.clip(alpha, 0.0, 1.0)
    # Remove ruídos residuais
    alpha[alpha < 0.04] = 0.0

    # 3. Função para colorir e recortar
    def create_colored_master(rgb_color):
        h, w = gray.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        rgba[..., 0] = rgb_color[0]
        rgba[..., 1] = rgb_color[1]
        rgba[..., 2] = rgb_color[2]
        rgba[..., 3] = (alpha * 255).astype(np.uint8)
        img = Image.fromarray(rgba, "RGBA")
        
        # Crop completo
        bbox = img.getbbox()
        full_crop = img.crop(bbox)
        
        # Crop do símbolo (lado esquerdo)
        sym_alpha = alpha[:, :160]
        coords_s = np.argwhere(sym_alpha > 0.1)
        sy0, sx0 = coords_s.min(axis=0)
        sy1, sx1 = coords_s.max(axis=0)
        sym_crop = img.crop((sx0, sy0, sx1 + 1, sy1 + 1))
        
        return full_crop, sym_crop

    # Paletas de cores
    palettes = {
        "branca": (255, 255, 255),      # Branco Puro (Igual à imagem enviada, ideal para fundos escuros)
        "dourada": (212, 175, 55),     # Dourado Ouro Nobre #D4AF37
        "preta": (20, 21, 26),         # Ônix / Preto Profundo (para fundos claros)
    }

    generated_files = []

    for name, color in palettes.items():
        full_crop, sym_crop = create_colored_master(color)
        
        # --- A. FORMATO HORIZONTAL: 400x100px (Requisito Oficial do Site) ---
        canvas_400 = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
        # Altura ideal 82px para respiro elegante (9px cima/baixo)
        target_h = 82
        aspect = full_crop.width / full_crop.height
        target_w = int(target_h * aspect)
        resized_full = full_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Centralizado no canvas 400x100
        offset_x = (400 - target_w) // 2
        offset_y = (100 - target_h) // 2
        canvas_400.paste(resized_full, (offset_x, offset_y), resized_full)
        
        # Versão 400x100
        fname_400 = f"logo_valteir_imoveis_400x100_{name}.png"
        p1 = os.path.join(out_dir_logos, fname_400)
        p2 = os.path.join(out_dir_root, fname_400)
        canvas_400.save(p1, "PNG", optimize=True)
        canvas_400.save(p2, "PNG", optimize=True)
        generated_files.append((fname_400, "400x100px (Horizontal)"))

        # --- B. FORMATO QUADRADO: 200x200px - Símbolo / Monograma (Requisito Oficial do Site) ---
        canvas_200_sym = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        target_sym_h = 160
        aspect_sym = sym_crop.width / sym_crop.height
        target_sym_w = int(target_sym_h * aspect_sym)
        resized_sym = sym_crop.resize((target_sym_w, target_sym_h), Image.Resampling.LANCZOS)
        
        offset_sx = (200 - target_sym_w) // 2
        offset_sy = (200 - target_sym_h) // 2
        canvas_200_sym.paste(resized_sym, (offset_sx, offset_sy), resized_sym)
        
        fname_200_sym = f"logo_valteir_simbolo_200x200_{name}.png"
        p3 = os.path.join(out_dir_logos, fname_200_sym)
        p4 = os.path.join(out_dir_root, fname_200_sym)
        canvas_200_sym.save(p3, "PNG", optimize=True)
        canvas_200_sym.save(p4, "PNG", optimize=True)
        generated_files.append((fname_200_sym, "200x200px (Símbolo/Ícone)"))

        # --- C. FORMATO QUADRADO: 200x200px - Logo Completa (Opção Adicional) ---
        canvas_200_full = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        target_full_w = 186
        target_full_h = int(target_full_w / aspect)
        resized_200_full = full_crop.resize((target_full_w, target_full_h), Image.Resampling.LANCZOS)
        
        offset_fx = (200 - target_full_w) // 2
        offset_fy = (200 - target_full_h) // 2
        canvas_200_full.paste(resized_200_full, (offset_fx, offset_fy), resized_200_full)
        
        fname_200_full = f"logo_valteir_completa_200x200_{name}.png"
        p5 = os.path.join(out_dir_logos, fname_200_full)
        p6 = os.path.join(out_dir_root, fname_200_full)
        canvas_200_full.save(p5, "PNG", optimize=True)
        canvas_200_full.save(p6, "PNG", optimize=True)
        generated_files.append((fname_200_full, "200x200px (Logo Completa)"))

    # --- D. ALTA RESOLUÇÃO RETINA (800x200px e 400x400px) para máxima nitidez ---
    for name, color in palettes.items():
        full_crop, sym_crop = create_colored_master(color)
        
        canvas_800 = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
        aspect = full_crop.width / full_crop.height
        target_h = 164
        target_w = int(target_h * aspect)
        resized = full_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        canvas_800.paste(resized, ((800 - target_w) // 2, (200 - target_h) // 2), resized)
        
        fname_800 = f"logo_valteir_imoveis_800x200_hd_{name}.png"
        canvas_800.save(os.path.join(out_dir_logos, fname_800), "PNG", optimize=True)
        canvas_800.save(os.path.join(out_dir_root, fname_800), "PNG", optimize=True)

    print("Sucesso! Arquivos gerados:")
    for f, desc in generated_files:
        print(f" - {f}: {desc}")

if __name__ == "__main__":
    generate_site_logos()
