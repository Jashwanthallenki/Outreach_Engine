import os
import smtplib

from email.message import EmailMessage

from config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    FROM_NAME,
    RESUME_FILE,
    EMAIL_SUBJECT
)


class EmailSender:

    def __init__(self):

        self.server = None

    def connect(self):

        if not SMTP_USERNAME:

            raise RuntimeError(
                "SMTP_USERNAME is not configured."
            )

        if not SMTP_PASSWORD:

            raise RuntimeError(
                "SMTP_PASSWORD is not configured."
            )

        self.server = smtplib.SMTP(
            SMTP_HOST,
            SMTP_PORT,
            timeout=30
        )

        self.server.starttls()

        self.server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

    def send(
        self,
        name,
        email,
        message_template
    ):

        message_text = message_template.format(
            name=name
        )

        message = EmailMessage()

        message["From"] = (
            f"{FROM_NAME} "
            f"<{SMTP_USERNAME}>"
        )

        message["To"] = email

        message["Subject"] = EMAIL_SUBJECT

        message.set_content(
            message_text
        )

        if RESUME_FILE.exists():

            with open(
                RESUME_FILE,
                "rb"
            ) as file:

                resume_data = file.read()

            message.add_attachment(
                resume_data,
                maintype="application",
                subtype="pdf",
                filename=RESUME_FILE.name
            )

        self.server.send_message(
            message
        )

    def close(self):

        if self.server:

            try:

                self.server.quit()

            except Exception:

                pass