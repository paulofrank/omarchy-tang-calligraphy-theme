#!/usr/bin/env python3
"""Render the Tang Calligraphy theme backgrounds.

Each variant is a 2560x1440 rice-paper canvas with a Tang poem in
traditional characters, set in vertical calligraphy columns (right to
left) using AR PL UKai TW, with an attribution column and a cinnabar
seal.

Usage: python3 bin/render-backgrounds.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts" / "AR-PL-UKai-TW.ttf"
OUT = ROOT / "backgrounds"

W, H = 2560, 1440
PAPER = "#FAF6EB"
INK = "#2B2620"
CINNABAR = "#B23A30"

# Traditional text, matching the poems used by the Tang screensaver.
POEMS = [
    ("luchai", "鹿柴 王維", ["空山不見人", "但聞人語響", "返景入深林", "復照青苔上"]),
    ("jingyesi", "靜夜思 李白", ["床前明月光", "疑是地上霜", "舉頭望明月", "低頭思故鄉"]),
    ("chunxiao", "春曉 孟浩然", ["春眠不覺曉", "處處聞啼鳥", "夜來風雨聲", "花落知多少"]),
    ("jiangxue", "江雪 柳宗元", ["千山鳥飛絕", "萬徑人蹤滅", "孤舟蓑笠翁", "獨釣寒江雪"]),
    ("guanquelou", "登鸛雀樓 王之渙", ["白日依山盡", "黃河入海流", "欲窮千里目", "更上一層樓"]),
    ("jueju", "絕句 杜甫", ["兩個黃鸝鳴翠柳", "一行白鷺上青天", "窗含西嶺千秋雪", "門泊東吳萬里船"]),
]

CHAR = 96        # poem glyph size
CHAR_STEP = 102  # vertical advance between glyphs
COL_STEP = 128   # horizontal advance between columns
SIGN_CHAR = 46   # attribution glyph size
SIGN_STEP = 52


def base_canvas(dest: Path) -> None:
    """Plain rice-paper canvas: the paper tone plus two faint noise
    layers (fine grain and vertical fibre). No imagery, no text."""
    subprocess.run([
        "magick", "-size", f"{W}x{H}", f"canvas:{PAPER}",
        "(", "-size", f"{W}x{H}", "xc:", "+noise", "Random",
             "-colorspace", "Gray", "-blur", "0x0.4",
             "-alpha", "set", "-channel", "A", "-evaluate", "set", "5%", "+channel", ")",
        "-compose", "over", "-composite",
        "(", "-size", f"{W}x{H}", "xc:", "+noise", "Gaussian",
             "-colorspace", "Gray", "-motion-blur", "0x16+90", "-blur", "0x1",
             "-alpha", "set", "-channel", "A", "-evaluate", "set", "3%", "+channel", ")",
        "-compose", "over", "-composite",
        str(dest),
    ], check=True)


def annotate_poem(dest: Path, columns: list[str], attribution: str) -> None:
    args = ["magick", str(dest), "-font", str(FONT)]
    x = W - 400  # rightmost column
    max_len = max(len(col) for col in columns)
    top = (H - max_len * CHAR_STEP) // 2
    for col in columns:
        y = top
        for ch in col:
            args += ["-fill", INK, "-pointsize", str(CHAR),
                     "-annotate", f"+{x}+{y}", ch]
            y += CHAR_STEP
        x -= COL_STEP
    # Attribution column, smaller, starting lower, left of the poem.
    # A space in the attribution becomes a gap between title and author.
    y = top + 2 * CHAR_STEP
    for ch in attribution:
        if ch == " ":
            y += SIGN_STEP
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
    OUT.mkdir(exist_ok=True)

    plain = OUT / "01-paper.png"
    base_canvas(plain)
    print("rendered", plain.name)

    for i, (slug, attribution, columns) in enumerate(POEMS, start=2):
        dest = OUT / f"{i:02d}-{slug}.png"
        base_canvas(dest)
        annotate_poem(dest, columns, attribution)
        print("rendered", dest.name)


if __name__ == "__main__":
    main()
