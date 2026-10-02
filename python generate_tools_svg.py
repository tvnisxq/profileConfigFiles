"""
Builds tools-animated.svg: your Tools & Technologies icons embedded as
data URIs, each floating up and down with a staggered delay.

Run:  python generate_tools_svg.py
Then commit tools-animated.svg to your profileConfigFiles repo.
"""
import base64
import urllib.request

DEVICON = "https://raw.githubusercontent.com/devicons/devicon/master/icons"
SIMPLE = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons"

# (name, url, optional fill color for monochrome icons)
ICONS = [
    ("git", f"{DEVICON}/git/git-original.svg", None),
    ("redis", f"{DEVICON}/redis/redis-original-wordmark.svg", None),
    ("linux", f"{DEVICON}/linux/linux-original.svg", None),
    ("docker", f"{DEVICON}/docker/docker-original-wordmark.svg", None),
    ("hadoop", f"{DEVICON}/hadoop/hadoop-original.svg", None),
    ("spark", f"{DEVICON}/apachespark/apachespark-original.svg", None),
    ("mysql", f"{DEVICON}/mysql/mysql-original.svg", None),
    # simple-icons are single-color black by default, which vanishes on
    # dark mode, so give them a color.
    ("hive", f"{SIMPLE}/apachehive.svg", "#FDEE21"),
    ("hbase", f"{SIMPLE}/apachehbase.svg", "#E4572E"),
]

SLOT = 72          # horizontal space per icon
SIZE = 48          # icon size
FLOAT_PX = 10      # how far icons float
DURATION = 2.4     # seconds per bob
STAGGER = 0.2      # delay between neighbouring icons
OUTFILE = "tools-animated.svg"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def to_data_uri(svg_text: str, color: str | None) -> str:
    if color:
        svg_text = svg_text.replace("<svg ", f'<svg fill="{color}" ', 1)
    b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def main() -> None:
    width = SLOT * len(ICONS)
    height = SIZE + FLOAT_PX * 2 + 8
    y = FLOAT_PX + 4

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        f"@keyframes float {{ 0%,100% {{ transform: translateY(0); }} "
        f"50% {{ transform: translateY(-{FLOAT_PX}px); }} }}",
        f".icon {{ animation: float {DURATION}s ease-in-out infinite; }}",
        "</style>",
    ]

    for i, (name, url, color) in enumerate(ICONS):
        try:
            uri = to_data_uri(fetch(url), color)
        except Exception as e:
            print(f"skipped {name}: {e}")
            continue
        x = i * SLOT + (SLOT - SIZE) // 2
        parts.append(
            f'<g class="icon" style="animation-delay:{i * STAGGER:.1f}s">'
            f'<image xlink:href="{uri}" x="{x}" y="{y}" '
            f'width="{SIZE}" height="{SIZE}"/></g>'
        )

    parts.append("</svg>")

    with open(OUTFILE, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"wrote {OUTFILE}")


if __name__ == "__main__":
    main()
