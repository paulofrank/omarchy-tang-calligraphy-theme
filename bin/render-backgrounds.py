#!/usr/bin/env python3
"""Render the Tang Calligraphy theme backgrounds.

Each variant is a 2560x1440 rice-paper canvas with a faded layer of the
source screenshot as texture, a Tang poem in vertical calligraphy columns
(right to left), a small attribution column, and a cinnabar seal.

Usage: python3 bin/render-backgrounds.py <source-screenshot>
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts" / "MaShanZheng-Regular.ttf"
OUT = ROOT / "backgrounds"

W, H = 2560, 1440
PAPER = "#FAF6EB"
INK = "#2B2620"
CINNABAR = "#B23A30"

POEMS = [
    ("luchai", "鹿柴·王维", ["空山不见人", "但闻人语响", "返景入深林", "复照青苔上"]),
    ("jingyesi", "静夜思·李白", ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]),
    ("chunxiao", "春晓·孟浩然", ["春眠不觉晓", "处处闻啼鸟", "夜来风雨声", "花落知多少"]),
    ("jiangxue", "江雪·柳宗元", ["千山鸟飞绝", "万径人踪灭", "孤舟蓑笠翁", "独钓寒江雪"]),
    ("guanquelou", "登鹳雀楼·王之涣", ["白日依山尽", "黄河入海流", "欲穷千里目", "更上一层楼"]),
    ("jueju", "绝句·杜甫", ["迟日江山丽", "春风花草香", "泥融飞燕子", "沙暖睡鸳鸯"]),
]

CHAR = 96        # poem glyph size
CHAR_STEP = 102  # vertical advance between glyphs
COL_STEP = 128   # horizontal advance between columns
SIGN_CHAR = 46   # attribution glyph size
SIGN_STEP = 52


def base_canvas(screenshot: str, dest: Path) -> None:
    """Paper canvas with the screenshot faintly blended in as texture."""
    subprocess.run([
        "magick", "-size", f"{W}x{H}", f"canvas:{PAPER}",
        "(", screenshot, "-resize", f"{W}x",
             "-gravity", "center", "-crop", f"{W}x{H}+0+420", "+repage",
             "-modulate", "100,25", "-brightness-contrast", "18x-25", ")",
        "-compose", "blend", "-define", "compose:args=14", "-composite",
        str(dest),
    ], check=True)


def annotate_poem(dest: Path, columns: list[str], attribution: str) -> None:
    args = ["magick", str(dest), "-font", str(FONT)]
    x = W - 400  # rightmost column
    top = (H - 5 * CHAR_STEP) // 2
    for col in columns:
        y = top
        for ch in col:
            args += ["-fill", INK, "-pointsize", str(CHAR),
                     "-annotate", f"+{x}+{y}", ch]
            y += CHAR_STEP
        x -= COL_STEP
    # Attribution column, smaller, lower start, left of the poem.
    y = top + 2 * CHAR_STEP
    for ch in attribution.replace(" · ", ""):
        if ch in "· ":
            continue
        args += ["-fill", INK, "-pointsize", str(SIGN_CHAR),
                 "-annotate", f"+{x}+{y}", ch]
        y += SIGN_STEP
    seal_y = y + 50
    # Cinnabar seal with a white 唐.
    args += ["-fill", CINNABAR, "-draw",
             f"roundrectangle {x - 18},{seal_y} {x + SIGN_CHAR + 26},{seal_y + SIGN_CHAR + 44} 14,14",
             "-fill", PAPER, "-pointsize", str(SIGN_CHAR),
             "-annotate", f"+{x - 6}+{seal_y + SIGN_CHAR + 6}", "唐"]
    args.append(str(dest))
    subprocess.run(args, check=True)


def main() -> None:
    screenshot = sys.argv[1] if len(sys.argv) > 1 else "/tmp/opencode/lrb-article.png"
    OUT.mkdir(exist_ok=True)

    plain = OUT / "01-paper.png"
    base_canvas(screenshot, plain)
    print("rendered", plain.name)

    for i, (slug, _title, columns) in enumerate(POEMS, start=2):
        dest = OUT / f"{i:02d}-{slug}.png"
        base_canvas(screenshot, dest)
        annotate_poem(dest, columns, POEMS[i - 2][1])
        print("rendered", dest.name)


if __name__ == "__main__":
    main()
