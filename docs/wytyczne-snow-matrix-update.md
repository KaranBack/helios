# Wytyczne aktualizacji HELIOS Master Matrix (SNOW Assignment Groups)

Źródło: czat KG + OneDrive (`CL-Gotha-Master-KB-Full.html`) + plik  
`Assignment Groups - Helios & FDT SNOW new.xlsm`.

Cel: macierz KB dla agentów (grupy Assignment w ServiceNow), **nie** macierz AD BLN/BEB/BS.

---

## 1. Usunąć z matrix (grupy nie istnieją w SNOW)

| Assignment Group | Region / Cluster | Uwaga |
|---|---|---|
| CL-Gotha \| Klinische Anwendungen | CL-Gotha | |
| CL-Gotha \| Infrastruktur | CL-Gotha | |
| CL-Gotha \| SAP | CL-Gotha | |
| CL-Gotha \| Accountmanagement | CL-Gotha | |
| CL-Gotha \| Field Service | CL-Gotha | |
| CL-Gifhorn \| Klinische Anwendungen | CL-Gifhorn | |
| CL-Gifhorn \| Infrastruktur | CL-Gifhorn | |
| Medico / KIS Team | CL-Gifhorn | Naming: powinno być `CL-Gifhorn \| Medico / KIS Team` |
| CL-Gifhorn \| Accountmanagement | CL-Gifhorn | |
| CL-Gifhorn \| Local IT / Field Service | CL-Gifhorn | |
| KC-IT \| MVZ | Saxony - North Franconia (East) | |
| PL-IT \| MVZ | Saxony - North Franconia (East) | |
| GRE-IT \| Fieldservice | Central Thuringia (South) | Istnieją: `GRE-IT`, `GRE-IT \| Mgt` |
| MUE-IT \| Infrastruktur | Black Forest - Lake Constance (South) | Istnieją: `MUE-IT`, `MUE-IT \| Fieldservice` |
| TIT-IT \| Infrastruktur | Black Forest - Lake Constance (South) | Istnieją: `TIT-IT`, `TIT-IT \| Fieldservice` |
| OC-IT \| Infrastruktur | Magdeburg (East) | Istnieją: `OC-IT \| Servicedesk`, `OC-IT \| Fieldservice` |
| ZE-IT \| Infrastruktur | Magdeburg (East) | Istnieją: `ZE-IT \| Servicedesk`, `ZE-IT \| Fieldservice` |
| LPZ-IT \| Infrastruktur | Leipzig (East) | Tylko grupa MGT |
| HBH-IT \| Fieldservice | South Lower Saxony - North Hesse (West) | Tylko `HBH-IT` (bez subgroup) |
| KS-IT \| Fieldservice | South Lower Saxony - North Hesse (West) | Tylko `KS-IT` |
| WAR-IT \| Fieldservice | South Lower Saxony - North Hesse (West) | Tylko `WAR-IT` |

---

## 2. Dodać grupy

Źródło: **`Assignment Groups - Helios & FDT SNOW new.xlsm`**

- ELO mapuje stare grupy Helios → nowe grupy używane przez agentów.
- Priorytet: najpierw **usunąć złe**, potem **wgrać dobre** z XLSM (jakkolwiek da się je wrzucić).
- Mapowanie ELO: follow-up w poniedziałek (z czatu).

---

## 3. Znane poprawne warianty (z komentarzy przy usunięciach)

Zostawić / używać zamiast usuwanych:

- `GRE-IT`, `GRE-IT | Mgt`
- `MUE-IT`, `MUE-IT | Fieldservice`
- `TIT-IT`, `TIT-IT | Fieldservice`
- `OC-IT | Servicedesk`, `OC-IT | Fieldservice`
- `ZE-IT | Servicedesk`, `ZE-IT | Fieldservice`
- LPZ: tylko MGT
- `HBH-IT`, `KS-IT`, `WAR-IT` (bez `| Fieldservice`)
- Gifhorn Medico: `CL-Gifhorn | Medico / KIS Team`

---

## 4. Bug wyszukiwania (`GIF-IT` nie znajduje)

Objaw: wpisane w matrix, ale search nie trafia (np. `GIF-IT`).

Prawdopodobne przyczyny (często po eksporcie Copilota):

1. **Inny myślnik** w HTML (`–` en-dash / `—` em-dash / non-breaking hyphen) vs `-` w query
2. **Ukryte znaki** (ZWSP, NBSP) między `GIF` a `IT`
3. Search case-sensitive albo tylko po jednej kolumnie
4. Tekst rozbity tagami (`GIF<span>-</span>IT`) — zwykle `textContent` i tak złączy, ale normalizacja pomaga

**Fix w HTML:** normalizacja przed `includes` — `toLowerCase()`, zamiana wszystkich dashy na `-`, usuwanie ZWSP/NBSP, collapse whitespace.

---

## 5. Pliki źródłowe do dostarczenia

| Plik | Skąd | Status |
|---|---|---|
| `CL-Gotha-Master-KB-Full.html` | OneDrive (czat KG) | **brak w workspace** — wrzuć do `docs/quellen/` |
| `Assignment Groups - Helios & FDT SNOW new.xlsm` | update z czatu | **brak** — wrzuć do `docs/quellen/` |

Bez tych dwóch plików nie da się 1:1 odtworzyć pełnego Master Matrix — poniżej w repo jest szkielet + changelog gotowy do merge po uploadzie.
