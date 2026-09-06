import os
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
TEMPLATE_DIR = BASE_DIR / "templates"
ATTACHMENT_DIR = BASE_DIR / "attachments"

LOG_FILE = LOG_DIR / "mailer.log"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
TEMPLATE_DIR.mkdir(exist_ok=True)
ATTACHMENT_DIR.mkdir(exist_ok=True)


# ============================================================
# INPUT
# ============================================================

# Supported:
# .csv
# .xlsx
# .xls
# .pdf

INPUT_FILE = BASE_DIR / "contacts.pdf"

MESSAGE_FILE = TEMPLATE_DIR / "message.txt"

RESUME_FILE = ATTACHMENT_DIR / "resume.pdf"


# ============================================================
# DATABASE
# ============================================================

DB_FILE = DATA_DIR / "mailer.db"


# ============================================================
# EMAIL
# ============================================================

SMTP_HOST = os.getenv(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME"
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD"
)

FROM_NAME = os.getenv(
    "FROM_NAME",
    "Your Name"
)


# ============================================================
# SENDING SETTINGS
# ============================================================

# Maximum number of emails per day
DAILY_LIMIT = 100

# Delay between emails
DELAY_BETWEEN_EMAILS = 5

# Maximum retries for failed emails
MAX_RETRIES = 3

# Email subject
EMAIL_SUBJECT = "Exploring Technology Opportunities"
