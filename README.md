# Helios Master Matrix

Jedna baza wiedzy Catch & Dispatch / Swivel Chair w pliku **`matrix.html`**.

## Plik

- [`matrix.html`](matrix.html) — pełna baza + UI (styl Global Routing Matrix / Wave 1)
- [`data/kb.json`](data/kb.json) — ta sama baza w JSON (łatwy diff / backup)

## Źródła

- CL-Berlin Master Knowledge Base v1.0
- Helios Global Routing Matrix v2.8 (Full KB Edition)
- Helios Service Desk Routing Wave 1

## Edycja

Otwórz `matrix.html`, znajdź `const KB = { ... }` i edytuj:

| Cel | Pole |
|-----|------|
| Nowy cluster | `KB.clusters` |
| Karta lokalizacji | `KB.locationCards` |
| Aplikacje | `KB.apps.*` |
| Berlin A-Z override | `KB.berlinAz` |
| Wave 1 keyword | `KB.wave1` |
| Global Helios group | `KB.globalHelios` |

Po zapisie odśwież przeglądarkę — tabele budują się automatycznie.
