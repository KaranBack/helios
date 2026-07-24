# HELIOS Matrix

Interaktive **Berechtigungsmatrix** für den Helios-Cluster Berlin-Brandenburg (BLN · BEB · BS).

## Inhalt

- AD-Gruppen nach Standort, Rolle und System (Windows-Basis, SAP, aQrate, Laufwerke, Verteiler, PDMS, Muse, Zenzy)
- Checkliste für Benutzeranträge
- Kurzprozesse: Projektlaufwerk anlegen, Abwesenheitsnotiz (Exchange)

## Start

```bash
npm install
npm run dev
```

Build:

```bash
npm run build
```

## Daten

Einträge liegen in `src/data/matrix.ts` und basieren auf den RO-IT-Dokumenten (Benutzeranträge, Laufwerks-Anlage, Abwesenheitsnotiz).
