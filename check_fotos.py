import os
from PIL import Image
from PIL.ExifTags import TAGS

fotos_dir = r"D:\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo\Fotos"
for f in os.listdir(fotos_dir):
    p = os.path.join(fotos_dir, f)
    try:
        im = Image.open(p)
        print(f, im.size)
    except Exception as e:
        print(f, e)
