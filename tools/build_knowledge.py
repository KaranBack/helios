#!/usr/bin/env python3
"""Build the knowledge/ markdown tree and KB.knowledge from curated data + data/kb.json.

Curated content (agent prompt, routing rules, application and location cards,
service groups, troubleshooting guides) lives in data/knowledge-source.json.
Reference pages are generated from data/kb.json so they stay in sync.

Assignment groups are never invented here: anything not confirmed stays "TBD".
"""

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB_PATH = ROOT / "data" / "kb.json"
SRC_PATH = ROOT / "data" / "knowledge-source.json"
OUT_DIR = ROOT / "knowledge"
KNOWLEDGE_JSON = ROOT / "data" / "knowledge.json"


def slug(text):
    s = str(text).lower()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "item"


def md_list(items, bullet="-"):
    return "\n".join(f"{bullet} {i}" for i in items if i)


def md_numbered(items):
    return "\n".join(f"{i + 1}. {v}" for i, v in enumerate(items) if v)


def md_kv_block(title, value):
    if not value:
        return ""
    return f"{title}:\n{value}\n"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return str(path.relative_to(ROOT))


def render_prompt(p):
    out = ["# Helios Service Desk AI Assistant", ""]
    out.append(md_kv_block("Goal", p.get("goal", "")))
    if p.get("determine"):
        out.append("Always determine:\n\n" + md_numbered(p["determine"]) + "\n")
    if p.get("routingPriority"):
        out.append("Routing Priority:\n\n" + md_numbered(p["routingPriority"]) + "\n")
    if p.get("sap"):
        out.append("SAP:\n\n" + p["sap"] + "\n")
    if p.get("clinical"):
        out.append("Clinical Applications:\n\n" + p["clinical"] + "\n")
    if p.get("responseFormat"):
        out.append("Response Format:\n\n" + md_list(p["responseFormat"]) + "\n")
    if p.get("requiredInformation"):
        out.append("Required Information:\n\n" + md_list(p["requiredInformation"]) + "\n")
    if p.get("ticketDefaults"):
        out.append("Ticket defaults:\n\n" + md_list(p["ticketDefaults"]) + "\n")
    if p.get("searchPriority"):
        out.append("Always search knowledge/ before answering.\n\nPriority:\n\n"
                   + md_numbered(p["searchPriority"]) + "\n")
    if p.get("rules"):
        out.append(md_list(p["rules"]) + "\n")
    return "\n".join(out)


def render_application(app):
    out = [f"# {app['name']}", ""]
    if app.get("aliases"):
        out.append(md_kv_block("Alias", ", ".join(app["aliases"])))
    if app.get("type"):
        out.append(md_kv_block("Type", app["type"]))
    if app.get("criticality"):
        out.append(md_kv_block("Criticality", app["criticality"]))
    if app.get("defaultGroup"):
        out.append(md_kv_block("Assignment Group", app["defaultGroup"]))
    if app.get("description"):
        out.append(md_kv_block("Description", app["description"]))
    if app.get("keywords"):
        out.append("Keywords:\n\n" + md_list(app["keywords"]) + "\n")
    if app.get("routing"):
        rows = [f"{loc}:\n{grp}" for loc, grp in app["routing"].items()]
        out.append("Routing:\n\n" + "\n\n".join(rows) + "\n")
    if app.get("requiredInformation"):
        out.append("Required Information:\n\n" + md_list(app["requiredInformation"]) + "\n")
    if app.get("troubleshooting"):
        out.append("Troubleshooting:\n\n" + md_numbered(app["troubleshooting"]) + "\n")
    if app.get("note"):
        out.append(md_kv_block("Note", app["note"]))
    return "\n".join(out)


def render_location(loc):
    out = [f"# {loc['name']}", ""]
    for label, key in [("Region", "region"), ("Cluster", "cluster"), ("Med. Cluster", "medCluster"),
                       ("Wave", "wave"), ("Go-live", "goLiveDate"), ("Service Unit", "serviceUnit"),
                       ("Default Group", "defaultGroup")]:
        if loc.get(key):
            out.append(md_kv_block(label, str(loc[key])))
    if loc.get("applications"):
        out.append("Applications:\n\n" + md_list(loc["applications"]) + "\n")
    if loc.get("routing"):
        rows = [f"{area}:\n{grp}" for area, grp in loc["routing"].items()]
        out.append("Routing:\n\n" + "\n\n".join(rows) + "\n")
    if loc.get("note"):
        out.append(md_kv_block("Note", loc["note"]))
    return "\n".join(out)


def render_service_group(g):
    out = [f"# {g['name']}", ""]
    if g.get("scope"):
        out.append(md_kv_block("Scope", g["scope"]))
    if g.get("responsibilities"):
        out.append("Responsibilities:\n\n" + md_list(g["responsibilities"]) + "\n")
    if g.get("escalations"):
        rows = [f"{area}:\n{grp}" for area, grp in g["escalations"].items()]
        out.append("Escalations:\n\n" + "\n\n".join(rows) + "\n")
    if g.get("note"):
        out.append(md_kv_block("Note", g["note"]))
    return "\n".join(out)


def render_troubleshooting(t):
    out = [f"# {t['title']}", ""]
    if t.get("collect"):
        out.append("Collect:\n\n" + md_list(t["collect"]) + "\n")
    if t.get("checks"):
        out.append("Checks:\n\n" + md_numbered(t["checks"]) + "\n")
    if t.get("routing"):
        rows = [f"{scope}:\n{grp}" for scope, grp in t["routing"].items()]
        out.append("Routing:\n\n" + "\n\n".join(rows) + "\n")
    if t.get("note"):
        out.append(md_kv_block("Note", t["note"]))
    return "\n".join(out)


def render_global_groups(rows):
    out = ["# Global Helios Groups", ""]
    for r in rows:
        out.append(f"## {r['service']}\n")
        out.append(f"Group:\n{r['group']}\n")
        if r.get("rule"):
            out.append(f"Rule:\n{r['rule']}\n")
    return "\n".join(out)


def render_assignment_rules(rules, policy):
    out = ["# Assignment Rules", ""]
    out.append(md_kv_block("Rule", policy.get("rule", "")))
    out.append(md_kv_block("Short rule", policy.get("shortRule", "")))
    out.append("Priority:\n\n" + md_numbered(rules.get("priority", [])) + "\n")
    if rules.get("rules"):
        out.append("Rules:\n\n" + md_list(rules["rules"]) + "\n")
    if rules.get("neverInvent"):
        out.append(md_kv_block("Constraint", rules["neverInvent"]))
    return "\n".join(out)


def render_waves(kb):
    out = ["# Waves", "", "| Wave | Go-live date | Status | Routing |", "|---|---|---|---|"]
    for w in sorted((kb.get("waveGoLive") or {}).keys()):
        s = kb["waveGoLive"][w]
        routing = ("ONLY Global Helios Groups · SAP → SAP Basis · Clinical → local IT"
                   if s.get("goLive") else "Local / legacy groups")
        out.append(f"| {w} | {s.get('goLiveDate', '')} | {s.get('status', '')} | {routing} |")
    out.append("")
    out.append("## Service Units")
    out.append("")
    out.append("| Service Unit | Wave | Go-live | KRITIS |")
    out.append("|---|---|---|---|")
    for u in (kb.get("planning") or {}).get("serviceUnits") or []:
        out.append(f"| {u.get('unit', '')} | {u.get('wave', '')} | {u.get('goLiveDate', '')} | "
                   f"{'yes' if u.get('kritis') else 'no'} |")
    return "\n".join(out)


def render_berlin(kb):
    b = kb.get("berlin") or {}
    out = ["# Berlin Groups", ""]
    if b.get("assignmentGroups"):
        out.append("| Group | Responsibility |")
        out.append("|---|---|")
        for g in b["assignmentGroups"]:
            out.append(f"| {g.get('group', '')} | {g.get('responsibility', '')} |")
        out.append("")
    if b.get("requiredInfo"):
        out.append("Required Information:\n\n" + md_list(b["requiredInfo"]) + "\n")
    if b.get("keywords"):
        out.append("| Keyword | Group |")
        out.append("|---|---|")
        for k in b["keywords"]:
            out.append(f"| {k.get('keyword', '')} | {k.get('group', '')} |")
    return "\n".join(out)


def render_ticket_template(items):
    out = ["# Ticket Template", "", "## Mandatory Information", ""]
    for i, t in enumerate(items):
        out.append(f"### {i + 1}. {t['field']}")
        out.append("")
        if t.get("detail"):
            out.append(t["detail"])
            out.append("")
        if t.get("default"):
            out.append("Default value:")
            out.append("")
            out.append("```")
            out.append(t["default"])
            out.append("```")
            out.append("")
    return "\n".join(out)


def render_service_desk_kb(kb_doc):
    out = ["# Global IT Service Desk Knowledge Base", "", "## Purpose", "", kb_doc["purpose"], ""]

    out.append("## Incident Prioritization\n")
    for p in kb_doc["prioritization"]:
        out.append(f"### {p['level']} ({p['name']})\n")
        out.append("Conditions:\n\n" + md_list(p["conditions"]) + "\n")
        out.append("Action:\n\n" + md_list(p["action"]) + "\n")

    out.append("## Troubleshooting Methodology\n")
    for s in kb_doc["methodology"]:
        out.append(f"### {s['step']} — {s['title']}\n")
        out.append(md_list(s["items"]) + "\n")

    out.append("## Escalation Rules\n")
    for r in kb_doc["escalationRules"]:
        out.append(f"### Escalate to {r['target']}\n")
        out.append(md_list(r["issues"]) + "\n")

    out.append("## User Communication Standards\n")
    for c in kb_doc["communication"]:
        out.append(f"### {c['stage']}\n")
        out.append(md_list(c["items"]) + "\n")

    pk = kb_doc.get("priorityKeywords")
    if pk:
        out.append("## Priority Keywords (clinical)\n")
        if pk.get("note"):
            out.append(pk["note"] + "\n")
        for lvl in pk.get("levels", []):
            out.append(f"### {lvl['level']} — {lvl['name']}\n")
            out.append(md_list(lvl["keywords"]) + "\n")

    op = kb_doc.get("outagePriorities")
    if op:
        out.append("## Outage Priorities\n")
        for lvl in op.get("levels", []):
            out.append(f"### {lvl['level']}\n")
            out.append(md_list(lvl["conditions"]) + "\n")
        m = op.get("matrix") or {}
        if m.get("rows"):
            out.append(m.get("note", "") + "\n")
            out.append("| Impact \\ Urgency | High (1) | Medium (2) | Low (3) |")
            out.append("|---|---|---|---|")
            for r in m["rows"]:
                out.append(f"| {r['impact']} | {r['High (1)']} | {r['Medium (2)']} | {r['Low (3)']} |")
            out.append("")
        if op.get("planningOnly"):
            out.append(op["planningOnly"] + "\n")
        if op.get("outageCriteria"):
            out.append("Open an outage when:\n\n" + md_list(op["outageCriteria"]) + "\n")

    out.append("## Major Incident Process\n")
    out.append("Identification:\n\n" + md_list(kb_doc["majorIncident"]["identification"]) + "\n")
    out.append("Actions:\n\n" + md_numbered(kb_doc["majorIncident"]["actions"]) + "\n")

    out.append("## Active Directory Procedures\n")
    for a in kb_doc["adProcedures"]:
        out.append(f"### {a['topic']}\n")
        out.append("Verify:\n\n" + md_list(a["verify"]) + "\n")

    out.append("## Remote Support Checklist\n")
    out.append("Before connecting:\n\n" + md_list(kb_doc["remoteSupport"]["before"]) + "\n")
    out.append("Verify:\n\n" + md_list(kb_doc["remoteSupport"]["verify"]) + "\n")
    out.append("Document:\n\n" + md_list(kb_doc["remoteSupport"]["document"]) + "\n")

    out.append("## Routing Matrix Structure\n")
    out.append(md_list([f"**{f['field']}** — {f['detail']}" for f in kb_doc["routingMatrixStructure"]]) + "\n")

    out.append("## Best Practices\n")
    out.append(md_list(kb_doc["bestPractices"]) + "\n")
    return "\n".join(out)


def render_major_incident_process(mi):
    out = ["# Major Incident Handling (FDT)", ""]
    out.append(md_kv_block("Source", mi.get("source", "")))
    out.append(md_kv_block("Effective", mi.get("effective", "")))
    out.append("## Important notice\n")
    out.append(md_list(mi.get("importantNotice", [])) + "\n")
    out.append("## Propose Major Incident — step by step\n")
    out.append(md_numbered(mi.get("steps", [])) + "\n")
    pf = mi.get("proposalFields") or {}
    if pf:
        out.append("## Proposal pop-up fields\n")
        out.append("Work Notes:\n\n" + md_list(pf.get("workNotes", [])) + "\n")
        out.append("Business Impact:\n\n" + md_list(pf.get("businessImpact", [])) + "\n")
    if mi.get("businessImpactQuestions"):
        out.append("## Business impact questions (collect before proposing)\n")
        out.append(md_numbered(mi["businessImpactQuestions"]) + "\n")
    for title, key in [("After promotion", "afterPromotion"),
                       ("Outage related / child ticket", "childTicket"),
                       ("Escalated P2", "escalatedP2"),
                       ("FME tickets affecting FDT systems (eBonding)", "fmeEbonding"),
                       ("IVR", "ivr"),
                       ("Ticket escalation", "ticketEscalation")]:
        if mi.get(key):
            out.append(f"## {title}\n")
            out.append(md_list(mi[key]) + "\n")
    if mi.get("contacts"):
        out.append("## Contacts\n")
        out.append("| Role | Details |")
        out.append("|---|---|")
        for c in mi["contacts"]:
            out.append(f"| {c['role']} | {c['detail']} |")
        out.append("")
    if mi.get("escalationLevels"):
        out.append("## Escalation matrix (MIM hotline unreachable)\n")
        out.append("| Level | Name | Mail | Phone |")
        out.append("|---|---|---|---|")
        for e in mi["escalationLevels"]:
            out.append(f"| {e['level']} | {e['name']} | {e['mail']} | {e['phone']} |")
        out.append("")
    return "\n".join(out)


def render_priority_keywords(pk):
    out = ["# Priority Keywords", ""]
    out.append(md_kv_block("Source", pk.get("source", "")))
    if pk.get("note"):
        out.append(pk["note"] + "\n")
    for lvl in pk.get("levels", []):
        out.append(f"## {lvl['level']} — {lvl['name']}\n")
        out.append(md_list(lvl["keywords"]) + "\n")
    return "\n".join(out)


def render_reference_snow(kb):
    rows = kb.get("snowLocations") or []
    out = ["# Helios SNOW Location Registry", "",
           f"Total: {len(rows)} entries. Street addresses, zip codes and phone numbers are not imported.", "",
           "| Name | City | Type | Related Cluster | Related Region |",
           "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x.get("region", ""), x.get("name", ""))):
        out.append(f"| {r.get('name', '')} | {r.get('city', '')} | {r.get('locationType', '')} | "
                   f"{r.get('cluster', '')} | {r.get('region', '')} |")
    return "\n".join(out)


def render_fhs(fhs):
    out = [f"# {fhs['title']}", ""]
    n = fhs.get("notice") or {}
    if n:
        out.append(f"## {n.get('title', 'Notice')}\n")
        out.append(n.get("text", "") + "\n")
        if n.get("contact"):
            out.append(md_kv_block("Contact", n["contact"]))
    co = fhs.get("coexistence") or {}
    if co.get("rows"):
        out.append(f"## {co.get('title', 'Coexisting phase')}\n")
        if co.get("note"):
            out.append(co["note"] + "\n")
        out.append("| App | Account | Description | Comment |")
        out.append("|---|---|---|---|")
        for r in co["rows"]:
            out.append(f"| {r['app']} | {r['account']} | {r['description']} | {r.get('comment', '')} |")
        out.append("")
    sup = fhs.get("support") or {}
    if sup.get("channels"):
        out.append(f"## {sup.get('title', 'Support')}\n")
        out.append("| Channel | Details |")
        out.append("|---|---|")
        for c in sup["channels"]:
            out.append(f"| {c['channel']} | {c['detail']} |")
        out.append("")
    if sup.get("links"):
        out.append("Useful links:\n\n" + md_list(sup["links"]) + "\n")
    return "\n".join(out)


def render_template(t):
    out = [f"# {t['title']}", ""]
    for s in t.get("sections", []):
        out.append(f"## {s['heading']}\n")
        if s.get("body"):
            out.append(s["body"] + "\n")
        if s.get("items"):
            out.append(md_list(s["items"]) + "\n")
    return "\n".join(out)


def render_agent_prompt(p):
    out = [f"# {p['title']}", ""]
    out.append(md_kv_block("Purpose", p.get("purpose", "")))
    if p.get("instructions"):
        out.append("Instructions:\n\n" + md_numbered(p["instructions"]) + "\n")
    if p.get("output"):
        out.append("Output:\n\n" + md_list(p["output"]) + "\n")
    return "\n".join(out)


def render_routing_matrix(r):
    out = [f"# {r['location']}", ""]
    out.append(md_kv_block("Location", r["location"]))
    if r.get("wave"):
        out.append(md_kv_block("Wave", str(r["wave"])))
    out.append(md_kv_block("Assignment Group", r.get("assignmentGroup", "")))
    if r.get("serviceScope"):
        out.append("Service Scope:\n\n" + md_list(r["serviceScope"]) + "\n")
    if r.get("escalationPath"):
        rows = [f"{k}:\n{v}" for k, v in r["escalationPath"].items()]
        out.append("Escalation Path:\n\n" + "\n\n".join(rows) + "\n")
    if r.get("notes"):
        out.append(md_kv_block("Notes", r["notes"]))
    return "\n".join(out)


def render_reference_locations(kb):
    out = ["# Helios Locations", "",
           f"Total: {len(kb.get('heliosLocations') or [])} locations "
           "(no street addresses, ticket volumes or FTE).", "",
           "| Location | City | Wave | Go-live | Service Unit | Group hub | Region |",
           "|---|---|---|---|---|---|---|"]
    for l in sorted(kb.get("heliosLocations") or [], key=lambda x: (str(x.get("city") or ""), x["name"])):
        out.append(f"| {l['name']} | {l.get('city', '')} | {l.get('wave', '')} | "
                   f"{l.get('goLiveDate', '')} | {l.get('serviceUnit', '')} | "
                   f"{l.get('groupHub', '')} | {l.get('region', '')} |")
    return "\n".join(out)


def render_reference_regions(kb):
    regions = {}
    for l in kb.get("heliosLocations") or []:
        regions.setdefault(l.get("region") or "—", []).append(l)
    out = ["# Helios Regions", "", "| Region | Locations | Waves |", "|---|---|---|"]
    for r, items in sorted(regions.items()):
        waves = sorted({str(i.get("wave")) for i in items if i.get("wave")})
        out.append(f"| {r} | {len(items)} | {', '.join(waves)} |")
    return "\n".join(out)


def render_reference_clusters(kb):
    out = ["# Helios Clusters", "",
           "| Cluster / site | Service Desk | Infrastructure | Clinical | SAP | Field Service |",
           "|---|---|---|---|---|---|"]
    for name in sorted(kb.get("clusters") or {}):
        c = kb["clusters"][name]
        out.append(f"| {name} | {c.get('ServiceDesk', '')} | {c.get('Infrastructure', '')} | "
                   f"{c.get('Clinical', '')} | {c.get('SAP', '')} | {c.get('FieldService', '')} |")
    out.append("")
    out.append("## Med. Clusters")
    out.append("")
    out.append("| Med. Cluster | Fallback group | Clinics | Locations |")
    out.append("|---|---|---|---|")
    for mc in (kb.get("medClusters") or {}).get("clusters") or []:
        out.append(f"| {mc['name']} | {mc.get('fallbackGroup', '')} | "
                   f"{len(mc.get('clinics') or [])} | {len(mc.get('sites') or [])} |")
    return "\n".join(out)


def render_application_catalog(kb, apps):
    out = ["# Application Catalog", "",
           "Assignment groups per site come from the site software matrices in the matrix "
           "(`siteApps`). TBD means the source left the group blank.", ""]
    for site, data in sorted((kb.get("siteApps") or {}).items()):
        out.append(f"## {site}")
        out.append("")
        if data.get("note"):
            out.append(data["note"])
            out.append("")
        out.append("| Software | Kritikalität | Assignment Group |")
        out.append("|---|---|---|")
        for a in data.get("apps") or []:
            out.append(f"| {a['application']} | {a.get('criticality', '')} | {a.get('group') or 'TBD'} |")
        out.append("")
    if apps:
        out.append("## Application cards")
        out.append("")
        out.append("| Application | Criticality | Default group |")
        out.append("|---|---|---|")
        for a in apps:
            out.append(f"| {a['name']} | {a.get('criticality', '')} | {a.get('defaultGroup') or 'TBD'} |")
    return "\n".join(out)


def main():
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))
    src = json.loads(SRC_PATH.read_text(encoding="utf-8"))

    files = []

    files.append({"path": write(OUT_DIR / "prompt.md", render_prompt(src["prompt"])),
                  "title": "Agent prompt", "category": "prompt"})

    files.append({"path": write(OUT_DIR / "routing" / "global_helios_groups.md",
                                render_global_groups(src["routing"]["globalHeliosGroups"])),
                  "title": "Global Helios Groups", "category": "routing"})
    files.append({"path": write(OUT_DIR / "routing" / "assignment_rules.md",
                                render_assignment_rules(src["routing"]["assignmentRules"],
                                                        kb.get("routingPolicy") or {})),
                  "title": "Assignment Rules", "category": "routing"})
    files.append({"path": write(OUT_DIR / "routing" / "waves.md", render_waves(kb)),
                  "title": "Waves", "category": "routing"})
    files.append({"path": write(OUT_DIR / "routing" / "berlin_groups.md", render_berlin(kb)),
                  "title": "Berlin Groups", "category": "routing"})
    files.append({"path": write(OUT_DIR / "routing" / "ticket_template.md",
                                render_ticket_template(src["ticketTemplate"])),
                  "title": "Ticket Template", "category": "routing"})

    for app in src["applications"]:
        files.append({"path": write(OUT_DIR / "applications" / f"{slug(app.get('id') or app['name'])}.md",
                                    render_application(app)),
                      "title": app["name"], "category": "applications"})

    for loc in src["locations"]:
        files.append({"path": write(OUT_DIR / "locations" / f"{slug(loc.get('id') or loc['name'])}.md",
                                    render_location(loc)),
                      "title": loc["name"], "category": "locations"})

    for cl in src.get("clusters", []):
        files.append({"path": write(OUT_DIR / "clusters" / f"{slug(cl.get('id') or cl['name'])}.md",
                                    render_location(cl)),
                      "title": cl["name"], "category": "clusters"})

    for g in src["serviceGroups"]:
        files.append({"path": write(OUT_DIR / "service_groups" / f"{slug(g.get('id') or g['name'])}.md",
                                    render_service_group(g)),
                      "title": g["name"], "category": "service_groups"})

    for t in src["troubleshooting"]:
        files.append({"path": write(OUT_DIR / "troubleshooting" / f"{slug(t.get('id') or t['title'])}.md",
                                    render_troubleshooting(t)),
                      "title": t["title"], "category": "troubleshooting"})

    files.append({"path": write(OUT_DIR / "knowledge_base.md",
                                render_service_desk_kb(src["serviceDeskKb"])),
                  "title": "Global IT Service Desk Knowledge Base", "category": "process"})

    if src["serviceDeskKb"].get("majorIncidentProcess"):
        files.append({"path": write(OUT_DIR / "process" / "major_incident_handling.md",
                                    render_major_incident_process(src["serviceDeskKb"]["majorIncidentProcess"])),
                      "title": "Major Incident Handling (FDT)", "category": "process"})
    if src["serviceDeskKb"].get("priorityKeywords"):
        files.append({"path": write(OUT_DIR / "routing" / "priority_keywords.md",
                                    render_priority_keywords(src["serviceDeskKb"]["priorityKeywords"])),
                      "title": "Priority Keywords", "category": "routing"})

    if src.get("fhs"):
        files.append({"path": write(OUT_DIR / "fhs" / "coexistence.md", render_fhs(src["fhs"])),
                      "title": "FHS — Fresenius Health Services", "category": "fhs"})

    for t in src.get("templates", []):
        files.append({"path": write(OUT_DIR / "templates" / f"{slug(t.get('id') or t['title'])}.md",
                                    render_template(t)),
                      "title": t["title"], "category": "templates"})

    for p in src.get("prompts", []):
        files.append({"path": write(OUT_DIR / "prompts" / f"{slug(p.get('id') or p['title'])}.md",
                                    render_agent_prompt(p)),
                      "title": p["title"], "category": "prompts"})

    for r in src.get("routingMatrix", []):
        files.append({"path": write(OUT_DIR / "routing_matrix" / f"{slug(r.get('id') or r['location'])}.md",
                                    render_routing_matrix(r)),
                      "title": r["location"], "category": "routing_matrix"})

    files.append({"path": write(OUT_DIR / "reference" / "helios_locations.md",
                                render_reference_locations(kb)),
                  "title": "Helios Locations", "category": "reference"})
    files.append({"path": write(OUT_DIR / "reference" / "helios_regions.md",
                                render_reference_regions(kb)),
                  "title": "Helios Regions", "category": "reference"})
    files.append({"path": write(OUT_DIR / "reference" / "helios_clusters.md",
                                render_reference_clusters(kb)),
                  "title": "Helios Clusters", "category": "reference"})
    files.append({"path": write(OUT_DIR / "reference" / "application_catalog.md",
                                render_application_catalog(kb, src["applications"])),
                  "title": "Application Catalog", "category": "reference"})
    if kb.get("snowLocations"):
        files.append({"path": write(OUT_DIR / "reference" / "snow_locations.md",
                                    render_reference_snow(kb)),
                      "title": "Helios SNOW Location Registry", "category": "reference"})

    knowledge = {
        "meta": dict(src["meta"], files=len(files)),
        "prompt": src["prompt"],
        "ticketTemplate": src["ticketTemplate"],
        "routing": src["routing"],
        "serviceDeskKb": src.get("serviceDeskKb", {}),
        "fhs": src.get("fhs", {}),
        "templates": src.get("templates", []),
        "prompts": src.get("prompts", []),
        "routingMatrix": src.get("routingMatrix", []),
        "applications": src["applications"],
        "locations": src["locations"],
        "clusters": src.get("clusters", []),
        "serviceGroups": src["serviceGroups"],
        "troubleshooting": src["troubleshooting"],
        "files": files,
    }

    KNOWLEDGE_JSON.write_text(json.dumps(knowledge, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    kb["knowledge"] = knowledge
    KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"knowledge files: {len(files)}")
    for cat in ["prompt", "process", "routing", "routing_matrix", "fhs", "templates", "prompts",
                "applications", "locations", "clusters", "service_groups",
                "troubleshooting", "reference"]:
        print(f"  {cat}: {sum(1 for f in files if f['category'] == cat)}")


if __name__ == "__main__":
    main()
