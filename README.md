# 📬 Outreach Engine

**A lightweight, persistent bulk email automation tool built with Python.**

Outreach Engine extracts names and email addresses from a PDF, personalizes an email template per contact, attaches a document (like a resume), and sends emails through SMTP — all while tracking delivery state in SQLite so nothing is ever sent twice, even across restarts.

Built for professional outreach, recruitment, networking, and announcement workflows.

<p>
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-unspecified-lightgrey">
  <img alt="Status" src="https://img.shields.io/badge/status-active-brightgreen">
</p>

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Gmail Setup](#-gmail-configuration)
- [Contact List (PDF)](#-contact-list)
- [Email Template](#️-email-template)
- [Attachments](#-attachments)
- [Configuration Options](#️-configuration-options)
- [Persistent State](#-persistent-state)
- [Email Processing Flow](#-email-processing-flow)
- [Duplicate Protection](#️-duplicate-protection)
- [Daily Sending Limit](#-daily-sending-limit)
- [Running the Application](#️-running-the-application)
- [Continuing After Restart](#-continuing-after-restart)
- [Logging](#-logging)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Security](#-security)
- [Public Repository Structure](#-public-repository-structure)
- [Project Modules](#-project-modules)
- [Design Principles](#-design-principles)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [Responsible Usage](#️-responsible-usage)
- [License](#-license)

---

## ✨ Features

- 📄 Extract names and email addresses from PDF files
- ✉️ Personalized emails using `{name}` placeholders
- 📎 PDF attachment support
- 🔐 Secure SMTP credential configuration via environment variables
- 💾 Persistent SQLite database — survives restarts
- 🛑 Prevents duplicate emails to already-processed contacts
- 📊 Configurable daily sending limit
- 🔄 Failed email tracking and retries
- ⏱️ Configurable delay between emails
- 📝 Email activity logging
- 🧩 Modular, single-responsibility architecture

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   contacts.pdf   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   extractor.py   │
                    │  PDF Extraction  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   database.py    │
                    │      SQLite      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   scheduler.py   │
                    │                  │
                    │ Daily Limit      │
                    │ Retry Handling   │
                    │ Delay Control    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     mailer.py    │
                    │                  │
                    │ SMTP Connection  │
                    │ Personalization  │
                    │ Attachments      │
                    └────────┬─────────┘
                             │
                             ▼
                       ┌────────────┐
                       │ SMTP Server│
                       └─────┬──────┘
                             │
                             ▼
                          Recipient
```

---

## 📁 Project Structure

```text
Outreach_Engine/
│
├── main.py
├── config.py
├── database.py
├── extractor.py
├── mailer.py
├── scheduler.py
│
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── message.example.txt
│
├── attachments/
│   └── (place resume.pdf or other attachments here)
│
├── data/            # created automatically — holds mailer.db
└── logs/            # created automatically — holds mailer.log
```

> `data/` and `logs/` are generated at runtime and are gitignored, so they won't appear in a fresh clone until you run the app.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Jashwanthallenki/Outreach_Engine.git
cd Outreach_Engine
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies (`requirements.txt`):

```text
pandas
openpyxl
pdfplumber
```

### 4. Configure and Run

```bash
cp .env.example .env      # then fill in your SMTP credentials
python main.py
```

---

## 🔐 Configuration

The application uses environment variables for SMTP credentials and other sensitive configuration.

Create a local `.env` file (copy `.env.example` as a starting point):

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password
FROM_NAME=Your Name
```

> ⚠️ **Never commit `.env` to GitHub.**

---

## 📧 Gmail Configuration

If you're using Gmail, use a **Google App Password** instead of your normal Gmail password.

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_NAME=Your Name
```

Make sure 2-Step Verification is enabled on the account before generating an App Password.

---

## 📄 Contact List

The application expects a PDF contact list.

Default file: `contacts.pdf`

Example content:

```text
John Smith
john@example.com

Jane Doe
jane@example.com

Alex Johnson
alex@example.com
```

The extractor searches the PDF for email addresses and attempts to identify the associated name.

### PDF Requirements

- Text-based PDFs generally work best.
- Scanned or image-only PDFs may require OCR support.
- Extraction quality depends on how the PDF is structured.

---

## ✉️ Email Template

Create `templates/message.txt`:

```text
Hello {name},

I hope you're doing well.

I'm currently exploring opportunities in AI/ML, SDE,
backend engineering, systems, and other technology-focused roles.

I've gained hands-on experience through internships and projects
across scalable backend systems, enterprise automation, RAG,
Agentic AI, HLD, LLD, and modern software engineering stacks.

I've attached my resume for your consideration.

I'd really appreciate it if you could let me know if there are
any relevant opportunities at your organization.

Thank you for your time.

Best regards,
Your Name
```

The `{name}` placeholder is automatically replaced with the contact's name:

```text
Hello John,
```

---

## 📎 Attachments

Place the file you want to attach inside `attachments/`, e.g.:

```text
attachments/resume.pdf
```

Configure the attachment path in `config.py`. For a public repository, do not commit personal resumes or private documents.

---

## ⚙️ Configuration Options

The main configuration lives in `config.py`:

```python
DAILY_LIMIT = 10
DELAY_BETWEEN_EMAILS = 5
MAX_RETRIES = 3
EMAIL_SUBJECT = "Exploring Technology Opportunities"
```

| Option | Description |
|---|---|
| `DAILY_LIMIT` | Maximum number of emails sent per day. |
| `DELAY_BETWEEN_EMAILS` | Seconds to wait between email attempts. |
| `MAX_RETRIES` | Maximum number of failed attempts per contact before giving up. |
| `EMAIL_SUBJECT` | Subject line used for outgoing emails. |

---

## 💾 Persistent State

The application uses SQLite (`data/mailer.db`) to maintain its state. Each contact record includes:

```text
id, name, email, status, attempts, last_error, sent_at, created_at
```

| ID | Name | Email | Status | Attempts |
|---|---|---|---|---|
| 1 | John Smith | john@example.com | SENT | 0 |
| 2 | Jane Doe | jane@example.com | FAILED | 2 |
| 3 | Alex Brown | alex@example.com | PENDING | 0 |

---

## 🔄 Email Processing Flow

```text
             ┌─────────┐
             │ PENDING │
             └────┬────┘
                  │
                  ▼
             ┌─────────┐
             │ SENDING │
             └────┬────┘
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
      ┌────────┐      ┌─────────┐
      │  SENT  │      │ FAILED  │
      └────────┘      └────┬────┘
                           │
                           ▼
                         Retry
```

| Status | Meaning |
|---|---|
| `PENDING` | Not yet successfully processed. |
| `SENT` | Successfully submitted to the SMTP server. |
| `FAILED` | Sending attempt failed; may be retried. |

---

## 🛡️ Duplicate Protection

Email addresses are stored as unique records — if the same address appears multiple times in the PDF, only one contact record is created. Once a contact is marked `SENT`, future runs will never email them again.

---

## 📊 Daily Sending Limit

The app tracks how many emails were sent today and stops once `DAILY_LIMIT` is reached:

```text
DAILY_LIMIT = 10
Already sent today: 7
Remaining:          3
```

Because the count lives in SQLite, restarting the app does **not** reset it — the limit is enforced across the whole day, not per run.

---

## ▶️ Running the Application

```bash
python main.py
```

Example output:

```text
========================================
       BULK OUTREACH MAILER
========================================

Reading: contacts.pdf
Found 42 contacts.
Contacts stored in database.

==============================
DATABASE STATUS
==============================
PENDING: 42
==============================

Connecting to SMTP...
SMTP connection successful.

Already sent today: 0
Remaining today: 10
Contacts to process: 10

[1] John Smith <john@example.com>
✓ SENT

[2] Jane Doe <jane@example.com>
✓ SENT

...

Done.
```

---

## 🔁 Continuing After Restart

Progress is never lost. On Day 1:

```text
SENT     → 10
PENDING  → 90
```

After restarting, the app picks up exactly where it left off:

```text
SENT     → 10
PENDING  → 90
```

---

## 📝 Logging

Logs are written to `logs/mailer.log`:

```text
2026-09-06 09:15:32 | INFO | SENT | John Smith | john@example.com
2026-09-06 09:15:38 | INFO | SENT | Jane Doe | jane@example.com
2026-09-06 09:15:44 | ERROR | FAILED | Alex Brown | SMTP error
```

---

## 🧪 Testing

Before processing a large contact list, test with a small dataset:

1. Create a small test PDF.
2. Add a few test email addresses.
3. Configure SMTP.
4. Set `DAILY_LIMIT = 2`.
5. Run the application.
6. Verify received emails.
7. Check database state.
8. Check logs.
9. Increase the limit when ready.

---

## 🔍 Troubleshooting

**`SMTP_USERNAME is not configured`**
Make sure the environment variable is set correctly in `.env`.

**`SMTP_PASSWORD is not configured`**
Check `SMTP_PASSWORD=your-app-password`. For Gmail, use an App Password.

**Authentication Failed** — check:
- SMTP username
- SMTP password
- SMTP host
- SMTP port
- Account security settings / App Password configuration

**Daily Limit Reached**
```text
Daily limit reached (10).
```
Expected behavior — the configured number of emails has already gone out today.

**No Pending Contacts**
```text
No pending contacts.
```
All contacts are already `SENT`, or remaining ones have exhausted their retries.

**PDF Contacts Not Detected** — possible causes:
- PDF contains scanned images (needs OCR)
- Text extraction unsupported by the PDF's structure
- Names/emails arranged in an unexpected format

---

## 🔒 Security

Never commit sensitive information. Keep these out of Git:

```text
.env
contacts.pdf
resume.pdf
mailer.db
*.sqlite
*.log
personal templates
API keys
SMTP passwords
private contact lists
```

`.gitignore` only prevents **untracked** files from being added. If a secret was already committed, adding it to `.gitignore` isn't enough — revoke/rotate the credential and scrub it from Git history.

---

## 🌍 Public Repository Structure

**Safe to publish**
```text
main.py, config.py, database.py, extractor.py, mailer.py, scheduler.py,
requirements.txt, README.md, .env.example, templates/message.example.txt
```

**Keep private**
```text
.env, contacts.pdf, resume.pdf, mailer.db, mailer.log,
personal templates, private datasets, credentials
```

---

## 🧩 Project Modules

| Module | Responsibility |
|---|---|
| `main.py` | Entry point — initializes the DB, extracts contacts, loads the message, opens the SMTP connection, runs the send loop, prints stats. |
| `config.py` | Central configuration — file paths, SMTP settings, daily limit, retry policy, subject line, delay. |
| `database.py` | Persistent state — create DB, add contacts, fetch pending, mark sent/failed, track daily stats. |
| `extractor.py` | Pulls `(name, email)` pairs out of the contact PDF. |
| `mailer.py` | SMTP connection, auth, message construction, personalization, attachments, delivery. |
| `scheduler.py` | Orchestrates the run — daily limits, contact selection, retries, delays, status updates. |

`extractor.py` flow:

```text
contacts.pdf → PDF text extraction → Email detection → Name detection → (name, email)
```

---

## 🧠 Design Principles

**Separation of Concerns**
```text
Extraction       → extractor.py
Persistence      → database.py
Email Delivery   → mailer.py
Scheduling       → scheduler.py
Configuration    → config.py
Application      → main.py
```

**Persistence** — state lives outside the Python process, so the app recovers cleanly from app/system restarts, SMTP failures, and network interruptions.

**Idempotency** — contacts marked `SENT` are never processed again, preventing accidental duplicate emails.

---

## 🚀 Future Enhancements

- Automatic next-day scheduling
- HTML email templates
- Multiple attachment support
- Web-based dashboard
- PostgreSQL/Redis support
- Campaign and contact management
- Multiple SMTP provider support
- Docker deployment
- Email analytics and reporting

---

## 🤝 Contributing

```bash
git checkout -b feature/my-feature
```

Make your changes, test them, and open a pull request. Make sure no personal information or credentials are included in commits.

---

## ⚠️ Responsible Usage

This project is for legitimate, professional communication. You're responsible for complying with applicable email regulations, privacy laws, anti-spam requirements, provider policies, and recipient preferences.

Do **not** use this for spam, phishing, impersonation, deceptive communication, circumventing provider restrictions, or unwanted bulk messaging. Use appropriate consent and opt-out practices where required.

---

## 📜 License

No `LICENSE` file is currently included in this repository. Until one is added, the code is **not** licensed for reuse by others under standard GitHub defaults — add a `LICENSE` file (e.g. MIT) if you want to permit that explicitly.

---

## Built With

- Python
- SQLite
- SMTP
- pdfplumber
- pandas
- openpyxl

---

## 📬 Support

Found a bug or have an improvement idea? Open a GitHub issue — pull requests are welcome.
