export type Standort = "BLN" | "BEB" | "BS";
export type Rolle = "aerzte" | "pflege" | "verwaltung" | "extern" | "alle";
export type Kategorie =
  | "basis"
  | "app"
  | "sap"
  | "aqrate"
  | "laufwerk"
  | "verteiler"
  | "pdms"
  | "muse"
  | "zenzy"
  | "fslogix"
  | "profil";

export interface MatrixEntry {
  id: string;
  standorte: Standort[];
  rollen: Rolle[];
  kategorie: Kategorie;
  system: string;
  gruppe: string;
  hinweis?: string;
  intern?: boolean;
  extern?: boolean;
}

export interface StandortInfo {
  code: Standort;
  name: string;
  loginScript: string;
}

export const STANDORTE: StandortInfo[] = [
  {
    code: "BLN",
    name: "Berlin Buch",
    loginScript: "BLN\\Scripts\\Login\\blnusers.bat",
  },
  {
    code: "BEB",
    name: "Berlin-Zehlendorf Emil von Behring",
    loginScript: "BEB\\Scripts\\Login\\bebusers.bat",
  },
  {
    code: "BS",
    name: "Bad Saarow",
    loginScript: "BS\\login.cmd",
  },
];

export const ROLLEN: { id: Rolle; label: string }[] = [
  { id: "aerzte", label: "Ärzte" },
  { id: "pflege", label: "Pflege" },
  { id: "verwaltung", label: "Verwaltung" },
  { id: "extern", label: "Externe" },
  { id: "alle", label: "Alle" },
];

export const KATEGORIEN: { id: Kategorie; label: string }[] = [
  { id: "basis", label: "AD Basis" },
  { id: "app", label: "Apps" },
  { id: "sap", label: "SAP" },
  { id: "aqrate", label: "aQrate" },
  { id: "laufwerk", label: "Laufwerke" },
  { id: "verteiler", label: "E-Mail Verteiler" },
  { id: "pdms", label: "PDMS" },
  { id: "muse", label: "Muse / CGM" },
  { id: "zenzy", label: "Zenzy" },
  { id: "fslogix", label: "FSLogix" },
  { id: "profil", label: "Profil / Home" },
];

/** Berechtigungsmatrix Cluster Berlin-Brandenburg (Quelle: Benutzeranträge) */
export const MATRIX: MatrixEntry[] = [
  // —— BLN interne Basis ——
  {
    id: "bln-quota",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "basis",
    system: "Quota",
    gruppe: "BLN-Quota-User-0000.3GB",
    hinweis: "Default-Quota",
    intern: true,
  },
  {
    id: "bln-ci-sign",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "app",
    system: "Outlook Signatur",
    gruppe: "BLN-app-CI-Sign-Outlook",
    intern: true,
  },
  {
    id: "bln-outlook-sig-ext",
    standorte: ["BLN"],
    rollen: ["extern"],
    kategorie: "app",
    system: "Outlook Signatur",
    gruppe: "BLN-App-Outlook-Signatur",
    extern: true,
  },
  {
    id: "bln-iris",
    standorte: ["BLN"],
    rollen: ["pflege", "aerzte", "alle"],
    kategorie: "app",
    system: "IRIS View",
    gruppe: "BLN-App-IrisView",
    hinweis: "Pflege-Set: immer vergeben",
  },
  {
    id: "bln-sap",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "sap",
    system: "SAP",
    gruppe: "BLN-sap-user",
  },
  {
    id: "bln-aqrate",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "aqrate",
    system: "aQrate",
    gruppe: "BLN-Aqrate-Grp-xxxxx",
    hinweis: "entsprechend der Abteilung (z. B. BLN-Aqrate-Grp-User-BLN-HTMN-Ergotherapie)",
  },
  {
    id: "bln-home-ah",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BLN-LW-USR-HomeShares-AH",
    hinweis: "Share anhand Vor-/Nachname – Support → UserHomes",
  },
  {
    id: "bln-home-ir",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BLN-LW-USR-HomeShares-IR",
  },
  {
    id: "bln-home-sz",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BLN-LW-USR-HomeShares-SZ",
  },
  {
    id: "bln-fslogix1",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "fslogix",
    system: "FSLogix",
    gruppe: "BLN-CTX-FSLogix1Pfad",
    hinweis: "Nur EINE FSLogix-Gruppe vergeben",
  },
  {
    id: "bln-fslogix2",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "fslogix",
    system: "FSLogix",
    gruppe: "BLN-CTX-FSLogix2Pfad",
    hinweis: "Nur EINE FSLogix-Gruppe vergeben",
  },
  {
    id: "bln-vert-hk",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "verteiler",
    system: "Exchange Verteiler",
    gruppe: "BLN-Alle-Mitarbeiter-HK",
    hinweis: "nach E-Mail-Erstellung; GmbH-Zugehörigkeit vom Antrag",
  },
  {
    id: "bln-vert-vbhd",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "verteiler",
    system: "Exchange Verteiler",
    gruppe: "BLN-Alle-Mitarbeiter-VBHD",
  },
  {
    id: "bln-vert-vbhd-schw",
    standorte: ["BLN"],
    rollen: ["pflege"],
    kategorie: "verteiler",
    system: "Exchange Verteiler",
    gruppe: "BLN-Alle-Mitarbeiter-VBHD-Schwestern",
  },
  {
    id: "bln-vert-hgz",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "verteiler",
    system: "Exchange Verteiler",
    gruppe: "BLN-Helios-Gesundheitszentren-Berlin",
  },
  {
    id: "bln-vert-ca",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BLN-CA (Station & Fachbereich)",
    hinweis: "Chefärzte immer aufnehmen",
  },
  {
    id: "bln-vert-oa",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BLN-OA (Station & Fachbereich)",
    hinweis: "Oberärzte immer aufnehmen",
  },
  {
    id: "bln-vert-aerzte",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BLN-Ärzte (Station & Fachbereich)",
  },
  {
    id: "bln-vert-pflege",
    standorte: ["BLN"],
    rollen: ["pflege"],
    kategorie: "verteiler",
    system: "Pflege Verteiler",
    gruppe: "BLN-Pflege",
    hinweis: "Pflegekräfte immer aufnehmen",
  },

  // —— BEB ——
  {
    id: "beb-outlook-std",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "app",
    system: "Outlook Profil",
    gruppe: "BEB-app-Outlook-StdPrf",
  },
  {
    id: "beb-outlook-ohne",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "app",
    system: "Outlook Profil",
    gruppe: "BEB-app-Outlook-ohne-PRF",
  },
  {
    id: "beb-rightfax",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "app",
    system: "Rightfax",
    gruppe: "BEB-app-Rightfax-Sync-Enabled",
  },
  {
    id: "beb-prof-path",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "profil",
    system: "Profilpfad",
    gruppe: "BEB-LW-Prof-Path",
  },
  {
    id: "beb-quota",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "basis",
    system: "Quota",
    gruppe: "BEB-quota-user-0000.3GB",
  },
  {
    id: "beb-iris",
    standorte: ["BEB"],
    rollen: ["pflege", "aerzte", "alle"],
    kategorie: "app",
    system: "IRIS View",
    gruppe: "BEB-App-IrisView",
    hinweis: "Pflege-Set: immer vergeben",
  },
  {
    id: "beb-sap",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "sap",
    system: "SAP",
    gruppe: "BEB-SAP-User",
  },
  {
    id: "beb-aqrate",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "aqrate",
    system: "aQrate",
    gruppe: "BEB-Aqrate-Grp-User",
  },
  {
    id: "beb-home-ah",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BEB-LW-USR-HomeShares-AH",
  },
  {
    id: "beb-home-ir",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BEB-LW-USR-HomeShares-IR",
  },
  {
    id: "beb-home-sz",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "laufwerk",
    system: "Home Share",
    gruppe: "BEB-LW-USR-HomeShares-SZ",
  },
  {
    id: "beb-vert-hk",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "verteiler",
    system: "Exchange Verteiler",
    gruppe: "BEB-alle-Mitarbeiter-HK",
    hinweis: "nach E-Mail-Erstellung; GmbH vom Antrag",
  },
  {
    id: "beb-vert-ca",
    standorte: ["BEB"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BEB-CA (Station & Fachbereich)",
    hinweis: "Chefärzte immer aufnehmen",
  },
  {
    id: "beb-vert-oa",
    standorte: ["BEB"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BEB-OA (Station & Fachbereich)",
  },
  {
    id: "beb-vert-aerzte",
    standorte: ["BEB"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BEB-Ärzte",
  },
  {
    id: "beb-vert-pflege",
    standorte: ["BEB"],
    rollen: ["pflege"],
    kategorie: "verteiler",
    system: "Pflege Verteiler",
    gruppe: "BEB-Pflegedienst",
  },

  // —— BS ——
  {
    id: "bs-fb",
    standorte: ["BS"],
    rollen: ["alle", "extern"],
    kategorie: "basis",
    system: "Fachbereich",
    gruppe: "BS-FB-XXX",
    hinweis: "anhand Fachbereich & Berufsgruppe (z. B. BS-FB-Neuro)",
  },
  {
    id: "bs-vg",
    standorte: ["BS"],
    rollen: ["alle"],
    kategorie: "verteiler",
    system: "Verteilergruppe",
    gruppe: "BS-VG-XXX",
    hinweis: "z. B. BS-VG-Neuro",
  },
  {
    id: "bs-aqrate",
    standorte: ["BS"],
    rollen: ["alle"],
    kategorie: "aqrate",
    system: "aQrate",
    gruppe: "BS-aQrate-Grp-XXX",
    hinweis: "z. B. BS-aQrate-Grp-BS-FB-Neuro",
  },
  {
    id: "bs-aqrate-ext",
    standorte: ["BS"],
    rollen: ["extern"],
    kategorie: "aqrate",
    system: "aQrate Externe",
    gruppe: "BS-aQrate-Grp-BS-FB-Sonstige",
    extern: true,
  },
  {
    id: "bs-home",
    standorte: ["BS"],
    rollen: ["alle", "extern"],
    kategorie: "profil",
    system: "Home Share",
    gruppe: "\\\\BSCLFILE01\\Home$\\%username%",
    hinweis: "Extension Attribute 5 pflegen",
  },
  {
    id: "bs-iris",
    standorte: ["BS"],
    rollen: ["pflege"],
    kategorie: "app",
    system: "IRIS View",
    gruppe: "BS-App-IrisView",
  },
  {
    id: "bs-vert-ca",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BS-CA (Station & Fachbereich)",
    hinweis: "z. B. BS-CA-Onkologie",
  },
  {
    id: "bs-vert-oa",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BS-OA (Station & Fachbereich)",
  },
  {
    id: "bs-vert-aerzte",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "verteiler",
    system: "Ärzte Verteiler",
    gruppe: "BS-Ärzte (Station & Fachbereich)",
    hinweis: "z. B. BS-Ärzte-Onkologie",
  },
  {
    id: "bs-vert-pflege",
    standorte: ["BS"],
    rollen: ["pflege"],
    kategorie: "verteiler",
    system: "Pflege Verteiler",
    gruppe: "BS-Pflegedienst",
  },

  // —— PDMS BLN ——
  {
    id: "pdms-bln-pflege-its",
    standorte: ["BLN"],
    rollen: ["pflege"],
    kategorie: "pdms",
    system: "PDMS Pflege",
    gruppe: "BLN-PDMS-Pflege-ITSIMC-alle",
    hinweis:
      "C1-11 ITS, C2-31 Kardio-IMC, C2-32 Anästhesie-IMC/Stroke, Pflege Nephrologie/Dialyse — nur EINE PDMS-Gruppe!",
  },
  {
    id: "pdms-bln-pflege-awr",
    standorte: ["BLN"],
    rollen: ["pflege"],
    kategorie: "pdms",
    system: "PDMS Pflege",
    gruppe: "BLN-PDMS-Pflege-AnästhAWR",
    hinweis: "Pflege ZOP Anästhesie und Aufwachraum — nur EINE PDMS-Gruppe!",
  },
  {
    id: "pdms-bln-arzt-intensiv",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BLN-PDMS-Ärzte-Intensiv",
    hinweis: "C1-11 Intensivstation",
  },
  {
    id: "pdms-bln-arzt-innere",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BLN-PDMS-Ärzte-Innere",
    hinweis: "C2-31 Kardio-IMC",
  },
  {
    id: "pdms-bln-arzt-intensiv-wa",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BLN-PDMS-Ärzte-Intensiv-WA",
    hinweis: "C2-31 Kardiologie und Nephrologie (nur Nephrologen)",
  },
  {
    id: "pdms-bln-arzt-neuro",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BLN-PDMS-Ärzte-Neuro",
    hinweis: "C2-32 Stroke Unit",
  },
  {
    id: "pdms-bln-arzt-wa",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BLN-PDMS-Ärzte-WA",
    hinweis: "Alle Ärzte der Anästhesie (ZOP oder IMC)",
  },
  {
    id: "pdms-bln-funk",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "pdms",
    system: "PDMS Funktionsbereiche",
    gruppe: "BLN-PDMS-Funktionsbereiche",
    hinweis: "Physio, Logo, Ergo",
  },
  {
    id: "pdms-bln-medco",
    standorte: ["BLN"],
    rollen: ["verwaltung"],
    kategorie: "pdms",
    system: "PDMS Med-Controlling",
    gruppe: "BLN-PDMS-MedCo",
  },
  {
    id: "pdms-beb-pflege",
    standorte: ["BEB"],
    rollen: ["pflege"],
    kategorie: "pdms",
    system: "PDMS Pflege",
    gruppe: "BEB-PDMS-Pflege-*",
    hinweis: "siehe WikIT: BEB PDMS Nutzergruppen",
  },
  {
    id: "pdms-bs-pflege",
    standorte: ["BS"],
    rollen: ["pflege"],
    kategorie: "pdms",
    system: "PDMS Pflege",
    gruppe: "BS-PDMS-Pflege-*",
    hinweis:
      "ITS/IMC über BS-FB-AINS-Pflege-ITS / BS-FB-AINS-Pflege-Anaesthesie verknüpft",
  },
  {
    id: "pdms-bs-arzt-ana",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BS-PDMS-Ärzte-PDMS-Anästhesie",
  },
  {
    id: "pdms-bs-arzt",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "pdms",
    system: "PDMS Ärzte",
    gruppe: "BS-PDMS-ÄrzteWeitere",
    hinweis: "Nur für Ärzte außerhalb ITS/IMC",
  },

  // —— Muse / CGM ——
  {
    id: "muse-web-bln",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "muse",
    system: "WebMuse",
    gruppe: "BLN-Webmuse-Allgemein + BLN-Webmuse-XXX",
    hinweis: "Kostenstelle erforderlich; Replikation ~24h; Citrix ZD_MUSE_sqAdmin",
  },
  {
    id: "muse-cgm-bln",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "muse",
    system: "CGM Muse",
    gruppe: "BLN-MUSE-User-temp",
    hinweis: "NIEMALS manuell anlegen — immer über AD-Gruppe",
  },
  {
    id: "muse-cgm-vbln",
    standorte: ["BLN"],
    rollen: ["alle"],
    kategorie: "muse",
    system: "CGM Muse MVZ",
    gruppe: "VBLN-MUSE-User-temp",
  },
  {
    id: "muse-cgm-beb",
    standorte: ["BEB"],
    rollen: ["alle"],
    kategorie: "muse",
    system: "CGM Muse",
    gruppe: "BEB-MUSE-User-temp",
  },
  {
    id: "muse-cgm-bs",
    standorte: ["BS"],
    rollen: ["alle"],
    kategorie: "muse",
    system: "CGM Muse",
    gruppe: "BS-MUSE-User-temp",
  },

  // —— Zenzy ——
  {
    id: "zenzy-bln",
    standorte: ["BLN"],
    rollen: ["aerzte"],
    kategorie: "zenzy",
    system: "Zenzy Arztmodul",
    gruppe: "BLN-app-Zenzy2-Arztmodul",
    hinweis:
      "Ticket inkl. Windows-ID an elke.dittmann@ / Anja.Obst@ / BLN.Zenzy@",
  },
  {
    id: "zenzy-beb",
    standorte: ["BEB"],
    rollen: ["aerzte"],
    kategorie: "zenzy",
    system: "Zenzy Arztmodul",
    gruppe: "BEB-app-Zenzy2-Arztmodul",
  },
  {
    id: "zenzy-bs",
    standorte: ["BS"],
    rollen: ["aerzte"],
    kategorie: "zenzy",
    system: "Zenzy Arztmodul",
    gruppe: "BS-cit-HELIOS-Berlin-Zenzy2-Arztmodul",
  },
];

export interface ChecklisteItem {
  id: string;
  titel: string;
  details: string;
}

export const CHECKLISTE: ChecklisteItem[] = [
  {
    id: "ticket",
    titel: "Ticketbetreff",
    details:
      "Datum – Standort – Nachname, Vorname (Funktion) Helios-ID  |  LÖ / NÄ / UMZUG / ROTATION markieren",
  },
  {
    id: "idm",
    titel: "IDM / LOGA",
    details:
      "IDM-Eintrag prüfen (Helios=LOGA). Anträge 14 Tage im Voraus ok; 30 Tage vorher täglich prüfen.",
  },
  {
    id: "namen",
    titel: "AD Namenskonvention",
    details:
      "Vorname.Nachname @helios-gesundheit.de; bei Dopplung 1. Buchstabe+Nachname; sAMAccountName max. 12 Zeichen.",
  },
  {
    id: "passwort",
    titel: "Initialpasswort",
    details:
      "Helios + aktuelles Jahr (z. B. Helios2026). Haken „Kennwort ändern“ erst NACH Test setzen.",
  },
  {
    id: "mailbox",
    titel: "Mailbox",
    details:
      "Reiter Rufnummern → Anmerkung: „Mailbox-Aktivierung“. Exchange-Verteiler erst danach.",
  },
  {
    id: "rotation",
    titel: "Rotation",
    details:
      "Vorherige Rechte NICHT entziehen — neue Rechte nur ergänzen.",
  },
  {
    id: "pdms-one",
    titel: "PDMS",
    details: "Jedem Mitarbeiter nur EINE PDMS-Gruppe zuordnen.",
  },
  {
    id: "fslogix-one",
    titel: "FSLogix",
    details: "Nur eine FSLogix-Pfad-Gruppe vergeben.",
  },
  {
    id: "umra",
    titel: "UMRA / Telefonbuch",
    details:
      "https://telefon.helios-kliniken.de/pages/user_edit.aspx — Anrede, Abteilung, Position, Firma, Adresse, Telefon, Berufsgruppe. Replikation ~15 min.",
  },
];

export interface ProzessDoc {
  id: string;
  titel: string;
  kurz: string;
  schritte: string[];
}

export const PROZESSE: ProzessDoc[] = [
  {
    id: "laufwerk-prj",
    titel: "Projektlaufwerk anlegen",
    kurz: "Fileserver → AD-Gruppen → DFS (BLN/BEB)",
    schritte: [
      "Projektordner unter \\\\helios-dom...\\{bln|beb}\\Support\\Projekte\\…-PRJ{1|2} anlegen",
      "Unterordner (Laufwerk) anlegen",
      "Sicherheitsgruppe FR anlegen und in BLN-LW-FS0x-PRJx-R / BEB-LW-FS02-PRJ1-R aufnehmen",
      "Lese- (R) und Schreibgruppe (W) nach Schema Standort-LW-PRJ-Projekt_Ordner-{R|W}",
      "DFS-Namespace-Ordner = Projektname, Ordnerziel setzen, explizite Anzeigeberechtigungen inkl. FR-Gruppe",
      "NTFS: nur Änderungsrechte (kein Vollzugriff); Link in AD-Beschreibung; User in Gruppen; Ticket schließen",
    ],
  },
  {
    id: "ooo",
    titel: "Abwesenheitsnotiz (Exchange)",
    kurz: "EX2019 Management Shell — nur auf Anfrage",
    schritte: [
      "Benötigt: Abwesenheitsnotiz-Text + Startdatum/Zeitraum (+ Username)",
      "$Message = \"…<br><br>…\" setzen",
      "Set-MailboxAutoReplyConfiguration -Identity USERNAME -DomainController ZDHDDC18.helios-dom.helios-kliniken.de -AutoReplyState Enabled -InternalMessage $Message -ExternalMessage $Message",
      "Optional: -StartTime für geplante Aktivierung",
      "Bei Ausscheiden: Standardtext mit Nachfolger + Abteilung verwenden",
    ],
  },
];
