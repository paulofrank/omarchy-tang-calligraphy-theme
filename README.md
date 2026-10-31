# Tang Calligraphy — an Omarchy theme

Ink on rice paper. A light Omarchy theme of warm paper tones, ink-black
text, and a cinnabar seal-red accent, with desktop backgrounds that carry
Tang dynasty poems in vertical calligraphy.

![preview](preview.png)

## Install

```bash
omarchy theme install https://github.com/paulofrank/omarchy-tang-calligraphy-theme
omarchy theme set tang-calligraphy
```

Cycle the poem backgrounds with `omarchy theme bg next`.

## Backgrounds

Seven variants, all built from the same rice-paper base:

- `01-paper.png` — plain paper texture
- `02-luchai.png` — 鹿柴 · 王维 (Wang Wei)
- `03-jingyesi.png` — 静夜思 · 李白 (Li Bai)
- `04-chunxiao.png` — 春晓 · 孟浩然 (Meng Haoran)
- `05-jiangxue.png` — 江雪 · 柳宗元 (Liu Zongyuan)
- `06-guanquelou.png` — 登鹳雀楼 · 王之涣 (Wang Zhihuan)
- `07-jueju.png` — 绝句 · 杜甫 (Du Fu)

The poems are rendered with the
[Ma Shan Zheng](https://fonts.google.com/specimen/Ma+Shan+Zheng)
calligraphy font (SIL Open Font License, included in `fonts/`), in
traditional vertical columns read right to left, with a cinnabar 唐 seal.

Regenerate the backgrounds (e.g. with your own base image) with:

```bash
python3 bin/render-backgrounds.py /path/to/your-screenshot.png
```

Requires ImageMagick.

## Palette

| Role | Colour | |
|---|---|---|
| background | `#FAF6EB` | rice paper |
| foreground | `#2B2620` | ink |
| accent | `#B23A30` | cinnabar / seal red |
| selection | `#E8E0CC` | aged paper |
| muted | `#A89C84` | faded ink |

## Compatibility

The theme is intentionally minimal — `colors.toml` plus backgrounds — so
Omarchy regenerates every application's config (terminal, Hyprland,
Neovim, VS Code…) from the palette through its own templates. That is the
mechanism designed to keep themes working across Omarchy versions. Tested
on Omarchy 3.x (October 2026); please open an issue if a future update
breaks anything.

## Credits

- Poems: Tang dynasty, public domain.
- Font: Ma Shan Zheng by Ma Shan Zheng, SIL OFL 1.1 (see `fonts/OFL.txt`).
- Theme: MIT (see `LICENSE`).
