#!/usr/bin/env python3
"""
src/index.html + src/img/* → şifreli index.html

Kullanım:
    AKIS360_PASSWORD='sifre' python3 build.py

Adımlar:
  1. src/img altındaki görselleri data URI olarak sayfaya gömer (böylece onlar da şifrelenir).
  2. Sayfayı OpenSSL ile AES-256-CBC (PBKDF2, 100k iterasyon) şifreler.
  3. gate.html şablonundaki {{CIPHERTEXT}} yerine koyup index.html olarak yazar.

Sadece index.html (şifreli) ve gate.html/build.py repoya girer; src/ .gitignore'da.
"""
import base64, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

password = os.environ.get("AKIS360_PASSWORD")
if not password:
    sys.exit("AKIS360_PASSWORD ortam değişkenini ayarlayın.")

html = (SRC / "index.html").read_text(encoding="utf-8")

def inline(m):
    rel = m.group(1)
    p = SRC / rel
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    data = base64.b64encode(p.read_bytes()).decode()
    return f'src="data:{mime};base64,{data}"'

html = re.sub(r'src="(img/[^"]+)"', inline, html)

enc = subprocess.run(
    ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "100000", "-md", "sha256",
     "-salt", "-base64", "-A", "-pass", "env:AKIS360_PASSWORD"],
    input=html.encode("utf-8"), capture_output=True, check=True,
).stdout.decode().strip()

gate = (ROOT / "gate.html").read_text(encoding="utf-8")
(ROOT / "index.html").write_text(gate.replace("{{CIPHERTEXT}}", enc), encoding="utf-8")
print(f"index.html yazıldı ({len(enc)//1024} KB şifreli veri)")
