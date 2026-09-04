# Global IT Service Desk Knowledge Base

## Purpose

Assist Service Desk Agents, Major Incident Managers and IT Support Teams in resolving incidents, routing requests and following operational procedures.

## Incident Prioritization

### Priority 1 (Critical)

Conditions:

- Complete service outage
- Multiple users affected
- Business-critical service unavailable

Action:

- Immediate escalation
- Major Incident process

### Priority 2 (High)

Conditions:

- Important service degraded
- Workaround unavailable

Action:

- Immediate assignment to support team

### Priority 3 (Medium)

Conditions:

- Limited business impact
- Workaround available

Action:

- Standard support process

### Priority 4 (Low)

Conditions:

- Information request
- Cosmetic issue

Action:

- Schedule within SLA

## Troubleshooting Methodology

### Step 1 — Verify

- User identity
- Affected application
- Scope of impact

### Step 2 — Check

- Service health
- Monitoring alerts
- Existing incidents

### Step 3 — Validate

- Network connectivity
- User permissions
- Device status

### Step 4 — Review

- Recent changes
- Planned maintenance
- Known errors

### Step 5 — Escalate when

- Root cause unknown
- Administrative permissions required
- Infrastructure modification needed

## Escalation Rules

### Escalate to Local IT

- Hardware
- Printer problems
- Local network
- Workstations

### Escalate to Application Support

- Application errors
- Performance degradation
- Database access
- Configuration problems

### Escalate to Infrastructure Team

- Servers
- Active Directory
- Storage
- Virtualization

### Escalate to Security Team

- Malware
- Suspicious emails
- Unauthorized access
- Data leakage risk

## User Communication Standards

### Initial contact

- Confirmation of issue
- Incident number
- Expected next action

### Progress update

- Current status
- Work completed
- Next planned step

### Resolution message

- Root cause
- Resolution
- Confirmation request

## Priority Keywords (clinical)

Clinical keywords that drive the priority. A P1 is not declared when a workaround exists.

### P1 — Kritisch

- Risiko für die Patientensicherheit
- Lebensgefahr für Patienten
- Klinischer Schaden / Beeinträchtigung der Patientenversorgung
- Notaufnahme außer Betrieb
- Intensivstation außer Betrieb
- Operationssaal / OP-Bereich außer Betrieb
- Medikationssystem nicht verfügbar
- Elektronische Patientenakte (EHR) nicht verfügbar
- Krankenhausweiter Ausfall
- Mehrere Abteilungen betroffen
- Keine Umgehungslösung für kritische klinische Systeme/Anwendungen verfügbar
- Kritische klinische Abläufe werden unterbrochen
- Laborsystem außer Betrieb
- Radiologiesystem außer Betrieb
- Allgemeiner Netzwerkausfall
- Rechenzentrumsausfall
- Verletzung/Offenlegung geschützter Patienteninformationen (PHI)
- Rechtliches Haftungsrisiko
- Operationen abgesagt
- Alle Benutzer betroffen

### P2 — Hoch

- Erhebliche Beeinträchtigung klinischer Abläufe
- Ausfall einer Abteilung (abhängig von den Auswirkungen auf Finanzen, klinische Prozesse, Personalwesen oder Management)
- Abteilungsweite Auswirkungen
- Apotheke betroffen
- Radiologie betroffen
- Elektronische Patientenakte (EHR) arbeitet langsam
- Wichtige Anwendung teilweise nicht verfügbar
- PACS (Bildarchivierungs- und Kommunikationssystem) beeinträchtigt
- Verzögerungen bei der Medikamentenausgabe
- Verzögerungen in der Patientenversorgung
- Erhebliche Anzahl von Benutzern betroffen

## Outage Priorities

### High (1)

- All users in a corporate unit or region are impacted
- Legal or major financial impact
- Defined company critical service is impacted
- Productivity is totally blocked; no workaround exists

### Medium (2)

- Multiple users in a corporate unit or region are impacted
- Business-critical services significantly impacted but not yet a Major Incident
- Productivity is partially blocked; significant service disruption

Priority = Impact × Urgency (High 1 / Medium 2 / Low 3).

| Impact \ Urgency | High (1) | Medium (2) | Low (3) |
|---|---|---|---|
| High (1) | 1 | 2 | 3 |
| Medium (2) | 2 | 3 | 4 |
| Low (3) | 3 | 4 | 5 |

Priority 5 – Only Planning, e.g. for development / test systems affected.

Open an outage when:

- Whole or an important part of a service is not available and business-critical processes cannot be used.
- Loss of the facility or essential supporting infrastructure (power grids, telephone switching centers, microwave towers).
- Business relations between the Business Partners and their customers are likely to be disrupted.
- Not Severity Level 1 yet, but could become one if not resolved quickly.
- Affects a large group of end users or a critical process is not functioning.

## Major Incident Process

Identification:

- Large user impact
- Multiple locations affected
- Critical business services unavailable

Actions:

1. Create Major Incident
2. Notify stakeholders
3. Engage support teams
4. Start bridge call
5. Provide regular updates
6. Document timeline
7. Complete post-incident review

## Active Directory Procedures

### Password Reset

Verify:

- Full name
- Employee ID
- Manager verification if necessary

### Account Unlock

Verify:

- Reason for lockout
- Recent password changes
- Failed login attempts

## Remote Support Checklist

Before connecting:

- User approval received
- Device confirmed
- Session logging enabled

Verify:

- Network
- Applications
- Security alerts

Document:

- Actions performed
- Results
- Follow-up requirements

## Routing Matrix Structure

- **Location** — Site name
- **Assignment Group** — Responsible support team
- **Service Scope** — Supported services
- **Escalation Path** — Primary and secondary support groups
- **Notes** — Special handling instructions

## Best Practices

- Always collect complete diagnostic information.
- Avoid unnecessary reassignments.
- Document every troubleshooting step.
- Verify resolution with the user.
- Use knowledge articles whenever available.
- Follow SLA requirements.
- Escalate with complete documentation.
