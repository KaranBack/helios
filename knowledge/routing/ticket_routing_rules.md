# Ticket routing rules — FHS · FDT · FSE · KABI · HELIOS

Source:
Zasady routingu ticketów (FHS/FDT/FSE/KABI/HELIOS) + Helios Support handling instruction

## Step 1 — read the ticket

**Do not route by the sender domain alone. Always establish: which account does the problem concern?**

Analyse:

- Description of the request
- Account named by the user
- Email address mentioned inside the request
- Error messages
- System or service the problem concerns

## Decision tree

### 1. Does the problem concern an FHS / FDT / FSE / KABI / Fresenius account?

Examples:

- @fresenius.com account
- FHS\xxxx account
- FDT\xxxx account
- FSE\xxxx account
- KABI\xxxx account

Routing:
FHS / FDT

### 2. Does the problem concern a HELIOS account?

Examples:

- HELIOS-DOM account
- HELIOS mailbox
- HELIOS login
- HELIOS password reset
- HELIOS account lockout

Routing:
HELIOS SUPPORT

### 3. Does an FHS / FDT / FSE / KABI user need access to a HELIOS system?

Examples:

- Access to an application, system or data in the HELIOS environment

Routing:
HELIOS SUPPORT

## Important — The address the request was sent from does not determine the routing

Do not decide only by:

- Sender address
- Domain of the requester
- Account used in Self Service
- Email address used to create the ticket

## Examples

| Sent from | Problem concerns | Result |
|---|---|---|
| Sent from an email account | Problem concerns an FHS / FDT account | FHS / FDT (NOT Helios) |
| Sent from an email account | Problem concerns a Helios system | HELIOS SUPPORT (NOT FHS / FDT) |

## Golden rule

- Route by the account the problem concerns.
- Do not route by the account the user sent the request from.

## Most common mistake

The agent sees the sender domain (e.g. @hermed.de, @fresenius.com, @helios-gesundheit.de) and picks the queue straight away.

1. First read the request.
2. Check which account the problem concerns.
3. Only then set the correct routing.

## Calls from Helios users — FDT agents

Status:
Tickets from users with the Helios domain are not handled by FDT yet.

- Phone: ask the user to contact Helios support.
- If someone already redirected the user to us: collect the user information, open a ticket, assign it to Swivel and hand it over to Aga / Gabi / Filip (they raise it with FDT).
- If the user insists on a contact, the safest answer is the email myservice@helios-gesundheit.de.
- Template “FDT Misplaced Call Helios related” — do not use it to close tickets from the Email and SSP channels.
- Email / SSP / Chat go to the Swivel queue Ext_WW_Swivel-Chair-Helios_Capgemini_Helios.
- Chats from Helios users should no longer appear — the option has been blocked.
- An FHS user reporting a Helios problem is handled with the same instruction.

| Item | Details |
|---|---|
| Helios user contact | myservice@helios-gesundheit.de |
| Swivel queue (Email / SSP / Chat) | Ext_WW_Swivel-Chair-Helios_Capgemini_Helios |
| Template | FDT Misplaced Call Helios related |
| Hand over to | Aga / Gabi / Filip |
