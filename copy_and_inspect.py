import os
import shutil
import glob

scratch = r"C:\Users\valte\.gemini\antigravity-ide\brain\7ec79ec2-23bd-4df3-904e-d61b1d8902ab\scratch"
os.makedirs(scratch, exist_ok=True)

src_dirs = [
    r"D:\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo\Compradores",
    r"D:\Negocios Imobiliários\Condomínio Buona Vita\Reginaldo\Vendedores"
]

copied = []
for sdir in src_dirs:
    for root, dirs, files in os.walk(sdir):
        for f in files:
            src_file = os.path.join(root, f)
            # Prefix with folder name to avoid collision
            prefix = os.path.basename(sdir) + "_"
            dst_file = os.path.join(scratch, prefix + f)
            shutil.copy2(src_file, dst_file)
            copied.append((prefix + f, os.path.getsize(dst_file)))

print(f"Total copied: {len(copied)}")
for name, size in copied:
    print(f"  {name}: {size} bytes")
