from pathlib import Path
p=Path('index.html')
s=p.read_text()
# Match the supplied square reference framing while sizing the physical jewel case
# to a standard CD jewel-case proportion (about 142 mm wide x 125 mm high).
s=s.replace('.stage-shell{width:min(78vh,820px);max-width:100%;position:relative}', '.stage-shell{width:min(78vh,820px);max-width:100%;position:relative;aspect-ratio:1/1}')
s=s.replace('.stage-shell:before{content:"";display:block;padding-top:100%}', '.stage-shell:before{content:"";display:block;padding-top:100%}')
# The supplied reference is square, but the clear case itself occupies roughly
# x=1.6%..98.1%, y=2.8%..97.9%: ~96.5% x 95.1% of the square frame.
# Preserve square Apple/Spotify-ready output and calibrate the case footprint.
s=s.replace("c.drawImage(templateImage,0,0,S,S);", "c.drawImage(templateImage,S*.016,S*.028,S*.965,S*.951);", 1)
# Specular reprojection and hub restoration must use the same calibrated case geometry.
s=s.replace("c.drawImage(templateImage,0,0,S,S);", "c.drawImage(templateImage,S*.016,S*.028,S*.965,S*.951);", 1)
s=s.replace("c.drawImage(templateImage,0,0,S,S);", "c.drawImage(templateImage,S*.016,S*.028,S*.965,S*.951);", 1)
# Align disc geometry to the supplied reference's case/disc footprint.
s=s.replace("const cx=S*.5030,cy=S*.4980,r=S*.3890,hubR=S*.0900,hubProtectR=S*.1120;", "const cx=S*.5010,cy=S*.5000,r=S*.4310,hubR=S*.0900,hubProtectR=S*.1120;")
s=s.replace("const cx=S*.5030,cy=S*.4980,discR=S*.4050;", "const cx=S*.5010,cy=S*.5000,discR=S*.4450;")
p.write_text(s)
