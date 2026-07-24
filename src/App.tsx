import { useDeferredValue, useMemo, useState } from "react";
import "./App.css";
import {
  CHECKLISTE,
  KATEGORIEN,
  MATRIX,
  PROZESSE,
  ROLLEN,
  STANDORTE,
  type Kategorie,
  type Rolle,
  type Standort,
} from "./data/matrix";

type Tab = "matrix" | "checkliste" | "prozesse";

function App() {
  const [tab, setTab] = useState<Tab>("matrix");
  const [standort, setStandort] = useState<Standort | "all">("all");
  const [rolle, setRolle] = useState<Rolle | "all">("all");
  const [kategorie, setKategorie] = useState<Kategorie | "all">("all");
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  const filtered = useMemo(() => {
    const q = deferredQuery.trim().toLowerCase();
    return MATRIX.filter((row) => {
      if (standort !== "all" && !row.standorte.includes(standort)) return false;
      if (rolle !== "all") {
        const matchRole =
          row.rollen.includes(rolle) || row.rollen.includes("alle");
        if (!matchRole) return false;
      }
      if (kategorie !== "all" && row.kategorie !== kategorie) return false;
      if (!q) return true;
      const hay = [
        row.system,
        row.gruppe,
        row.hinweis ?? "",
        ...row.standorte,
        row.kategorie,
      ]
        .join(" ")
        .toLowerCase();
      return hay.includes(q);
    });
  }, [standort, rolle, kategorie, deferredQuery]);

  return (
    <div className="app">
      <header className="masthead">
        <div className="brand-row">
          <div className="brand-mark" aria-hidden>
            H
          </div>
          <div className="brand-text">
            <h1 className="brand-name">HELIOS Matrix</h1>
            <p className="brand-sub">
              Cluster Berlin-Brandenburg · Benutzerrechte &amp; AD-Gruppen
            </p>
          </div>
        </div>
        <p className="lede">
          Schnellreferenz für First-Level: Welche AD-Gruppen gehören zu Standort,
          Rolle und System — aus den Benutzeranträgen BLN / BEB / BS, inkl.
          PDMS, Muse und Zenzy.
        </p>
      </header>

      <nav className="tabs" aria-label="Bereiche">
        {(
          [
            ["matrix", "Berechtigungsmatrix"],
            ["checkliste", "Checkliste Antrag"],
            ["prozesse", "Prozesse"],
          ] as const
        ).map(([id, label]) => (
          <button
            key={id}
            type="button"
            className={`tab${tab === id ? " active" : ""}`}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </nav>

      {tab === "matrix" && (
        <>
          <div className="standort-strip">
            {STANDORTE.map((s) => (
              <div key={s.code} className="standort-pill">
                <div className="code">{s.code}</div>
                <div className="name">{s.name}</div>
                <div className="script">{s.loginScript}</div>
              </div>
            ))}
          </div>

          <div className="toolbar">
            <div className="filters">
              <div className="field">
                <label htmlFor="q">Suche</label>
                <input
                  id="q"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Gruppe, System, Hinweis…"
                />
              </div>
              <div className="field">
                <label htmlFor="standort">Standort</label>
                <select
                  id="standort"
                  value={standort}
                  onChange={(e) =>
                    setStandort(e.target.value as Standort | "all")
                  }
                >
                  <option value="all">Alle</option>
                  {STANDORTE.map((s) => (
                    <option key={s.code} value={s.code}>
                      {s.code} – {s.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="rolle">Rolle</label>
                <select
                  id="rolle"
                  value={rolle}
                  onChange={(e) => setRolle(e.target.value as Rolle | "all")}
                >
                  <option value="all">Alle</option>
                  {ROLLEN.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="kat">Kategorie</label>
                <select
                  id="kat"
                  value={kategorie}
                  onChange={(e) =>
                    setKategorie(e.target.value as Kategorie | "all")
                  }
                >
                  <option value="all">Alle</option>
                  {KATEGORIEN.map((k) => (
                    <option key={k.id} value={k.id}>
                      {k.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="meta-row">
              <span className="chip">
                Treffer: <strong>{filtered.length}</strong> / {MATRIX.length}
              </span>
              <span className="chip">Quelle: Benutzeranträge RO-IT</span>
            </div>
          </div>

          <div className="panel">
            <div className="table-wrap">
              {filtered.length === 0 ? (
                <div className="empty">Keine Einträge für diese Filter.</div>
              ) : (
                <table className="matrix">
                  <thead>
                    <tr>
                      <th>Standort</th>
                      <th>Rolle</th>
                      <th>System</th>
                      <th>AD-Gruppe / Wert</th>
                      <th>Kategorie</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((row) => (
                      <tr key={row.id}>
                        <td>
                          <div className="badges">
                            {row.standorte.map((s) => (
                              <span
                                key={s}
                                className={`badge ${s.toLowerCase()}`}
                              >
                                {s}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td>
                          <div className="badges">
                            {row.rollen.map((r) => (
                              <span key={r} className="badge role">
                                {ROLLEN.find((x) => x.id === r)?.label ?? r}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td>{row.system}</td>
                        <td>
                          <div className="mono">{row.gruppe}</div>
                          {row.hinweis && (
                            <div className="hint">{row.hinweis}</div>
                          )}
                        </td>
                        <td>
                          {KATEGORIEN.find((k) => k.id === row.kategorie)
                            ?.label ?? row.kategorie}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </>
      )}

      {tab === "checkliste" && (
        <div className="check-list">
          {CHECKLISTE.map((item, i) => (
            <article key={item.id} className="check-item">
              <div className="check-num">{i + 1}</div>
              <div>
                <h3>{item.titel}</h3>
                <p>{item.details}</p>
              </div>
            </article>
          ))}
        </div>
      )}

      {tab === "prozesse" && (
        <div className="grid-cards">
          {PROZESSE.map((p) => (
            <article key={p.id} className="doc-card">
              <h3>{p.titel}</h3>
              <p>{p.kurz}</p>
              <ol>
                {p.schritte.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ol>
            </article>
          ))}
        </div>
      )}

      <p className="footer-note">
        Interne Arbeitsmatrix · Kein Ersatz für WikIT / ZD-IT-Richtlinien.
        Datenstand aus bereitgestellten Benutzeranträgen, Laufwerks-Anlage und
        Abwesenheitsnotiz-Doku.
      </p>
    </div>
  );
}

export default App;
