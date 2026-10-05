# Beregn eiendomsskatt – Steigen kommune (prototype)

Veiledende kalkulator for eiendomsskatt på bolig og fritidsbolig, bygget etter
*Rammer og retningslinjer for taksering i Steigen kommune 2019* (sakkyndig
takstnemnd, revidert 17.02.2020) og kommunestyrets vedtak om skattesats.

Utviklet av Robert Cygan, økonomikonsulent, Steigen kommune. Status: prototype,
ikke godkjent for publisering.

## Innhold

| Mappe / fil | Hva |
|---|---|
| `dist/beregn-eiendomsskatt.html` | Ferdig kalkulator. Én fil, virker uten internett. Åpnes i nettleser. |
| `src/beregn-eiendomsskatt.src.html` | Kildefil (HTML, CSS, JavaScript) med plassholdere for skrift og logo. Redigeres her. |
| `build.py` | Bygger `dist/` fra `src/` og `assets/`. |
| `assets/fonts/` | Inter (samme skrift som steigen.kommune.no), SIL Open Font License 1.1. |
| `assets/logo/` | Kommunens logo (original og nedskalert). |
| `test/test_kalkulator.py` | Kontrollerer beregningen mot tre håndregnede eksempler. |
| `test/skjermbilder/` | Skjermbilder av alle steg og mobilvisning. |
| `kilder/` | Rammer og retningslinjer 2019 (vedtatt 26.02.19) og revisjon 17.02.2020. |

## Beregning

```
Takst          = (bygningsareal × etasjefaktor × sats per m² + tomteareal × tomtepris)
                 × sonefaktor × ytre faktor × indre faktor  [× 0,9 gårdsbruk i drift]
Skattegrunnlag = takst × 0,7 − bunnfradrag
Eiendomsskatt  = skattegrunnlag × skattesats (4 ‰ for bolig og fritid)
```

Alle satser og faktorer ligger i objektet `CONFIG` øverst i skriptet i
`src/beregn-eiendomsskatt.src.html`, med henvisning til punkt i retningslinjene.
Årlige endringer (skatteår, skattesats, bunnfradrag) gjøres bare der.

## Oppdatere

1. Endre `CONFIG` i `src/beregn-eiendomsskatt.src.html`.
2. Kjør `python build.py`.
3. Kjør `python test/test_kalkulator.py` (krever Playwright). Oppdater fasit i
   testen hvis satsene er endret.

## Publisering på steigen.kommune.no

Header, brødsmulesti og footer i filen er bare forhåndsvisning – de finnes
allerede på nettsiden. Det som skal bygges inn er `<section id="eskatt-kalkulator">`
med tilhørende `<style>` og `<script>`. Kalkulatoren bruker ingen eksterne
skript, informasjonskapsler eller sporing, og lagrer ingen opplysninger.

## Antakelser som må avklares

1. Indre faktor brukes på hele eiendommen, også tomten («tomt og bygninger
   dersom bebygd»). Flagg: `CONFIG.indreFaktorGjelderTomt`.
2. Gårdbrukers bolig: 0,9 multipliseres med ytre faktor (0,8 × 0,9 = 0,72).
3. Lav standard: midtverdien i intervallet brukes (f.eks. 0,4–0,5 → 0,45).
4. Bunnfradrag er satt til 0 kr og må kontrolleres mot årets budsjettvedtak.
5. Takst rundes ikke av.

## Ikke med i denne versjonen

Næringseiendom, ubebygd tomt (maks takstgrunnlag 50 000 kr), seksjonerte
eiendommer, flere boliger på samme gnr./bnr., festetomter og restaurerings- eller
rivningsobjekter.
