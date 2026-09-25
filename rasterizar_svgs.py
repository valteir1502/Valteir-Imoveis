import os
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image

base_dir = r"C:\Users\valte\OneDrive\Área de Trabalho\Projeto - Valteir Imoveis\Logos_Novas"

def render_svg_to_png(svg_name, out_name):
    svg_path = os.path.join(base_dir, svg_name)
    drawing = svg2rlg(svg_path)
    if drawing:
        temp_png = os.path.join(base_dir, f"temp_{out_name}.png")
        renderPM.drawToFile(drawing, temp_png, fmt="PNG")
        
        # Load and resize cleanly
        img = Image.open(temp_png).convert("RGBA")
        
        # Full HD
        img.save(os.path.join(base_dir, f"{out_name}_HD_transparente.png"), "PNG")
        
        # 100x100
        img_100 = img.resize((100, 100), Image.Resampling.LANCZOS)
        img_100.save(os.path.join(base_dir, f"{out_name}_100x100_transparente.png"), "PNG")
        
        # 100x100 Dark Mode
        bg_dark = Image.new("RGBA", (100, 100), (12, 14, 18, 255))
        bg_dark.paste(img_100, (0, 0), img_100)
        bg_dark.convert("RGB").save(os.path.join(base_dir, f"{out_name}_100x100_dark.jpg"), quality=95)
        
        if os.path.exists(temp_png):
            os.remove(temp_png)
        print(f"Exportado com sucesso: {out_name}")

render_svg_to_png("logo_valteir_vetorial_icone.svg", "logo_valteir_vetorial_icone")
render_svg_to_png("logo_valteir_vetorial_horizontal.svg", "logo_valteir_vetorial_horizontal")
render_svg_to_png("logo_valteir_vetorial_vertical.svg", "logo_valteir_vetorial_vertical")
