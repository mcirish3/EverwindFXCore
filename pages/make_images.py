"""Draw the mod page images for EverwindFXCore (1920x1080 gallery images and a 1300x372 header)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
F = "C:/Windows/Fonts/"


def font(bold, size):
    return ImageFont.truetype(F + ("segoeuib.ttf" if bold else "segoeui.ttf"), size)


BG, PANEL, LINE = (16, 22, 30), (26, 35, 47), (52, 66, 84)
TEXT, MUTED, GOLD = (232, 236, 241), (150, 163, 179), (231, 176, 74)
TEAL, RED, BLUE = (72, 186, 168), (214, 96, 86), (96, 150, 222)


def centered(d, x0, w, y, s, f, fill):
    d.text((x0 + (w - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill)


def main_image():
    im = Image.new("RGB", (1920, 1080), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1920, 8), fill=GOLD)
    d.text((110, 60), "EverwindFXCore", font=font(True, 96), fill=TEXT)
    d.text((114, 190), "CPU thread scheduling for Everwind on older CPUs", font=font(False, 44), fill=GOLD)
    d.text((114, 256), "No graphics settings changed  \u00b7  No game files touched  \u00b7  Open source  \u00b7  Beta",
           font=font(False, 28), fill=MUTED)

    d.text((110, 340), "On an AMD FX-8350: the GameThread gets a whole module to itself", font=font(True, 34), fill=TEXT)
    assign = {0: ("GameThread", TEAL), 1: ("kept empty", LINE), 2: ("RenderThread", BLUE), 4: ("RHIThread", BLUE),
              6: ("Audio mixer", GOLD)}
    mw, mh, gap = 400, 210, 28
    for m in range(4):
        mx, my = 110 + m * (mw + gap), 410
        d.rounded_rectangle((mx, my, mx + mw, my + mh), 16, fill=PANEL, outline=LINE, width=3)
        centered(d, mx, mw, my + 12, f"Module {m}  \u00b7  shared FPU + L2", font(False, 22), MUTED)
        for c in range(2):
            cx, cy = mx + 18 + c * 186, my + 58
            label, col = assign.get(m * 2 + c, ("workers", LINE))
            d.rounded_rectangle((cx, cy, cx + 178, cy + 130), 12, fill=BG, outline=col, width=4)
            centered(d, cx, 178, cy + 14, f"Core {m * 2 + c}", font(False, 22), MUTED)
            centered(d, cx, 178, cy + 64, label, font(True, 23), col if col != LINE else MUTED)
    d.text((110, 640), "Every other thread in the game is kept off module 0  \u00b7  0.5 ms timer  \u00b7  no power throttling",
           font=font(False, 26), fill=TEAL)

    d.rounded_rectangle((110, 720, 1810, 990), 16, fill=PANEL, outline=GOLD, width=3)
    d.text((140, 740), "Check these two in-game settings first (they mattered more than the mod)", font=font(True, 32), fill=GOLD)
    d.text((140, 800), "\u2022  Frame Generation ON with a 60 FPS limit = only 30 real frames. Turn it off on a 60 Hz display.",
           font=font(False, 28), fill=TEXT)
    d.text((140, 850), "\u2022  XeSS upscaling on Quality took the test PC from 55.6 to 59.5 average FPS (GPU 91% \u2192 73%).",
           font=font(False, 28), fill=TEXT)
    d.text((140, 912), "Test PC: FX-8350, Radeon RX 6600, 1080p. The mod's own effect on FPS has not been measured in isolation.",
           font=font(False, 24), fill=MUTED)
    d.text((110, 1020), "MIT license  \u00b7  github.com/mcirish3/EverwindFXCore  \u00b7  port of WindroseFXCore",
           font=font(False, 24), fill=MUTED)
    im.save(OUT / "everwind-1-main.png", optimize=True)


def settings_image():
    im = Image.new("RGB", (1920, 1080), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1920, 8), fill=GOLD)
    d.text((110, 60), "Measured on the test PC", font=font(True, 80), fill=TEXT)
    d.text((114, 170), "FX-8350  \u00b7  Radeon RX 6600  \u00b7  1080p  \u00b7  60 FPS limit  \u00b7  AMD Adrenalin logs",
           font=font(False, 32), fill=MUTED)
    rows = [("Frame Generation on", 30.0, "30 real FPS (shown as 60)", RED, "GPU 59%"),
            ("Frame Generation off, native", 55.6, "55.6 average, dips to 47", GOLD, "GPU 91%"),
            ("Frame Generation off, XeSS Quality", 59.5, "59.5 average, lowest 52", TEAL, "GPU 73%")]
    for i, (name, fps, label, col, gpu) in enumerate(rows):
        y = 290 + i * 220
        d.text((110, y), name, font=font(True, 38), fill=TEXT)
        d.rounded_rectangle((110, y + 62, 1810, y + 142), 12, fill=PANEL, outline=LINE, width=2)
        d.rounded_rectangle((110, y + 62, 110 + int(1700 * fps / 60), y + 142), 12, fill=col)
        d.text((134, y + 76), label, font=font(True, 34), fill=BG)
        d.text((1810 - d.textlength(gpu, font=font(False, 28)) - 20, y + 150), gpu, font=font(False, 28), fill=MUTED)
    d.text((110, 960), "These are in-game settings. You don't need the mod for them.", font=font(False, 30), fill=GOLD)
    d.text((110, 1010), "The mod's own effect on frame rate has not been measured in isolation.", font=font(False, 26), fill=MUTED)
    im.save(OUT / "everwind-2-settings.png", optimize=True)


def log_image():
    im = Image.new("RGB", (1920, 1080), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1920, 8), fill=GOLD)
    d.text((110, 60), "Check it's working: EverwindFXCore.log", font=font(True, 64), fill=TEXT)
    d.text((114, 150), "skyverse\\Binaries\\Win64\\EverwindFXCore.log, written at every launch", font=font(False, 30), fill=MUTED)
    lines = [
        "EverwindFXCore 0.2.0-beta loaded into ...\\Everwind-Win64-Shipping.exe",
        "CPU: AMD FX(tm)-8350 Eight-Core Processor",
        "Topology: 8 logical processors, 4 execution groups, 1 L3 domain(s)",
        "Timer resolution: 0.500 ms",
        "Power throttling opt-out: ok (execution speed only)",
        "Process priority: raised",
        "Critical LPs: game 0, render 2, rhi 4, audio 6 | background mask 0xe8",
        "Exclusive game module: GameThread mask 0x3, every other thread 0xfc",
        "  GameThread       tid 36732  prio 1",
        "Exclusive game module: moved 11 thread(s) off the GameThread's group",
        "  RHIThread        tid  5784  prio 1",
        "  RenderThread     tid 39564  prio 1",
        "  AudioMixer       tid  3336  prio 15",
    ]
    d.rounded_rectangle((110, 230, 1810, 960), 16, fill=PANEL, outline=LINE, width=3)
    mono = ImageFont.truetype(F + "consola.ttf", 34)
    for i, s in enumerate(lines):
        d.text((150, 262 + i * 52), s, font=mono, fill=TEAL if "Exclusive" in s else TEXT)
    d.text((110, 1000), "No log file means the DLL did not load.", font=font(False, 28), fill=MUTED)
    im.save(OUT / "everwind-3-log.png", optimize=True)


def header():
    im = Image.new("RGB", (1300, 372), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1300, 6), fill=GOLD)
    d.text((70, 80), "EverwindFXCore", font=font(True, 84), fill=TEXT)
    d.text((74, 196), "CPU thread scheduling for older CPUs", font=font(False, 40), fill=GOLD)
    d.text((74, 262), "Runtime only \u00b7 no graphics changes \u00b7 open source \u00b7 beta", font=font(False, 26), fill=MUTED)
    for i in range(4):
        x, y = 1000 + (i % 2) * 150, 80 + (i // 2) * 120
        d.rounded_rectangle((x, y, x + 130, y + 100), 12, fill=PANEL, outline=LINE, width=3)
        for c in range(2):
            col = TEAL if (i == 0 and c == 0) else BLUE if (c == 0 and i in (1, 2)) else LINE
            d.rounded_rectangle((x + 12 + c * 56, y + 22, x + 62 + c * 56, y + 78), 8, outline=col, width=4)
    im.save(OUT / "everwind-header-1300x372.png", optimize=True)


main_image()
settings_image()
log_image()
header()
print("ok")
