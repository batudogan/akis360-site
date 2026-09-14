# Akış360 — tanıtım sitesi

Tek sayfalık, şifre korumalı ön izleme. `index.html` içerik şifrelenmiş halde yayınlanır; ziyaretçi şifreyi girince sayfa tarayıcıda çözülür.

Kaynak (`src/`) repoya girmez. Güncellemek için:

```bash
AKIS360_PASSWORD='...' python3 build.py
git commit -am "Update site" && git push
```
