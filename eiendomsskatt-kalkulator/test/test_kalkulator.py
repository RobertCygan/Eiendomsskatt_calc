"""Kontroll av beregningene i kalkulatoren.

Åpner dist/beregn-eiendomsskatt.html i en hodeløs nettleser, kjører tre
testeiendommer gjennom beregningen og sammenligner med håndregnede svar.

Krever:  pip install playwright   og   playwright install chromium
Kjør:    python test/test_kalkulator.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
URL = (ROOT / "dist" / "beregn-eiendomsskatt.html").as_uri()

TOM = {"step": 1, "floors": {"hoved": "", "under": "", "sokkel": "", "loft": "", "kjeller": ""},
       "standard": "normal", "bygg": [], "tomt": "", "noMaal": False, "gard": False, "sone": "", "ytre": "normal"}


def tilfelle(**kw):
    s = {**TOM, **kw}
    s["floors"] = {**TOM["floors"], **kw.get("floors", {})}
    return s


# Sone-indekser følger rekkefølgen i CONFIG.soner (0 = Leinesfjord, 8 = Nordskott, 10 = Øvrige)
TILFELLER = [
    ("A: Enebolig Nordskott, før 1960, garasje 30 m² + bod 12 m², tomt 1 500 m²",
     tilfelle(type="enebolig", floors={"hoved": "120", "under": "60", "sokkel": "40", "loft": "20"},
              alder="f60", bygg=[{"id": 1, "type": "garasje", "areal": "30"}, {"id": 2, "type": "garasje", "areal": "12"}],
              tomt="1500", sone="8"),
     # (1 200 000 + 120 000 + 320 000 + 60 000 + 60 000 + 0 + 75 000) × 0,8 × 1,0 × 0,6
     {"takst": 880800, "skatt": 2466.24}),
    ("B: Fritidsbolig 80 m², 2010+, uten målebrev, øvrige områder, dårlig beliggenhet",
     tilfelle(type="fritid", floors={"hoved": "80"}, alder="2010", noMaal=True, sone="10", ytre="darlig"),
     # (800 000 + 2 000 × 50) × 0,7 × 0,8 × 1,0
     {"takst": 504000, "skatt": 1411.2}),
    ("C: Gårdbrukers bolig 150 m², 1960–1985 oppgradert, tomt 3 000 m², Leinesfjord",
     tilfelle(type="enebolig", floors={"hoved": "150"}, alder="1960", standard="hoy", tomt="3000", gard=True, sone="0"),
     # (1 500 000 + 1 000 × 50) × 1,0 × 1,0 × 0,9 × 0,9
     {"takst": 1255500, "skatt": 3515.4}),
]


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL)
        feil = 0
        for navn, state, fasit in TILFELLER:
            r = await page.evaluate("s => { const r = __eskatt.beregn(s); return {takst: r.takst, skatt: r.skatt}; }", state)
            ok = abs(r["takst"] - fasit["takst"]) < 0.01 and abs(r["skatt"] - fasit["skatt"]) < 0.01
            feil += not ok
            print(("OK   " if ok else "FEIL ") + navn, r)
        await browser.close()
        raise SystemExit(1 if feil else 0)


if __name__ == "__main__":
    asyncio.run(main())
