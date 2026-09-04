# Major Incident Handling (FDT)

Source:
FDT GSD. Major Incident - Major Incident Handling (KB0016201 v14.0)

Effective:
07 July 2025

## Important notice

- Manual priority setting to P1 is no longer allowed — backend users cannot set Priority to P1.
- P1 equals a Major Incident and must be initiated with the “Propose Major Incident” action in ServiceNow.
- FME-raised incidents impacting FDT systems follow the FDT follow-up-incident process; eBonded tickets cannot be proposed directly as Major Incidents.

## Propose Major Incident — step by step

1. Identify a potential Major Incident based on impact and urgency.
2. Create the incident and apply the Major Incident template.
3. Use the “Propose Major Incident” action in ServiceNow.
4. Fill in Work Notes (contact details, availability, symptoms) and Business Impact (application affected, number of users, financial impact).
5. Call the MIM team at +91 2267 802 355 or contact them via FreDi Chat — mandatory even after proposing.
6. Send the MI email to the MIM distribution lists with ticket and user details.
7. Add a Work Note: “MIM informed”.
8. Follow the guidance of the Major Incident Manager on priority, assignment and next steps.

## Proposal pop-up fields

Work Notes:

- Contact person (full name)
- Contact for additional questions
- Phone number
- Customer's language
- Secondary contact person
- Availability / remaining working time of affected team
- Error message / symptoms

Business Impact:

- Application not working
- When was it working fine / since when (CET)
- Locations impacted
- Number of users impacted
- Any workaround available
- Immediate business / financial impact

## Business impact questions (collect before proposing)

1. Which application is not working as expected? (during network/VPN outage document all inaccessible applications)
2. What is the error message or symptoms?
3. When was it working fine / since when did the issue start (CET)?
4. Number of users impacted?
5. Any workaround available? (no P1 is declared when a workaround exists)
6. Who is the contact for clarifying additional questions, and are they available?
7. What is the immediate business / financial impact?
8. What is the remaining working time of the affected team? (bridge call starts asap)

## After promotion

- The Major Incident Manager owns the incident until resolution.
- The incident is tracked under the Major Incident tab (business impact, segments, timestamps).
- Once promoted, the incident must not be downgraded.
- Related user tickets are attached to the parent ticket as child tickets.
- An IVR message may be set up on instruction of the Incident / Team Manager.

## Outage related / child ticket

- Create a new incident and apply the Outage Related template.
- Assign it to the same team as the parent incident.
- Short description starts with OUTAGE RELATED.
- Fill the Parent Incident field with the outage number in Related Records.
- Set the ticket to the lowest possible priority (P4).

## Escalated P2

- Propose the incident as a Major Incident using the same process.
- The MIM team opens a taskforce call and performs the MI assessment.
- If rejected, the call stays open for tracking.
- Add the Work Note: “This is an escalated P2.”
- Tag the incident in ServiceNow with the label “escalated”.

## FME tickets affecting FDT systems (eBonding)

- FME GSD contacts FDT GSD by phone and provides the FME incident number (visible under Related Records).
- eBonded incidents cannot be proposed as a Major Incident in FDT ServiceNow.
- FDT GSD creates a follow-up incident from the eBonded ticket and proposes that one as MI.
- The eBonded incident is added as a child incident of the new FDT incident.

## IVR

- Emergency IVR messages inform end users before they reach the Service Desk.
- Typical cases: network down for an entire site, widespread application outages, major infrastructure failures.
- Not every outage requires an IVR — always consult the Incident Manager or Team Manager.
- See KB0016190 — Service Desk IVR Recording and Activation.

## Ticket escalation

- Only phone or FreDi live chat can be used to escalate a ticket — not email or the Report an Issue form.
- Have the incident (INC…) or request (REQ…) number ready.
- Any FDT ticket can be escalated via the FDT Global IT Service Desk.

## Contacts

| Role | Details |
|---|---|
| MIM hotline (24/7) | +91 2267 802 355 |
| MIM distribution list | dachmim.in@capgemini.com |
| MIM generic mailbox | dachmajorincidentmanagement.in@capgemini.com |
| Smart Hands Friedberg (HCL, 24/7) | +49 731 96584000 — assignment group Ext_WW_GNS_NOC_HCL |
| Email subject format | Client Name (FDT/FMC/FME) // INC***** – short description // P2 |

## Escalation matrix (MIM hotline unreachable)

| Level | Name | Mail | Phone |
|---|---|---|---|
| 1st level | Nabil Nasir Shaikh | nabil.nasir-shaikh@capgemini.com | +91 7304615600 |
| 2nd level | Siddhartha Guha | siddhartha.guha@capgemini.com | +91 9008864844 |
| 3rd level | Rajagopalan Jagannathan | rajagopalan.jaganathan@capgemini.com | +49 15140251861 |
| 4th level | Tim Freistühler | tim.freistuehler@capgemini.com | +49 15118898146 |
