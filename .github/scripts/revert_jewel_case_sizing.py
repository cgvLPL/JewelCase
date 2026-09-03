from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Restore the previous full-frame template sizing.
s = s.replace("c.drawImage(templateImage,S*.016,S*.028,S*.965,S*.951);", "c.drawImage(templateImage,0,0,S,S);")

# Restore the previous disc geometry.
s = s.replace(
    "const cx=S*.5010,cy=S*.5000,r=S*.4310,hubR=S*.0900,hubProtectR=S*.1120;",
    "const cx=S*.5030,cy=S*.4980,r=S*.3890,hubR=S*.0900,hubProtectR=S*.1120;"
)
s = s.replace(
    "const cx=S*.5010,cy=S*.5000,discR=S*.4450;",
    "const cx=S*.5030,cy=S*.4980,discR=S*.4050;"
)

# Remove the sizing-only aspect-ratio addition so preview sizing matches the prior layout.
s = s.replace(
    ".stage-shell{width:min(78vh,820px);max-width:100%;position:relative;aspect-ratio:1/1}",
    ".stage-shell{width:min(78vh,820px);max-width:100%;position:relative}"
)

p.write_text(s)
