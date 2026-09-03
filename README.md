# Helios Master Matrix

Catch & Dispatch knowledge base for Helios assignment groups, clusters, waves and applications.

## Files

- `matrix.html` — knowledge base and UI
- `data/kb.json` — knowledge base data (JSON)

## Routing rule (Wave go-live)

- **Go-live** location / cluster / region → use **ONLY Global Helios Groups**
- **Pre-wave** (not go-live yet) → use **local / legacy groups** for that location
- Go-live dates are on the Waves tab

| Wave | Go-live date |
|------|----------------|
| 1 | 29/07/2026 |
| 2 | 26/08/2026 |
| 3 | 23/09/2026 |
| 4 | 16/10/2026 |
| 5 | 30/10/2026 |

## Tabs

| Tab | Purpose |
|-----|---------|
| Start | Search clusters, locations, applications and groups |
| Application Base | Applications by cluster |
| Waves | Wave 1–5 planning, go-live dates and local routing |
| Regions | Nord / Ost / Süd / West |
| Clusters | Cluster and location assignment groups |
| Med. Clusters | Helios Med. Cluster map clinics (local IT or cluster/region fallback) |
| Berlin Groups | Berlin / Brandenburg routing |
| Global Helios Groups | Global Helios assignment groups (go-live) |
| Changelog | Matrix content changes |

Document information (version, status, author) is shown in the footer.

## knowledge/

Service Desk knowledge base for Helios / Fresenius agents.

| Folder | Content |
|--------|---------|
| `prompt.md` | Agent prompt: what to determine, routing priority, response format |
| `routing/` | Global Helios groups, assignment rules, waves, Berlin groups, ticket template |
| `applications/` | Application cards: criticality, keywords, routing per location, troubleshooting |
| `locations/` | Location cards: region, cluster, wave, routing per area |
| `clusters/` | Cluster cards with assignment groups |
| `service_groups/` | Group responsibilities and escalations |
| `troubleshooting/` | Guides: what to collect, checks, routing |
| `reference/` | Generated from the matrix: locations, regions, clusters, application catalog |

Rebuild after changing `data/knowledge-source.json` or `data/kb.json`:

```bash
python3 tools/seed_knowledge_source.py   # optional: re-seed curated cards from the matrix
python3 tools/build_knowledge.py         # writes knowledge/*.md, data/knowledge.json, KB.knowledge
```

Assignment groups are never invented: anything unconfirmed stays `TBD`.
