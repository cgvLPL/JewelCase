from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='src="assets/jewelcase-logo-transparent.png" alt="JewelCase - Photo to Jewel Case Artwork"'
new='src="assets/jewelcase-logotype.svg?v=20260903-1512" alt="JewelCase"'
if old not in s:
    raise SystemExit('Header logo source not found')
s=s.replace(old,new,1)
p.write_text(s)
