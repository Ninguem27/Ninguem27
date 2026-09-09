from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
]
FONT = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)


def font(size):
    if FONT:
        return ImageFont.truetype(FONT, size)
    return ImageFont.load_default()


def centered(draw, y, text, fnt, fill, width):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text(((width - (box[2] - box[0])) / 2, y), text, font=fnt, fill=fill)


def banner():
    W, H, N = 900, 240, 36
    frames = []
    for i in range(N):
        im = Image.new("RGB", (W, H), (9, 13, 22))
        d = ImageDraw.Draw(im)
        for y in range(H):
            t = y / H
            d.line((0, y, W, y), fill=(9 + int(9*t), 13 + int(12*t), 22 + int(20*t)))
        d.rounded_rectangle((6, 6, W-7, H-7), radius=18, outline=(184, 138, 68), width=2)
        cx, cy = W//2, H//2
        for rad, speed, col in [(72, 1, (139, 92, 246)), (96, -0.7, (120, 80, 220))]:
            a0 = 2*math.pi*(i/N)*speed
            for k in range(12):
                a = a0 + 2*math.pi*k/12
                x, y = cx + rad*math.cos(a), cy + rad*math.sin(a)
                d.ellipse((x-1.5, y-1.5, x+1.5, y+1.5), fill=col)
        for j, x in enumerate([120, 180, 720, 790]):
            phase = (i*7 + j*11) % (H-40)
            y = H - 20 - phase
            d.ellipse((x-2, y-2, x+2, y+2), fill=(245, 158, 11))
        ang = math.radians(-10 + 20*math.sin(2*math.pi*i/N))
        ox, oy, L = 120, 118, 65
        x2, y2 = ox + L*math.cos(ang), oy + L*math.sin(ang)
        d.line((ox, oy, x2, y2), fill=(214, 179, 106), width=6)
        hx, hy = ox - 12*math.sin(ang), oy + 12*math.cos(ang)
        d.line((hx-18*math.cos(ang), hy-18*math.sin(ang), hx+18*math.cos(ang), hy+18*math.sin(ang)), fill=(214, 179, 106), width=10)
        d.line((770, 80, 830, 140), fill=(214, 179, 106), width=5)
        d.line((830, 80, 770, 140), fill=(214, 179, 106), width=5)
        centered(d, 64, "KAIO • NINGUEM27", font(34), (248,250,252), W)
        centered(d, 112, "DESENVOLVIMENTO • GAME DESIGN • RPG • WORLDBUILDING", font(17), (196,181,253), W)
        centered(d, 151, "FORJA DOS MUNDOS • SISTEMAS • MAPAS • BESTIÁRIOS • CARTAS", font(15), (214,179,106), W)
        r = 5 + 3*math.sin(2*math.pi*i/N)
        d.ellipse((cx-r, 195-r, cx+r, 195+r), fill=(249,115,22))
        frames.append(im)
    frames[0].save(os.path.join(OUT, "forja-rpg-banner.gif"), save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)


def dice():
    W, H, N = 520, 260, 44
    frames = []
    for i in range(N):
        im = Image.new("RGB", (W, H), (9, 13, 22))
        d = ImageDraw.Draw(im)
        for y in range(H):
            t = y/H
            d.line((0, y, W, y), fill=(9+int(12*t), 13+int(18*t), 22+int(28*t)))
        d.rounded_rectangle((6, 6, W-7, H-7), radius=18, outline=(139,92,246), width=2)
        centered(d, 18, "D20 EM MOVIMENTO • FORJA DOS MUNDOS", font(19), (214,179,106), W)
        d.arc((55,45,W-55,235), start=195, end=345, fill=(139,92,246), width=2)
        t = i/(N-1)
        if t < 0.7:
            u = t/0.7
            x = 75 + (W-150)*u
            y = 185 - 120*math.sin(math.pi*u)
        else:
            u = (t-0.7)/0.3
            x = W-75 - 110*u
            y = 185 - 25*abs(math.sin(math.pi*2*u))*(1-u)
        ang = 2*math.pi*3*t
        R = 38
        pts=[]
        for k in range(6):
            a = ang + 2*math.pi*k/6 - math.pi/2
            pts.append((x+R*math.cos(a), y+R*math.sin(a)))
        d.polygon(pts, fill=(16,24,39), outline=(248,211,106))
        for p in pts:
            d.line((x, y, p[0], p[1]), fill=(214,179,106), width=2)
        num = "20" if i % 11 < 5 else "17"
        f = font(20)
        b = d.textbbox((0,0), num, font=f)
        d.text((x-(b[2]-b[0])/2, y-(b[3]-b[1])/2-2), num, font=f, fill=(255,255,255))
        for j in range(4):
            sx, sy = x-40-j*12, y+30+(j%2)*6
            d.ellipse((sx-2,sy-2,sx+2,sy+2), fill=(245,158,11))
        centered(d, 228, "rolando pela mesa...", font(15), (196,181,253), W)
        frames.append(im)
    frames[0].save(os.path.join(OUT, "d20-rolling.gif"), save_all=True, append_images=frames[1:], duration=85, loop=0, optimize=True)


if __name__ == "__main__":
    banner()
    dice()
