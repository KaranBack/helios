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
    {"field": "User details", "detail": "Full Name, User ID, Department"},
    {"field": "Phone number", "detail": "Contact number"},
    {"field": "Location", "detail": "Site, Building, Country"},
    {"field": "Issue description", "detail": "Detailed description of the issue"},
    {"field": "Start date of the issue", "detail": "When did the issue begin?"},
    {"field": "Error message", "detail": "Exact error message if available"},
    {"field": "Observation during initial investigation", "detail": "", "default": "N/A"},
    {"field": "Troubleshooting steps taken", "detail": "List all actions already performed"},
    {"field": "Hostname", "detail": "", "default": "Internal"},
    {"field": "Windows version", "detail": "", "default": "Windows 11 24H2"},
    {"field": "Availability", "detail": "State user availability for further troubleshooting"},
]

service_desk_kb = {
    "purpose": "Assist Service Desk Agents, Major Incident Managers and IT Support Teams in resolving "
               "incidents, routing requests and following operational procedures.",
    "prioritization": [
        {"level": "Priority 1", "name": "Critical",
         "conditions": ["Complete service outage", "Multiple users affected", "Business-critical service unavailable"],
         "action": ["Immediate escalation", "Major Incident process"]},
        {"level": "Priority 2", "name": "High",
         "conditions": ["Important service degraded", "Workaround unavailable"],
         "action": ["Immediate assignment to support team"]},
        {"level": "Priority 3", "name": "Medium",
         "conditions": ["Limited business impact", "Workaround available"],
         "action": ["Standard support process"]},
        {"level": "Priority 4", "name": "Low",
         "conditions": ["Information request", "Cosmetic issue"],
         "action": ["Schedule within SLA"]},
    ],
    "methodology": [
        {"step": "Step 1", "title": "Verify", "items": ["User identity", "Affected application", "Scope of impact"]},
        {"step": "Step 2", "title": "Check", "items": ["Service health", "Monitoring alerts", "Existing incidents"]},
        {"step": "Step 3", "title": "Validate", "items": ["Network connectivity", "User permissions", "Device status"]},
        {"step": "Step 4", "title": "Review", "items": ["Recent changes", "Planned maintenance", "Known errors"]},
        {"step": "Step 5", "title": "Escalate when",
         "items": ["Root cause unknown", "Administrative permissions required", "Infrastructure modification needed"]},
    ],
    "escalationRules": [
        {"target": "Local IT", "issues": ["Hardware", "Printer problems", "Local network", "Workstations"]},
        {"target": "Application Support",
         "issues": ["Application errors", "Performance degradation", "Database access", "Configuration problems"]},
        {"target": "Infrastructure Team", "issues": ["Servers", "Active Directory", "Storage", "Virtualization"]},
        {"target": "Security Team",
         "issues": ["Malware", "Suspicious emails", "Unauthorized access", "Data leakage risk"]},
    ],
    "communication": [
        {"stage": "Initial contact", "items": ["Confirmation of issue", "Incident number", "Expected next action"]},
        {"stage": "Progress update", "items": ["Current status", "Work completed", "Next planned step"]},
        {"stage": "Resolution message", "items": ["Root cause", "Resolution", "Confirmation request"]},
    ],
    "majorIncident": {
        "identification": ["Large user impact", "Multiple locations affected", "Critical business services unavailable"],
        "actions": ["Create Major Incident", "Notify stakeholders", "Engage support teams", "Start bridge call",
                    "Provide regular updates", "Document timeline", "Complete post-incident review"],
    },
    "priorityKeywords": {
        "source": "Keywords zur Einstufung der Incident-Priorität für Service-Desk-Agents",
        "note": "Clinical keywords that drive the priority. A P1 is not declared when a workaround exists.",
        "levels": [
            {"level": "P1", "name": "Kritisch", "keywords": [
                "Risiko für die Patientensicherheit",
                "Lebensgefahr für Patienten",
                "Klinischer Schaden / Beeinträchtigung der Patientenversorgung",
                "Notaufnahme außer Betrieb",
                "Intensivstation außer Betrieb",
                "Operationssaal / OP-Bereich außer Betrieb",
                "Medikationssystem nicht verfügbar",
                "Elektronische Patientenakte (EHR) nicht verfügbar",
                "Krankenhausweiter Ausfall",
                "Mehrere Abteilungen betroffen",
                "Keine Umgehungslösung für kritische klinische Systeme/Anwendungen verfügbar",
                "Kritische klinische Abläufe werden unterbrochen",
                "Laborsystem außer Betrieb",
                "Radiologiesystem außer Betrieb",
                "Allgemeiner Netzwerkausfall",
                "Rechenzentrumsausfall",
                "Verletzung/Offenlegung geschützter Patienteninformationen (PHI)",
                "Rechtliches Haftungsrisiko",
                "Operationen abgesagt",
                "Alle Benutzer betroffen",
            ]},
            {"level": "P2", "name": "Hoch", "keywords": [
                "Erhebliche Beeinträchtigung klinischer Abläufe",
                "Ausfall einer Abteilung (abhängig von den Auswirkungen auf Finanzen, klinische Prozesse, "
                "Personalwesen oder Management)",
                "Abteilungsweite Auswirkungen",
                "Apotheke betroffen",
                "Radiologie betroffen",
                "Elektronische Patientenakte (EHR) arbeitet langsam",
                "Wichtige Anwendung teilweise nicht verfügbar",
                "PACS (Bildarchivierungs- und Kommunikationssystem) beeinträchtigt",
                "Verzögerungen bei der Medikamentenausgabe",
                "Verzögerungen in der Patientenversorgung",
                "Erhebliche Anzahl von Benutzern betroffen",
            ]},
        ],
    },
    "outagePriorities": {
        "source": "FDT GSD. Major Incident - Major Incident Handling (KB0016201)",
        "levels": [
            {"level": "High (1)",
             "conditions": ["All users in a corporate unit or region are impacted",
                            "Legal or major financial impact",
                            "Defined company critical service is impacted",
                            "Productivity is totally blocked; no workaround exists"]},
            {"level": "Medium (2)",
             "conditions": ["Multiple users in a corporate unit or region are impacted",
                            "Business-critical services significantly impacted but not yet a Major Incident",
                            "Productivity is partially blocked; significant service disruption"]},
        ],
        "matrix": {
            "note": "Priority = Impact × Urgency (High 1 / Medium 2 / Low 3).",
            "rows": [
                {"impact": "High (1)", "High (1)": "1", "Medium (2)": "2", "Low (3)": "3"},
                {"impact": "Medium (2)", "High (1)": "2", "Medium (2)": "3", "Low (3)": "4"},
                {"impact": "Low (3)", "High (1)": "3", "Medium (2)": "4", "Low (3)": "5"},
            ],
        },
        "planningOnly": "Priority 5 – Only Planning, e.g. for development / test systems affected.",
        "outageCriteria": [
            "Whole or an important part of a service is not available and business-critical processes cannot be used.",
            "Loss of the facility or essential supporting infrastructure (power grids, telephone switching centers, microwave towers).",
            "Business relations between the Business Partners and their customers are likely to be disrupted.",
            "Not Severity Level 1 yet, but could become one if not resolved quickly.",
            "Affects a large group of end users or a critical process is not functioning.",
        ],
    },
    "majorIncidentProcess": {
        "source": "FDT GSD. Major Incident - Major Incident Handling (KB0016201 v14.0)",
        "effective": "07 July 2025",
        "importantNotice": [
            "Manual priority setting to P1 is no longer allowed — backend users cannot set Priority to P1.",
            "P1 equals a Major Incident and must be initiated with the “Propose Major Incident” action in ServiceNow.",
            "FME-raised incidents impacting FDT systems follow the FDT follow-up-incident process; "
            "eBonded tickets cannot be proposed directly as Major Incidents.",
        ],
        "steps": [
            "Identify a potential Major Incident based on impact and urgency.",
            "Create the incident and apply the Major Incident template.",
            "Use the “Propose Major Incident” action in ServiceNow.",
            "Fill in Work Notes (contact details, availability, symptoms) and Business Impact "
            "(application affected, number of users, financial impact).",
            "Call the MIM team at +91 2267 802 355 or contact them via FreDi Chat — mandatory even after proposing.",
            "Send the MI email to the MIM distribution lists with ticket and user details.",
            "Add a Work Note: “MIM informed”.",
            "Follow the guidance of the Major Incident Manager on priority, assignment and next steps.",
        ],
        "proposalFields": {
            "workNotes": ["Contact person (full name)", "Contact for additional questions", "Phone number",
                          "Customer's language", "Secondary contact person",
                          "Availability / remaining working time of affected team", "Error message / symptoms"],
            "businessImpact": ["Application not working", "When was it working fine / since when (CET)",
                               "Locations impacted", "Number of users impacted", "Any workaround available",
                               "Immediate business / financial impact"],
        },
        "businessImpactQuestions": [
            "Which application is not working as expected? (during network/VPN outage document all inaccessible applications)",
            "What is the error message or symptoms?",
            "When was it working fine / since when did the issue start (CET)?",
            "Number of users impacted?",
            "Any workaround available? (no P1 is declared when a workaround exists)",
            "Who is the contact for clarifying additional questions, and are they available?",
            "What is the immediate business / financial impact?",
            "What is the remaining working time of the affected team? (bridge call starts asap)",
        ],
        "afterPromotion": [
            "The Major Incident Manager owns the incident until resolution.",
            "The incident is tracked under the Major Incident tab (business impact, segments, timestamps).",
            "Once promoted, the incident must not be downgraded.",
            "Related user tickets are attached to the parent ticket as child tickets.",
            "An IVR message may be set up on instruction of the Incident / Team Manager.",
        ],
        "childTicket": [
            "Create a new incident and apply the Outage Related template.",
            "Assign it to the same team as the parent incident.",
            "Short description starts with OUTAGE RELATED.",
            "Fill the Parent Incident field with the outage number in Related Records.",
            "Set the ticket to the lowest possible priority (P4).",
        ],
        "escalatedP2": [
            "Propose the incident as a Major Incident using the same process.",
            "The MIM team opens a taskforce call and performs the MI assessment.",
            "If rejected, the call stays open for tracking.",
            "Add the Work Note: “This is an escalated P2.”",
            "Tag the incident in ServiceNow with the label “escalated”.",
        ],
        "fmeEbonding": [
            "FME GSD contacts FDT GSD by phone and provides the FME incident number (visible under Related Records).",
            "eBonded incidents cannot be proposed as a Major Incident in FDT ServiceNow.",
            "FDT GSD creates a follow-up incident from the eBonded ticket and proposes that one as MI.",
            "The eBonded incident is added as a child incident of the new FDT incident.",
        ],
        "ivr": [
            "Emergency IVR messages inform end users before they reach the Service Desk.",
            "Typical cases: network down for an entire site, widespread application outages, major infrastructure failures.",
            "Not every outage requires an IVR — always consult the Incident Manager or Team Manager.",
            "See KB0016190 — Service Desk IVR Recording and Activation.",
        ],
        "contacts": [
            {"role": "MIM hotline (24/7)", "detail": "+91 2267 802 355"},
            {"role": "MIM distribution list", "detail": "dachmim.in@capgemini.com"},
            {"role": "MIM generic mailbox", "detail": "dachmajorincidentmanagement.in@capgemini.com"},
            {"role": "Smart Hands Friedberg (HCL, 24/7)",
             "detail": "+49 731 96584000 — assignment group Ext_WW_GNS_NOC_HCL"},
            {"role": "Email subject format", "detail": "Client Name (FDT/FMC/FME) // INC***** – short description // P2"},
        ],
        "escalationLevels": [
            {"level": "1st level", "name": "Nabil Nasir Shaikh",
             "mail": "nabil.nasir-shaikh@capgemini.com", "phone": "+91 7304615600"},
            {"level": "2nd level", "name": "Siddhartha Guha",
             "mail": "siddhartha.guha@capgemini.com", "phone": "+91 9008864844"},
            {"level": "3rd level", "name": "Rajagopalan Jagannathan",
             "mail": "rajagopalan.jaganathan@capgemini.com", "phone": "+49 15140251861"},
            {"level": "4th level", "name": "Tim Freistühler",
             "mail": "tim.freistuehler@capgemini.com", "phone": "+49 15118898146"},
        ],
        "ticketEscalation": [
            "Only phone or FreDi live chat can be used to escalate a ticket — not email or the Report an Issue form.",
            "Have the incident (INC…) or request (REQ…) number ready.",
            "Any FDT ticket can be escalated via the FDT Global IT Service Desk.",
        ],
    },
    "adProcedures": [
        {"topic": "Password Reset", "verify": ["Full name", "Employee ID", "Manager verification if necessary"]},
        {"topic": "Account Unlock", "verify": ["Reason for lockout", "Recent password changes", "Failed login attempts"]},
    ],
    "remoteSupport": {
        "before": ["User approval received", "Device confirmed", "Session logging enabled"],
        "verify": ["Network", "Applications", "Security alerts"],
        "document": ["Actions performed", "Results", "Follow-up requirements"],
    },
    "bestPractices": [
        "Always collect complete diagnostic information.",
        "Avoid unnecessary reassignments.",
        "Document every troubleshooting step.",
        "Verify resolution with the user.",
        "Use knowledge articles whenever available.",
        "Follow SLA requirements.",
        "Escalate with complete documentation.",
    ],
    "routingMatrixStructure": [
        {"field": "Location", "detail": "Site name"},
        {"field": "Assignment Group", "detail": "Responsible support team"},
        {"field": "Service Scope", "detail": "Supported services"},
        {"field": "Escalation Path", "detail": "Primary and secondary support groups"},
        {"field": "Notes", "detail": "Special handling instructions"},
    ],
}

templates = [
    {"id": "incident", "title": "Incident",
     "sections": [
         {"heading": "Mandatory information", "items": [t["field"] + (f" — {t['detail']}" if t.get("detail") else "")
                                                        + (f" (default: {t['default']})" if t.get("default") else "")
                                                        for t in ticket_template]},
         {"heading": "Priority", "items": [f"{p['level']} ({p['name']}): " + "; ".join(p["conditions"])
                                           for p in service_desk_kb["prioritization"]]},
         {"heading": "Assignment", "body": "Determine location, cluster, wave and application first, then apply "
                                           "the routing rules (Global Helios → local cluster → local site)."},
     ]},
    {"id": "request", "title": "Service Request",
     "sections": [
         {"heading": "Mandatory information",
          "items": ["User details (Full Name, User ID, Department)", "Phone number", "Location (Site, Building, Country)",
                    "Requested service or item", "Business justification", "Required by date", "Manager approval"]},
         {"heading": "Assignment", "body": "Route to the group that owns the requested service. "
                                           "Account and access requests follow the Active Directory procedures."},
     ]},
    {"id": "escalation", "title": "Escalation",
     "sections": [
         {"heading": "Before escalating",
          "items": ["Complete diagnostic information collected", "All troubleshooting steps documented",
                    "Priority and business impact confirmed", "Correct assignment group identified"]},
         {"heading": "Escalation targets",
          "items": [f"{r['target']}: " + ", ".join(r["issues"]) for r in service_desk_kb["escalationRules"]]},
         {"heading": "Content",
          "items": ["Incident number", "Summary and business impact", "Affected users and locations",
                    "Steps already taken and results", "Requested action from the receiving team"]},
     ]},
    {"id": "major_incident", "title": "Major Incident",
     "sections": [
         {"heading": "Ask the user (requester details)",
          "items": ["Contact person for additional questions:", "Phone number:", "Customer's language:",
                    "Secondary contact person:", "Phone number:", "Availability of the affected team:",
                    "Error message / symptoms:"]},
         {"heading": "Business impact (Propose Major Incident pop-up)",
          "items": service_desk_kb["majorIncidentProcess"]["proposalFields"]["businessImpact"]},
         {"heading": "Business impact questions",
          "items": service_desk_kb["majorIncidentProcess"]["businessImpactQuestions"]},
         {"heading": "How to propose",
          "items": service_desk_kb["majorIncidentProcess"]["steps"]},
         {"heading": "Contacts",
          "items": [c["role"] + ": " + c["detail"]
                    for c in service_desk_kb["majorIncidentProcess"]["contacts"]]},
     ]},
    {"id": "known_error", "title": "Known Error",
     "sections": [
         {"heading": "Fields", "items": ["Title — concise error title", "Symptoms — observable symptoms",
                                         "Root Cause — confirmed cause", "Resolution — permanent fix",
                                         "Workaround — if available", "Related Systems — affected systems"]},
     ]},
    {"id": "knowledge_article", "title": "Knowledge Article",
     "sections": [
         {"heading": "Fields", "items": ["Summary — short description", "Symptoms — observed behavior",
                                         "Cause — known root cause", "Solution — step-by-step resolution",
                                         "Validation — how to confirm the issue is resolved",
                                         "Related Articles — links to relevant KBs"]},
     ]},
]

prompts = [
    {"id": "service_desk_agent", "title": "Service Desk Agent",
     "purpose": "Route and document incidents for Helios / Fresenius locations.",
     "instructions": [
         "Determine location, cluster, region, application, wave status and assignment group.",
         "Apply routing priority: Global Helios Group → Local Cluster Group → Local Site Group.",
         "Wave 1 / Wave 2 SAP topics go to SAP Basis; Clinical Applications always stay on local IT.",
         "Collect the mandatory ticket template fields before assigning.",
         "Never invent assignment groups — use only groups from the knowledge base.",
     ],
     "output": ["Location", "Cluster", "Wave", "Assignment Group", "Reason",
                "Required Information", "Initial Troubleshooting", "Next Action"]},
    {"id": "major_incident_manager", "title": "Major Incident Manager",
     "purpose": "Drive major incidents from identification to post-incident review.",
     "instructions": [
         "Confirm major incident criteria: large user impact, multiple locations, critical service unavailable.",
         "Create the Major Incident and notify stakeholders.",
         "Engage the support teams that own the affected services and start the bridge call.",
         "Provide regular updates and document the timeline.",
         "Complete the post-incident review and record the known error.",
     ],
     "output": ["Incident number", "Impact and scope", "Engaged teams", "Current status",
                "Next update time", "Timeline", "Post-incident actions"]},
    {"id": "translator", "title": "Translator",
     "purpose": "Translate ticket content between German and English without changing technical meaning.",
     "instructions": [
         "Keep assignment group names, hostnames, application names and error messages unchanged.",
         "Translate the description, observations and troubleshooting steps only.",
         "Preserve the ticket template structure and field order.",
         "Mark uncertain medical or product terms instead of guessing.",
     ],
     "output": ["Original language", "Translated text", "Terms left untranslated"]},
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

def routing_matrix_card(location, key, service_scope, escalation, notes=""):
    c = CLUSTERS.get(key) or {}
    return {
        "id": location.lower().replace(" ", "_"),
        "location": location,
        "assignmentGroup": c.get("ServiceDesk", ""),
        "wave": wave_of(key),
        "serviceScope": service_scope,
        "escalationPath": escalation,
        "notes": notes,
    }


routing_matrix = [
    routing_matrix_card(
        "Berlin", "Berlin",
        ["Service Desk", "Account Management", "Infrastructure", "Clinical Applications", "KIS", "Field Service"],
        {"Primary": "CLBB-IT | Servicedesk",
         "Infrastructure": "CLBB-IT | Infrastruktur",
         "Clinical": "CLBB-IT | Klinische Anwendungen",
         "KIS / SAP": "CLBB-IT | KIS Support",
         "Field Service": "BLN-IT | Fieldservice"},
        "Cluster Berlin Brandenburg. Field service is site-specific (BLN-IT, BEB-IT, BS-IT)."),
    routing_matrix_card(
        "Duisburg", "Duisburg",
        ["Service Desk", "Infrastructure", "Software", "Clinical Applications", "Orbis", "Muse", "JiveX"],
        {"Primary": "DU-IT | Client Mgt",
         "Infrastructure": "DU-IT | Infrastruktur",
         "Software": "DU-IT | Software & Systeme",
         "Clinical / JiveX": "SKZ-IT | Klinische Anwendungen",
         "Orbis": "Orbis",
         "Muse": "AMOR/MUSE",
         "SAP": "SAP Basis"},
        "Wave 2 go-live: general topics use Global Helios Groups, SAP uses SAP Basis, Clinical stays local."),
    routing_matrix_card(
        "Krefeld", "Krefeld",
        ["Service Desk", "Infrastructure", "Clinical Applications", "Medico / SAP", "Field Service"],
        {"Primary": "KR-IT | Service Desk",
         "Infrastructure": "KR-IT | Infrastruktur",
         "Clinical": "KR-IT | Klinische Applikationen",
         "Medico / KIS": "KR-IT | Medico",
         "Field Service": "KR-IT | Fieldservice"},
        "Wave 2 go-live. Hüls inherits Krefeld routing."),
    {
        "id": "helios_global",
        "location": "Helios Global (Wave go-live)",
        "assignmentGroup": "Global Helios Groups",
        "wave": "1 / 2",
        "serviceScope": [g["service"] for g in global_helios_groups],
        "escalationPath": {g["service"]: g["group"] for g in global_helios_groups},
        "notes": "Used for every Wave 1 / Wave 2 location. SAP → SAP Basis. "
                 "Clinical Applications always stay on the local IT group.",
    },
]

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

fhs = {
    "title": "FHS — Fresenius Health Services",
    "notice": {
        "title": "FHS Citrix — where to send the ticket",
        "text": "If Helios users encounter issues with or request access to FHS Citrix, they must submit a ticket "
                "by contacting it-services@vamed.com.",
        "contact": "it-services@vamed.com",
    },
    "coexistence": {
        "title": "Coexisting phase — which account to use",
        "note": "During the coexistence phase two environments run in parallel. Use the account listed per app.",
        "rows": [
            {"app": "Laptop login", "account": "Fresenius",
             "description": "After the migration, log in to your laptop using your Fresenius account credentials.",
             "comment": "Your laptop is now managed by Fresenius."},
            {"app": "VPN", "account": "Fresenius Health Services",
             "description": "To establish a VPN connection use your FHS VPN client.",
             "comment": "Temporary solution. You will be informed prior to the planned change."},
            {"app": "Outlook (desktop)", "account": "Fresenius",
             "description": "Use the Outlook desktop app for all your emails. This is the consolidated view "
                            "(Fresenius + FHS). Do not use Citrix Outlook.",
             "comment": "All inbound emails appear in your Fresenius mailbox. Outbound emails come from "
                        "@fresenius.com with a banner explaining the change to external recipients."},
            {"app": "Outlook Web App", "account": "Fresenius Health Services",
             "description": "Use the Outlook Web App only to access shared mailboxes.",
             "comment": "Access via a web browser, logged in with the FHS profile."},
            {"app": "Teams", "account": "Fresenius",
             "description": "Switch to your Fresenius account if required.",
             "comment": "Your primary account is the Teams app."},
            {"app": "Teams (FHS account)", "account": "Fresenius Health Services",
             "description": "You can continue your work on your FHS account profile as usual.",
             "comment": "Your additional account in Teams. This account must be manually added to your Teams app "
                        "after the migration."},
            {"app": "SharePoint", "account": "Fresenius",
             "description": "Fresenius SharePoint websites.",
             "comment": "Access via a web browser using the Fresenius profile."},
            {"app": "SharePoint (FHS)", "account": "Fresenius Health Services",
             "description": "FHS SharePoint websites.",
             "comment": "Access via a web browser, logged in with the FHS profile."},
            {"app": "OneDrive", "account": "Fresenius",
             "description": "Use the Fresenius OneDrive desktop app for all files. The FHS content has been copied. "
                            "When collaborating you must share the new file link, as colleagues may still be working "
                            "on the FHS file.",
             "comment": "Access via a web browser, logged in with the FHS profile."},
            {"app": "OneDrive (FHS)", "account": "Fresenius Health Services",
             "description": "Use only if you believe files have not been transferred.",
             "comment": "Access via a web browser, logged in with the FHS profile."},
            {"app": "Citrix (FHS)", "account": "Fresenius Health Services",
             "description": "Use a web browser to access the FHS Citrix apps. Do not use the Outlook app in Citrix.",
             "comment": "Access via a web browser, logged in with the FHS profile. "
                        "Issues / access requests → it-services@vamed.com."},
        ],
    },
    "support": {
        "title": "Do you need support? Fresenius Global Service Desk",
        "channels": [
            {"channel": "FreDi live chat", "detail": "In Teams"},
            {"channel": "Portal", "detail": "Open a ticket — https://fnc.service-now.com/sp"},
            {"channel": "Phone", "detail": "+49 (0)6172 608-1111"},
            {"channel": "Email", "detail": "GlobalServiceDesk@fresenius.com"},
            {"channel": "FHS Citrix", "detail": "it-services@vamed.com"},
        ],
        "links": [
            "myIT Information portal — myIT Community",
            "myIT Link Cheat Page — all the key Fresenius links",
            "Intranet home page — Fresenius One Site for all your news",
        ],
    },
}

troubleshooting = [
    {
        "id": "shared_mailbox",
        "title": "Shared mailbox in Outlook Online (coexistence phase)",
        "collect": ["Username", "Shared mailbox name or address", "Browser used", "Error message"],
        "checks": [
            "Open Edge logged in with the non-Fresenius (FHS) account.",
            "Go to https://outlook.office.com (Outlook Online).",
            "Click the profile icon (top right) and select “Open another mailbox”.",
            "Enter the shared mailbox name or email, select it from the list and click “Open”.",
            "The mailbox opens in a new browser tab — add it to favourites with the star icon.",
        ],
        "routing": {
            "Coexistence phase": "Shared mailboxes must be used via Outlook Online, not the Outlook desktop app",
            "Wave 1/2": "Ext_WW_Collaboration_SLS_Capgemini_Helios",
            "Pre-wave": "Local IT group of the location",
        },
        "note": "Using Outlook Online avoids the shared mailbox missing in Outlook desktop, missing folders/emails "
                "and not being able to send from the shared mailbox. Source: Using a Shared Mailbox in Outlook "
                "Online — user guide.",
    },
    {
        "id": "printer_mapping",
        "title": "Post-migration printer mapping",
        "collect": ["New printer name from the printer label (HOST NAME / GLOBAL PRINTER NAME)", "Hostname",
                    "Location / room", "Error message"],
        "checks": [
            "Confirm the user is connected to the Fresenius corporate network.",
            "Find the new printer name on the printer label (e.g. DEANS1RNF).",
            "Press Windows + R and open \\\\PFDTFHSAP1001.ads.fresenius.com.",
            "Locate the printer in the list and double-click it — Windows installs the printer and drivers.",
            "Verify under Printers & scanners that the printer is listed.",
            "Print a test page: Printers & scanners → printer → Printer properties → Print Test Page.",
            "Optional: set as default via Settings → Bluetooth & devices → Printers & scanners → "
            "More devices and printers settings → right-click → Set as default printer.",
        ],
        "routing": {
            "Fresenius Service Desk": "+49 (0)6172 608-1111 · GlobalServiceDesk@fresenius.com · "
                                      "https://fnc.service-now.com/sp",
            "Wave 1/2": "Ext_WW_Printer-Services_SLS_Capgemini_Helios",
            "Hardware defect / onsite": "Ext_DE_FSO_Incidents_SLS_Capgemini_Helios",
        },
        "note": "Printer names changed during the migration. Source: Post migration printer mapping — user guide.",
    },
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
    "serviceDeskKb": service_desk_kb,
    "fhs": fhs,
    "templates": templates,
    "prompts": prompts,
    "routingMatrix": routing_matrix,
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
