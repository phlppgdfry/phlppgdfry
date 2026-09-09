"""Rebuild the original geometric profile artwork. Requires Pillow."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG, PANEL, LINE = '#0b1119', '#131f2c', '#26384a'
LIME, CYAN, WHITE, MUTED = '#c8f135', '#55ddec', '#edf4fa', '#a2b2c4'

def font(size):
    for path in ['/System/Library/Fonts/Menlo.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)

def base(w, h, title):
    im = Image.new('RGB', (w,h), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,w-2,h-2), 15, outline=LINE, width=2)
    d.text((24,18), title, font=font(13), fill=MUTED)
    for x,c in [(w-65,LIME),(w-47,CYAN),(w-29,'#f58b8b')]:
        d.ellipse((x,22,x+7,29),fill=c)
    return im,d

def save(name,frames,ms=90):
    frames[0].save(OUT/name, save_all=True, append_images=frames[1:], duration=ms, loop=0, optimize=True, disposal=2)

def harbor():
    frames=[]
    for i in range(64):
        im,d=base(960,250,'01 / THE SHIPPING DEPARTMENT')
        t=i/64*2*math.pi
        d.line((20,196,940,196),fill=LINE,width=3)
        for x,y,c,label in [(70,150,CYAN,'DATA'),(207,150,LIME,'APPS'),(70,105,LIME,'IDEAS'),(645,150,CYAN,'PORTOPS'),(782,150,LIME,'TOOLS')]:
            d.rounded_rectangle((x,y,x+124,y+39),4,outline=c,width=2)
            for xx in range(x+8,x+120,12): d.line((xx,y+8,xx,y+30),fill=LINE)
            d.rectangle((x+16,y+10,x+110,y+29),fill=BG)
            d.text((x+22,y+11),label,font=font(14),fill=c)
        d.line((403,191,403,65,688,65),fill=MUTED,width=5)
        d.line((370,191,435,191),fill=MUTED,width=5)
        d.line((403,65,448,42,510,65),fill=LINE,width=3)
        x=490+int(90*math.sin(t)); y=98+int(12*math.cos(t))
        d.line((x+51,65,x+51,y),fill=CYAN,width=2)
        d.rounded_rectangle((x,y,x+104,y+35),4,fill=LIME)
        d.text((x+16,y+9),'SHIP IT',font=font(14),fill=BG)
        for xx in range(30,940,30):
            yy=218+int(3*math.sin(t+xx/38))
            d.line((xx,yy,xx+17,yy),fill=CYAN,width=2)
        frames.append(im)
    save('harbor.gif',frames)

def terminal():
    frames=[]
    lines=['$ whoami','Philippe / builder / Belgium','$ make something-useful','[ok] find the messy workflow','[ok] build a working slice','[ok] test the awkward cases','> side quest detected_']
    for i in range(56):
        im,d=base(460,270,'02 / TERMINAL WINDOW')
        for j,line in enumerate(lines):
            count=max(0,min(len(line),(i-j*5)*3))
            d.text((23,58+j*27),line[:count],font=font(15),fill=LIME if j in [0,2,6] else WHITE)
        frames.append(im)
    save('terminal.gif',frames,110)

def pipeline():
    frames=[]
    for i in range(48):
        im,d=base(460,270,'03 / DATA, WITH A DESTINATION')
        for j,(label,c) in enumerate([('BRONZE','#dfa46d'),('SILVER','#c2d1dd'),('GOLD',LIME)]):
            x=23+j*145
            d.rounded_rectangle((x,100,x+121,164),9,fill=PANEL,outline=c,width=2)
            d.text((x+24,123),label,font=font(15),fill=c)
            if j<2: d.line((x+123,132,x+141,132),fill=MUTED,width=2)
        x=26+int(i/48*407)
        d.ellipse((x,184,x+8,192),fill=CYAN)
        d.text((27,220),'raw -> validated -> useful',font=font(16),fill=WHITE)
        frames.append(im)
    save('pipeline.gif',frames)

def radar():
    frames=[]
    for i in range(48):
        im,d=base(460,250,'04 / SIDE-QUEST RADAR')
        cx,cy=118,145
        for r in [28,53,78]: d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=LINE,width=1)
        d.line((cx-80,cy,cx+80,cy),fill=LINE); d.line((cx,cy-80,cx,cy+80),fill=LINE)
        a=i/48*2*math.pi
        d.line((cx,cy,cx+77*math.cos(a),cy+77*math.sin(a)),fill=LIME,width=3)
        for x,y in [(150,113),(86,165),(139,195)]: d.ellipse((x-3,y-3,x+3,y+3),fill=CYAN)
        d.text((229,99),'NEW IDEA',font=font(22),fill=LIME)
        d.text((229,134),'Scope: tiny.',font=font(15),fill=WHITE)
        d.text((229,160),'Probably.',font=font(15),fill=MUTED)
        frames.append(im)
    save('radar.gif',frames)

def coast():
    frames=[]
    for i in range(48):
        im,d=base(960,160,'05 / NORTH SEA RESET')
        for row in range(3):
            points=[(x,90+row*20+int(6*math.sin(x/44+i/48*2*math.pi+row))) for x in range(24,937,3)]
            d.line(points,fill=[CYAN,'#368fa3','#255467'][row],width=2)
        x=760+int(20*math.sin(i/48*2*math.pi))
        d.polygon([(x,46),(x+24,59),(x+5,74),(x-17,60)],outline=LIME)
        d.line((x+5,74,x-19,108),fill=MUTED)
        frames.append(im)
    save('coast.gif',frames)

def banner(title,subtitle,name):
    from html import escape
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="290" viewBox="0 0 960 290" role="img" aria-label="{escape(title)}">
    <rect width="960" height="290" rx="18" fill="{BG}"/>
    <path d="M0 235H960M690 0V290M738 0V290M786 0V290M834 0V290M882 0V290M930 0V290" stroke="{LINE}" opacity=".55"/>
    <rect x="34" y="32" width="182" height="27" rx="5" fill="{LIME}"/>
    <text x="47" y="50" font-family="monospace" font-size="13" fill="{BG}">PHLPPGDFRY / BELGIUM</text>
    <text x="34" y="123" font-family="Arial,sans-serif" font-weight="700" font-size="49" fill="{WHITE}">{escape(title)}</text>
    <text x="36" y="163" font-family="Arial,sans-serif" font-size="18" fill="{MUTED}">{escape(subtitle)}</text>
    <text x="36" y="212" font-family="monospace" font-size="13" fill="{CYAN}">LOGISTICS / DATA &amp; AI / NATIVE APPS / BUSINESS ANALYSIS</text>
    <text x="36" y="267" font-family="monospace" font-size="12" fill="{MUTED}">HALF BUSINESS BRAIN. HALF TERMINAL WINDOW.</text>
    <path d="M797 222V58H922M770 223H824M797 58L825 32L864 58M881 58V113" stroke="{LIME}" stroke-width="4" fill="none"/>
    <rect x="845" y="113" width="73" height="39" rx="4" fill="{CYAN}"/>
    <path d="M859 122V143M873 122V143M887 122V143M901 122V143" stroke="{BG}" opacity=".35"/>
    </svg>'''
    (OUT/name).write_text(svg)

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for args in [('Philippe Godfroy','I turn operational chaos into software. Sometimes it becomes a product.','banner.svg'),('Indie workshop','Small apps. Useful details. The entire journey from idea to release.','indie.svg'),('Business analysis','From a messy workflow to a clear requirement and a testable outcome.','ba.svg'),('Professional profile','Software engineering, operational thinking and commercial experience.','professional.svg'),('Beyond the terminal','Philippe, also known as Kippie. Somewhere near the North Sea.','personal.svg')]: banner(*args)
    harbor(); terminal(); pipeline(); radar(); coast()
