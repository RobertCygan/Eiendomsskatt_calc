"""Bygger dist/beregn-eiendomsskatt.html fra src/ og assets/.

Skrift (Inter) og logo legges inn som base64, slik at resultatet blir én
selvstendig HTML-fil uten eksterne avhengigheter.

Kjør:  python build.py
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "beregn-eiendomsskatt.src.html"
OUT = ROOT / "dist" / "beregn-eiendomsskatt.html"


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    for weight in (400, 500, 600, 700):
        html = html.replace(f"{{{{FONT{weight}}}}}", b64(ROOT / "assets" / "fonts" / f"inter-{weight}.woff2"))
    html = html.replace("{{LOGO}}", b64(ROOT / "assets" / "logo" / "steigen-logo-160.png"))
    if "{{" in html:
        raise SystemExit("Fant plassholder som ikke er erstattet i kildefilen.")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Skrev {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
