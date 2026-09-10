"""Generate the animated harbor header and two illustrated developer jokes."""
import math
from PIL import Image, ImageDraw
from build_visuals import BG, PANEL, LINE, LIME, CYAN, WHITE, MUTED, base, font, save


def harbor_banner():
    frames = []
    for i in range(64):
        t = i / 64 * math.tau
        im = Image.new('RGB', (960, 320), BG)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((1, 1, 958, 318), 18, outline=LINE, width=2)
        d.rounded_rectangle((30, 29, 250, 59), 5, fill=LIME)
        d.text((41, 37), 'PHLPPGDFRY / BELGIUM', font=font(17), fill=BG)
        d.text((30, 92), 'Philippe Godfroy', font=font(43), fill=WHITE)
        d.text((32, 154), 'I turn operational chaos into software.', font=font(18), fill=MUTED)
        d.text((32, 184), 'Sometimes it becomes a product.', font=font(18), fill=MUTED)
        d.text((32, 237), 'LOGISTICS / DATA & AI / NATIVE APPS', font=font(15), fill=CYAN)
        d.text((32, 282), 'HALF BUSINESS BRAIN. HALF TERMINAL WINDOW.', font=font(12), fill=MUTED)
        d.line((600, 28, 600, 292), fill=LINE, width=2)
        d.text((626, 29), 'PORT OF SIDE QUESTS', font=font(15), fill=MUTED)
        # Quay, gantry and moving crane trolley.
        d.rectangle((615, 217, 745, 228), fill=LINE)
        d.line((664, 215, 664, 86, 924, 86), fill=LIME, width=5)
        d.line((640, 215, 690, 215), fill=LIME, width=5)
        d.line((664, 86, 703, 57, 750, 86), fill=LIME, width=3)
        x = 796 + round(44 * math.sin(t))
        y = 134 + round(14 * math.cos(t))
        d.rectangle((x - 8, 80, x + 8, 91), fill=WHITE)
        d.line((x, 90, x, y), fill=CYAN, width=2)
        d.rounded_rectangle((x - 39, y, x + 39, y + 31), 3, fill=CYAN)
        d.text((x - 31, y + 8), 'SHIP IT', font=font(14), fill=BG)
        # Vessel gently bobs; tiny containers keep the harbor recognisable.
        dx, dy = round(5 * math.sin(t)), round(2 * math.cos(t))
        d.polygon([(746+dx, 223+dy), (927+dx, 223+dy), (908+dx, 246+dy), (766+dx, 246+dy)], fill=MUTED)
        d.rectangle((887+dx, 193+dy, 914+dx, 222+dy), fill=WHITE)
        d.rectangle((893+dx, 199+dy, 909+dx, 206+dy), fill=BG)
        for j, color in enumerate([LIME, CYAN, '#bc9cff']):
            cx = 759 + j*42 + dx
            d.rectangle((cx, 204+dy, cx+36, 221+dy), fill=color)
        for row in range(3):
            points = [(x, 259+row*13+round(3*math.sin(x/23+t+row))) for x in range(623, 934, 3)]
            d.line(points, fill=[CYAN, '#368fa3', '#255467'][row], width=2)
        frames.append(im)
    save('banner.gif', frames, 100)


def scope_creep():
    frames = []
    for i in range(64):
        im, d = base(600, 255, 'SIDE QUEST / JUST ONE SMALL FEATURE')
        d.text((25, 64), 'Estimated scope: tiny.', font=font(24), fill=WHITE)
        count = min(5, i // 8)
        labels = ['a button', '+ settings', '+ sync', '+ an API', '+ a dashboard', '+ a new repo']
        for j in range(count+1):
            x, y = 25+(j%3)*185, 112+(j//3)*44
            d.rounded_rectangle((x, y, x+173, y+33), 5, fill=PANEL, outline=LIME if j==count else LINE)
            d.text((x+10, y+9), labels[j], font=font(14), fill=LIME if j==count else MUTED)
        d.text((25, 217), 'Narrator: it was not tiny.' if i>=40 else 'This should only take a minute...', font=font(18), fill=CYAN)
        frames.append(im)
    save('one-small-feature.gif', frames, 110)


def production_bug():
    frames = []
    for i in range(60):
        im, d = base(600, 255, 'INCIDENT REPORT / A COMPLETELY FICTIONAL BUG')
        live = i>=25
        d.text((25, 66), 'Works on my machine.', font=font(25), fill=WHITE)
        for x, label, color in [(25, 'LOCAL: OK', LIME), (310, 'PROD: '+('SURPRISE' if live else 'DEPLOYING'), '#f58b8b' if live else CYAN)]:
            d.rounded_rectangle((x, 117, x+265, 173), 8, fill=PANEL, outline=color, width=2)
            d.text((x+16, 136), label, font=font(18), fill=color)
        d.text((25, 210), 'The bug has requested a sea view.' if live else 'Shipping the machine was not an option.', font=font(16), fill=MUTED)
        if live:
            x, y = 535, 82+round(3*math.sin(i/3))
            d.ellipse((x-9,y-12,x+9,y+12), fill='#f58b8b')
            for offset in [-7,0,7]:
                d.line((x-16,y+offset-4,x+16,y+offset+4), fill='#f58b8b', width=2)
        frames.append(im)
    save('production-surprise.gif', frames, 110)


if __name__ == '__main__':
    harbor_banner()
    scope_creep()
    production_bug()
