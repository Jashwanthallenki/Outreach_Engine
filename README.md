# Bulk Outreach Mailer

A lightweight and persistent bulk email automation tool built with Python.

The application extracts names and email addresses from a PDF, personalizes an email template, attaches a document, and sends emails through SMTP while maintaining persistent delivery state using SQLite.

It is designed to be reusable for professional outreach, recruitment, networking, announcements, and other legitimate email workflows.

---

## ✨ Features

- 📄 Extract names and email addresses from PDF files
- ✉️ Personalized emails using `{name}` placeholders
- 📎 PDF attachment support
- 🔐 Secure SMTP credential configuration
- 💾 Persistent SQLite database
- 🛑 Prevents duplicate emails to already processed contacts
- 📊 Configurable daily sending limit
- 🔄 Failed email tracking and retries
- ⏱️ Configurable delay between emails
- 📝 Email activity logging
- 🧩 Modular and extensible architecture

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
bulk-mailer/
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
│   └── .gitkeep
│
├── data/
│   └── .gitkeep
│
└── logs/
    └── .gitkeep
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd bulk-mailer
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

---

## 🔐 Configuration

The application uses environment variables for SMTP credentials and other sensitive configuration.

Create a local `.env` file:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password
FROM_NAME=Your Name
```

> **Never commit `.env` to GitHub.**

A safe `.env.example` file is included in the repository so users know which variables are required.

---

## 📧 Gmail Configuration

If you are using Gmail, use a Google App Password instead of your normal Gmail password.

Example:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_NAME=Your Name
```

Make sure the required Google account security settings are enabled before generating an App Password.

---

## 📄 Contact List

The application expects a PDF contact list.

Default file:

```text
contacts.pdf
```

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

Create:

```text
templates/message.txt
```

Example:

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

The `{name}` placeholder is automatically replaced with the contact's name.

For example:

```text
Hello John,
```

---

## 📎 Attachments

Place the file you want to attach inside:

```text
attachments/
```

For example:

```text
attachments/resume.pdf
```

Configure the attachment path in `config.py`.

For a public repository, do not commit personal resumes or private documents.

---

## ⚙️ Configuration Options

The main configuration is available in `config.py`:

```python
DAILY_LIMIT = 10
DELAY_BETWEEN_EMAILS = 5
MAX_RETRIES = 3
EMAIL_SUBJECT = "Exploring Technology Opportunities"
```

| Option | Description |
|---|---|
| `DAILY_LIMIT` | Maximum number of emails sent per day (e.g. `10`). |
| `DELAY_BETWEEN_EMAILS` | Seconds to wait between email attempts (e.g. `5`). |
| `MAX_RETRIES` | Maximum number of failed attempts per contact (e.g. `3`). |
| `EMAIL_SUBJECT` | Subject line used for outgoing emails. |

---

## 💾 Persistent State

The application uses SQLite to maintain its state:

```text
data/mailer.db
```

Each contact is stored with information such as:

```text
id
name
email
status
attempts
last_error
sent_at
created_at
```

Example:

| ID | Name | Email | Status | Attempts |
|---|---|---|---|---|
| 1 | John Smith | john@example.com | SENT | 0 |
| 2 | Jane Doe | jane@example.com | FAILED | 2 |
| 3 | Alex Brown | alex@example.com | PENDING | 0 |

---

## 🔄 Email Processing Flow

Each contact follows this lifecycle:

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

- **PENDING** — The contact has not been successfully processed.
- **SENT** — The email was successfully submitted to the SMTP server.
- **FAILED** — The sending attempt failed and may be retried.

---

## 🛡️ Duplicate Protection

Email addresses are stored as unique records in the database.

For example, if the PDF contains:

```text
john@example.com
john@example.com
john@example.com
```

only one contact record is stored.

Once a contact is marked `SENT`, future executions will not send another email to that contact.

---

## 📊 Daily Sending Limit

The application tracks the number of emails sent on the current day.

For example:

```text
DAILY_LIMIT = 10

Already sent today: 7
Remaining:          3
```

Only three additional contacts will be processed.

If the limit has already been reached:

```text
Already sent today: 10
Remaining:          0
```

the application stops sending for that execution.

Because the state is stored in SQLite, restarting the application does not reset the sending count.

---

## ▶️ Running the Application

Start the application with:

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

The application does not lose its progress when restarted.

For example, on Day 1:

```text
SENT     → 10
PENDING  → 90
```

After restarting:

```text
SENT     → 10
PENDING  → 90
```

The application continues processing pending contacts instead of starting from the beginning.

---

## 📝 Logging

Application logs are stored in:

```text
logs/mailer.log
```

Example:

```text
2026-09-06 09:15:32 | INFO | SENT | John Smith | john@example.com
2026-09-06 09:15:38 | INFO | SENT | Jane Doe | jane@example.com
2026-09-06 09:15:44 | ERROR | FAILED | Alex Brown | SMTP error
```

Logs can be used to investigate failures and monitor application activity.

---

## 🧪 Testing

Before processing a large contact list, test the application with a small dataset. Recommended workflow:

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
Make sure the environment variable is configured correctly.

**`SMTP_PASSWORD is not configured`**
Check that `SMTP_PASSWORD=your-app-password` is set. For Gmail, use an App Password when required.

**Authentication Failed**
Check:
- SMTP username
- SMTP password
- SMTP host
- SMTP port
- Account security settings
- App Password configuration

**Daily Limit Reached**
```text
Daily limit reached (10).
```
This means the configured number of emails has already been sent today. This is expected behavior.

**No Pending Contacts**
```text
No pending contacts.
```
The database may already contain all contacts as `SENT`, or contacts may have exhausted their retry attempts.

**PDF Contacts Not Detected**
Possible causes:
- PDF contains scanned images
- Text extraction is not supported by the PDF structure
- Names and emails are arranged in an unexpected format

Text-based PDFs are recommended. OCR support can be added as a future enhancement.

---

## 🔒 Security

Never commit sensitive information to GitHub. Do not commit:

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

The `.gitignore` file is configured to prevent common sensitive files from being tracked.

> **Important:** `.gitignore` only prevents untracked files from being added. If a secret has already been committed to Git history, simply adding it to `.gitignore` is not enough — the secret should be revoked or rotated and the sensitive file should be removed from Git history.

---

## 🌍 Public Repository Structure

The repository separates reusable source code from personal information.

**Safe to publish**

```text
main.py
config.py
database.py
extractor.py
mailer.py
scheduler.py
requirements.txt
README.md
.env.example
templates/message.example.txt
```

**Keep private**

```text
.env
contacts.pdf
resume.pdf
mailer.db
mailer.log
personal templates
private datasets
credentials
```

---

## 🧩 Project Modules

### `main.py`
Application entry point. Responsible for:
- Initializing the database
- Extracting contacts
- Loading the message
- Starting the SMTP connection
- Running the sending process
- Displaying statistics

### `config.py`
Central configuration. Contains:
- File paths
- SMTP configuration
- Daily sending limit
- Retry configuration
- Email subject
- Delay configuration

### `database.py`
Handles persistent application state. Responsible for:
- Creating the database
- Adding contacts
- Fetching pending contacts
- Marking contacts as sent
- Marking contacts as failed
- Tracking daily sending statistics

### `extractor.py`
Responsible for extracting contacts from input files.

```text
contacts.pdf
     │
     ▼
PDF text extraction
     │
     ▼
Email detection
     │
     ▼
Name detection
     │
     ▼
(name, email)
```

### `mailer.py`
Responsible for email delivery. Handles:
- SMTP connection
- Authentication
- Message creation
- Personalization
- Attachments
- Email delivery

### `scheduler.py`
Controls the sending workflow. Responsible for:
- Daily limits
- Selecting contacts
- Retry handling
- Delays between emails
- Updating contact status

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

**Persistence**
Application state is stored outside the Python process. This allows the application to recover its progress after:
- Application restart
- System restart
- SMTP failures
- Network interruptions

**Idempotency**
Successfully processed contacts are marked `SENT`. Future executions ignore these contacts, which helps prevent accidental duplicate emails.

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

Contributions are welcome.

Create a feature branch:

```bash
git checkout -b feature/my-feature
```

Make your changes, test them, and submit a pull request. Please make sure no personal information or credentials are included in commits.

---

## ⚠️ Responsible Usage

This project is intended for legitimate and professional communication. Users are responsible for complying with applicable:

- Email regulations
- Privacy laws
- Anti-spam requirements
- Email provider policies
- Recipient preferences

Do not use this project for:

- Spam
- Phishing
- Impersonation
- Deceptive communication
- Circumventing provider restrictions
- Unwanted bulk messaging

Use appropriate consent, opt-out, and communication practices where required.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## ⭐ Project Overview

```text
                 ┌──────────────┐
                 │ Contact PDF  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Extract    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │    Store     │
                 │   SQLite     │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Schedule   │
                 │ Daily Limits │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Personalize  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │     Send     │
                 │     SMTP     │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │    Track     │
                 │ SENT/FAILED  │
                 └──────────────┘
```

## Built With

- Python
- SQLite
- SMTP
- pdfplumber
- pandas
- openpyxl

---

## 📬 Support

If you find a bug or have an improvement suggestion, please open a GitHub issue. Pull requests are welcome.