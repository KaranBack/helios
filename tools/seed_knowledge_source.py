#!/usr/bin/env python3
"""Seed data/knowledge-source.json for the knowledge/ tree.

Curated cards (prompt, routing rules, application and troubleshooting guides) are
written here; location, cluster and service-group cards are filled from data/kb.json
so assignment groups always come from the matrix instead of being invented.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB = json.loads((ROOT / "data" / "kb.json").read_text(encoding="utf-8"))
OUT = ROOT / "data" / "knowledge-source.json"

CLUSTERS = KB["clusters"]
GROUP_DIR = {g["name"]: g for g in KB.get("groupDirectory") or []}
SITE_APPS = KB.get("siteApps") or {}
CLUSTER_META = KB.get("clusterMeta") or {}
LOCS = KB.get("heliosLocations") or []

AREA_KEYS = [
    ("Service Desk", "ServiceDesk"),
    ("Account Management", "Account"),
    ("Infrastructure", "Infrastructure"),
    ("Clinical", "Clinical"),
    ("SAP", "SAP"),
    ("Field Service", "FieldService"),
]


def wave_of(name):
    meta = CLUSTER_META.get(name) or {}
    if meta.get("waves"):
        return meta["waves"][0]
    for l in LOCS:
        if l.get("matrixKey") == name or l.get("groupHub") == name:
            return l.get("wave")
    return ""


def go_live_of(wave):
    return ((KB.get("waveGoLive") or {}).get(str(wave)) or {}).get("goLiveDate", "")


def routing_from_cluster(name, overrides=None):
    c = CLUSTERS.get(name) or {}
    routing = {}
    for label, key in AREA_KEYS:
        if c.get(key) and c[key] != "TBD":
            routing[label] = c[key]
    for extra in ("Orbis", "Muse", "JiveX", "iMedOne", "Software", "Netzwerk"):
        if c.get(extra) and c[extra] != "TBD":
            routing[extra] = c[extra]
    if overrides:
        routing.update(overrides)
    return routing


def apps_for_site(site):
    return [a["application"] for a in (SITE_APPS.get(site) or {}).get("apps") or []]


CLUSTER_APP_KEYS = {"orbis": "Orbis", "cgm muse": "Muse", "jivex": "JiveX", "imedone": "iMedOne"}


def app_routing(app_name):
    """Assignment group per site for one application, from the site software matrices
    and from cluster-specific application overrides in the matrix."""
    routing = {}
    for site, data in SITE_APPS.items():
        for a in data.get("apps") or []:
            if a["application"].lower() == app_name.lower():
                routing[site] = a.get("group") or "TBD"
    cluster_key = CLUSTER_APP_KEYS.get(app_name.lower())
    if cluster_key:
        for name, c in CLUSTERS.items():
            if c.get(cluster_key) and c[cluster_key] != "TBD":
                routing.setdefault(name, c[cluster_key])
    return routing


def app_meta(app_name):
    for data in SITE_APPS.values():
        for a in data.get("apps") or []:
            if a["application"].lower() == app_name.lower():
                return a
    return {}


def location_card(name, key=None, extra=None):
    key = key or name
    meta = CLUSTER_META.get(key) or {}
    wave = wave_of(key)
    card = {
        "id": None,
        "name": name,
        "region": ", ".join(meta.get("regions") or []),
        "medCluster": meta.get("medCluster", ""),
        "wave": wave,
        "goLiveDate": go_live_of(wave),
        "defaultGroup": (CLUSTERS.get(key) or {}).get("ServiceDesk", ""),
        "routing": routing_from_cluster(key),
        "applications": apps_for_site(key),
    }
    if extra:
        card.update(extra)
    card["id"] = card.get("id") or name
    return card


def service_group_card(name, responsibilities=None, escalations=None, note=None):
    entry = GROUP_DIR.get(name) or {}
    card = {
        "id": name,
        "name": name,
        "scope": entry.get("description", ""),
        "responsibilities": responsibilities or [],
        "escalations": escalations or {},
    }
    if entry.get("manager"):
        card["note"] = f"Management group: {entry['manager']}" + (f". {note}" if note else "")
    elif note:
        card["note"] = note
    return card


prompt = {
    "goal": "Support Service Desk Analysts in the Helios environment.",
    "determine": ["Location", "Cluster", "Region", "Application", "Wave Status", "Assignment Group"],
    "routingPriority": ["Global Helios Group", "Local Cluster Group", "Local Site Group"],
    "sap": "Wave 1 / Wave 2: SAP Basis",
    "clinical": "Always stay on Local IT.",
    "responseFormat": ["Location", "Cluster", "Wave", "Assignment Group", "Reason"],
    "requiredInformation": ["User", "Hostname", "Error Message", "Business Impact"],
    "searchPriority": ["locations/", "applications/", "service_groups/", "routing/", "troubleshooting/"],
    "rules": [
        "Always search knowledge/ before answering.",
        "When the user provides a location and an application, always return: Assignment Group, Reason, Required Information, Initial Troubleshooting.",
        "Never invent assignment groups. Use only groups found in knowledge/.",
    ],
}

ticket_template = [
    "User details",
    "Phone number",
    "Location",
    "Issue description",
    "Start date of the issue",
    "Error message",
    "Observation during initial investigation",
    "Troubleshooting steps taken",
    "Hostname",
    "Windows version",
    "Availability",
]

global_helios_groups = [
    {"service": "Active Directory", "group": "Ext_WW_AD_FLS_Capgemini_Helios"},
    {"service": "Office365 / Outlook / Teams", "group": "Ext_WW_Collaboration_SLS_Capgemini_Helios"},
    {"service": "Printer Services", "group": "Ext_WW_Printer-Services_SLS_Capgemini_Helios"},
    {"service": "Network", "group": "Ext_WW_Network_SLS_Capgemini_Helios"},
    {"service": "Virtual Workplace", "group": "Ext_WW_Virtual-Workplace_SLS_Capgemini_Helios"},
    {"service": "Physical Workplace", "group": "Ext_WW_Physical-Workplace_SLS_Capgemini_Helios"},
    {"service": "Mobile Devices", "group": "Ext_WW_Mobile-Workplace_SLS_Capgemini_Helios"},
    {"service": "SAP", "group": "SAP Basis", "rule": "Wave 1 and Wave 2 only."},
]

assignment_rules = {
    "priority": ["Global Helios Group", "Local Cluster Group", "Local Site Group"],
    "rules": [
        "Wave go-live (Wave 1 and Wave 2): general topics use ONLY Global Helios Groups.",
        "Pre-wave (Wave 3-5): use the local / legacy groups of the location.",
        "SAP after go-live: SAP Basis.",
        "Clinical Applications: always the local IT group, before and after go-live.",
        "A site under a Wave hub uses the hub's Wave and assignment groups (e.g. Attendorn under CL-Wuppertal).",
    ],
    "neverInvent": "Only assignment groups present in the matrix / knowledge base may be used. Unknown groups stay TBD.",
}

applications = [
    {
        "id": "orbis",
        "name": "ORBIS",
        "type": "KIS",
        "criticality": "High",
        "description": "Hospital Information System.",
        "keywords": ["ORBIS", "KIS", "Patient Record", "Clinical Documentation"],
        "routing": {
            "Kassel": "KS-IT",
            "Berlin": "CLBB-IT | KIS Support",
            "Duisburg": "Orbis",
        },
        "requiredInformation": ["Username", "Hostname", "Error Message", "Screenshot"],
        "troubleshooting": [
            "Verify application availability",
            "Test login",
            "Verify Citrix session",
            "Verify user permissions",
        ],
        "note": "Kassel KIS Useranlagen route to the group ORBIS (see Kassel software matrix).",
    },
    {
        "id": "dragon_medical_one",
        "name": "Dragon Medical One",
        "aliases": ["DMO", "Nuance Dragon Medical One"],
        "criticality": "Medium",
        "defaultGroup": "INK DMO",
        "description": "Cloud-based medical speech recognition.",
        "keywords": ["DMO", "Dictation", "Speech Recognition", "Nuance"],
        "requiredInformation": ["Headset model", "Username", "Error message", "Hostname"],
        "troubleshooting": [
            "Verify microphone",
            "Verify DMO profile",
            "Restart DMO",
            "Verify audio device",
            "Test speech recognition",
        ],
    },
]

# Application cards generated from the site software matrices (groups from the matrix only).
for app_name, aliases, keywords, required, steps in [
    ("ApoFact", [], ["Apotheke", "Taxierung", "Abrechnung"],
     ["Username", "Hostname", "Error message"], []),
    ("Delegate", [], ["Essensbestellung", "Catering", "Stationsbestellung"],
     ["Username", "Ward / Station", "Error message"], []),
    ("Evident", [], ["Zahnarzt", "MKG", "Praxissoftware"],
     ["Username", "Hostname", "Error message"], []),
    ("iMedOne", ["i.MedOne", "IMedOne"], ["KIS", "iMedOne"],
     ["Username", "Hostname", "Error message", "Screenshot"], []),
    ("JiveX", [], ["PACS", "Bildmanagement", "Visus"],
     ["Username", "Hostname", "Study / Accession number", "Error message"], []),
    ("MetaVision", [], ["PDMS", "CIS", "Intensivmedizin", "iMDsoft"],
     ["Username", "Hostname", "Ward / ICU", "Error message"], []),
    ("3M QSMED", ["QSMED", "QS-MED"], ["Qualitätssicherung", "QS-Bögen"],
     ["Username", "Hostname", "Error message"], []),
    ("Telepaxx", [], ["Langzeitarchiv", "Bildarchiv"],
     ["Username", "Study / Accession number", "Error message"], []),
    ("ZENZY", [], ["Zytostatika", "Apotheke"],
     ["Username", "Hostname", "Error message"], []),
]:
    meta = app_meta(app_name)
    routing = app_routing(app_name)
    if not meta and not routing:
        continue
    applications.append({
        "id": app_name.lower().replace(" ", "_").replace("®", ""),
        "name": app_name,
        "aliases": aliases,
        "criticality": meta.get("criticality", ""),
        "description": meta.get("description", ""),
        "keywords": [app_name] + keywords,
        "routing": routing,
        "requiredInformation": required,
        "troubleshooting": steps,
        "note": "Assignment group depends on the site software matrix; TBD means the source left it blank.",
    })

locations = [
    location_card("Kassel", "Kassel", {
        "id": "kassel",
        "region": "West",
        "wave": 2,
        "defaultGroup": "KS-IT",
        "routing": {
            "Service Desk": "KS-IT",
            "Infrastructure": "KS-IT",
            "Clinical": "KS-IT",
            "SAP": "SAP Basis",
            "Field Service": "KS-IT",
        },
        "note": "Wave 2 go-live: general topics via Global Helios Groups, SAP via SAP Basis, "
                "Clinical stays on KS-IT. Legacy local SAP group in the matrix is KS-IT.",
    }),
    location_card("Duisburg", "Duisburg", {
        "id": "duisburg",
        "wave": 2,
        "defaultGroup": "DU-IT | Client Mgt",
        "routing": {
            "Service Desk": "DU-IT | Client Mgt",
            "Infrastructure": "DU-IT | Infrastruktur",
            "Clinical": "SKZ-IT | Klinische Anwendungen",
            "SAP": "SAP Basis",
            "Software": "DU-IT | Software & Systeme",
            "Orbis": "Orbis",
            "Muse": "AMOR/MUSE",
            "JiveX": "SKZ-IT | Klinische Anwendungen",
        },
    }),
    location_card("Berlin", "Berlin", {
        "id": "berlin",
        "cluster": "Berlin Brandenburg",
        "defaultGroup": "CLBB-IT | Servicedesk",
        "routing": {
            "Service Desk": "CLBB-IT | Servicedesk",
            "Infrastructure": "CLBB-IT | Infrastruktur",
            "Clinical": "CLBB-IT | Klinische Anwendungen",
            "KIS": "CLBB-IT | KIS Support",
            "Account Management": "CLBB-IT | Accountmanagement",
            "Field Service": "BLN-IT | Fieldservice",
        },
    }),
    location_card("Wuppertal", "CL-Wuppertal", {"id": "wuppertal", "cluster": "CL-Wuppertal"}),
    location_card("Northeim", "Northeim", {"id": "northeim"}),
    location_card("Erfurt", "Erfurt", {"id": "erfurt"}),
    location_card("Pirna", "Pirna", {"id": "pirna"}),
    location_card("Hildburghausen", "Hildburghausen", {"id": "hildburghausen"}),
    location_card("Krefeld", "Krefeld", {"id": "krefeld"}),
    location_card("Mansfeld-Südharz", "Mansfeld-Südharz", {"id": "mansfeld_suedharz"}),
    location_card("Attendorn", "Attendorn", {
        "id": "attendorn",
        "note": "Attendorn sits under CL-Wuppertal (Wave 1) and uses the CL-Wuppertal assignment groups.",
    }),
    location_card("Uelzen", "Uelzen", {"id": "uelzen"}),
]

clusters = [
    location_card("Cluster Berlin Brandenburg", "Berlin", {"id": "berlin_brandenburg"}),
    location_card("Cluster Wuppertal", "CL-Wuppertal", {"id": "wuppertal"}),
    location_card("Cluster Nordsee", "CL-Nordsee", {"id": "nordsee"}),
    location_card("Cluster Ostsee", "CL-Ostsee", {"id": "ostsee"}),
    location_card("Cluster Nordbaden", "CL-Nordbaden", {"id": "nordbaden"}),
    location_card("Region Süd", "Region Süd", {"id": "region_sued"}),
    location_card("Region Ost", "Region Ost", {"id": "region_ost"}),
    location_card("Cluster Sachsen", "Cluster Sachsen", {"id": "sachsen"}),
    location_card("Cluster Sachsen-Anhalt", "Cluster Sachsen-Anhalt", {"id": "sachsen_anhalt"}),
]

service_groups = [
    service_group_card(
        "CLBB-IT | Servicedesk",
        ["Password Reset", "MFA", "Outlook", "Teams", "Windows Login", "User Administration"],
        {
            "Infrastructure": "CLBB-IT | Infrastruktur",
            "Clinical": "CLBB-IT | Klinische Anwendungen",
            "SAP": "CLBB-IT | KIS Support",
        },
    ),
    service_group_card("CLBB-IT | Infrastruktur", [], {"Service Desk": "CLBB-IT | Servicedesk"}),
    service_group_card("KS-IT", [], {"SAP (Wave 2 go-live)": "SAP Basis"},
                       note="Kassel local IT: Service Desk, Infrastructure, Clinical and Field Service."),
    service_group_card("KR-IT | Service Desk", [], {}),
    service_group_card("MSH-IT | Servicedesk", [], {"Field Service": "MSH-IT | Fieldservice"},
                       note="Mansfeld-Südharz sites: Sangerhausen, Hettstedt, Eisleben."),
    service_group_card("RS | Servicedesk", [], {
        "Infrastructure": "RS | Infrastruktur",
        "Clinical": "RS | Klinische Prozesse & Anwendungen",
    }),
    service_group_card("SAP Basis", [], {},
                       note="SAP topics for Wave 1 and Wave 2 go-live locations."),
]

troubleshooting = [
    {
        "id": "vpn",
        "title": "VPN Troubleshooting",
        "collect": ["Username", "Hostname", "VPN Client", "Error Message"],
        "checks": ["Internet access", "MFA status", "VPN profile", "Certificate status", "User credentials"],
        "routing": {
            "Wave 1/2": "Ext_WW_Network_SLS_Capgemini_Helios",
            "Berlin": "CLBB-IT | Infrastruktur",
            "Kassel": "KS-IT",
        },
    },
    {
        "id": "active_directory",
        "title": "Active Directory / Password",
        "collect": ["Username", "Hostname", "Error Message", "Affected system"],
        "checks": ["Account locked or disabled", "Password expiry", "AD group membership", "Windows login on a second device"],
        "routing": {
            "Wave 1/2": "Ext_WW_AD_FLS_Capgemini_Helios",
            "Permissions / AD groups": "Ext_WW_AD_FLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "mfa",
        "title": "MFA / Account disabled",
        "collect": ["Username", "Registered device", "Error Message"],
        "checks": ["Account status", "Registered MFA method", "Device time / token sync"],
        "routing": {
            "Wave 1/2": "Ext_WW_OCC_SLS_Capgemini_Helios",
            "Berlin": "CLBB-IT | Servicedesk",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "outlook",
        "title": "Outlook / Exchange",
        "collect": ["Username", "Hostname", "Mailbox / Shared Mailbox", "Error Message"],
        "checks": ["Outlook profile", "Mailbox size / quota", "Shared mailbox permissions", "Webmail test"],
        "routing": {
            "Wave 1/2": "Ext_WW_Collaboration_SLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "teams",
        "title": "Microsoft Teams / SharePoint / OneDrive",
        "collect": ["Username", "Hostname", "Team / Site", "Error Message"],
        "checks": ["Teams client version", "Sign-in status", "Web client test", "Cache reset"],
        "routing": {
            "Wave 1/2": "Ext_WW_Collaboration_SLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "citrix",
        "title": "Citrix / Published Apps",
        "collect": ["Username", "Hostname", "Published app name", "Error Message"],
        "checks": ["Citrix Workspace version", "Session state / black screen", "Published app availability", "Login on a second device"],
        "routing": {
            "Wave 1/2": "Ext_WW_Virtual-Workplace_SLS_Capgemini_Helios",
            "Central SysOp": "SysOp | Citrix | Zentrale",
        },
    },
    {
        "id": "printer",
        "title": "Printer / FollowMe / Label printer",
        "collect": ["Printer name / queue", "Hostname", "Location / ward", "Error Message"],
        "checks": ["Printer online", "Print queue", "Driver / mapping", "Test page"],
        "routing": {
            "Wave 1/2": "Ext_WW_Printer-Services_SLS_Capgemini_Helios",
            "Hardware defect / onsite": "Ext_DE_FSO_Incidents_SLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "sap",
        "title": "SAP / KIS",
        "collect": ["SAP user", "System / client", "Transaction", "Error Message"],
        "checks": ["SAP GUI / Launchpad reachable", "User locked", "Role / authorisation", "Login on a second device"],
        "routing": {
            "Wave 1/2": "SAP Basis",
            "Berlin": "CLBB-IT | KIS Support",
            "Pre-wave": "Local IT / cluster SAP group",
        },
    },
    {
        "id": "workstation",
        "title": "Workstation / Hardware",
        "collect": ["Hostname", "Asset tag", "Location / room", "Error Message"],
        "checks": ["Power and cabling", "Cross-test with another device", "Disk space", "Windows updates"],
        "routing": {
            "Slow PC / disk full (Wave 1/2)": "Ext_WW_Physical-Workplace_SLS_Capgemini_Helios",
            "Hardware defect / onsite": "Ext_DE_FSO_Incidents_SLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
    },
    {
        "id": "dmo",
        "title": "Dragon Medical One (DMO)",
        "collect": ["Username", "Hostname", "Headset model", "Error Message"],
        "checks": ["Verify microphone", "Verify DMO profile", "Restart DMO", "Verify audio device", "Test speech recognition"],
        "routing": {"All locations": "INK DMO"},
    },
]

source = {
    "meta": {
        "title": "Helios Service Desk knowledge base",
        "source": "knowledge/ tree provided for Helios / Fresenius service desk agents",
        "updated": "2026-09-03",
        "priority": ["locations/", "applications/", "service_groups/", "routing/", "troubleshooting/"],
        "rules": [
            "Always search knowledge/ before answering.",
            "Never invent assignment groups — use only groups from the matrix / knowledge base.",
        ],
    },
    "prompt": prompt,
    "ticketTemplate": ticket_template,
    "routing": {
        "globalHeliosGroups": global_helios_groups,
        "assignmentRules": assignment_rules,
    },
    "applications": applications,
    "locations": locations,
    "clusters": clusters,
    "serviceGroups": service_groups,
    "troubleshooting": troubleshooting,
}

OUT.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("applications", len(applications))
print("locations", len(locations))
print("clusters", len(clusters))
print("serviceGroups", len(service_groups))
print("troubleshooting", len(troubleshooting))
