import time
import logging

from config import (
    DAILY_LIMIT,
    DELAY_BETWEEN_EMAILS,
    MAX_RETRIES
)

from database import (
    get_today_sent_count,
    get_pending_contacts,
    mark_sent,
    mark_failed
)


logger = logging.getLogger(__name__)


def run_sender(
    conn,
    email_sender,
    message
):

    sent_today = get_today_sent_count(
        conn
    )

    remaining = (
        DAILY_LIMIT - sent_today
    )

    if remaining <= 0:

        print(
            f"Daily limit reached "
            f"({DAILY_LIMIT})."
        )

        return

    contacts = get_pending_contacts(
        conn,
        remaining
    )

    if not contacts:

        print(
            "No pending contacts."
        )

        return

    print(
        f"Already sent today: "
        f"{sent_today}"
    )

    print(
        f"Remaining today: "
        f"{remaining}"
    )

    print(
        f"Contacts to process: "
        f"{len(contacts)}"
    )

    for contact in contacts:

        contact_id = contact["id"]
        name = contact["name"]
        email = contact["email"]
        attempts = contact["attempts"]

        print(
            f"\n[{contact_id}] "
            f"{name} <{email}>"
        )

        try:

            email_sender.send(
                name,
                email,
                message
            )

            mark_sent(
                conn,
                contact_id
            )

            print(
                "✓ SENT"
            )

            logger.info(
                f"SENT | {name} | {email}"
            )

        except Exception as error:

            mark_failed(
                conn,
                contact_id,
                error
            )

            print(
                f"✗ FAILED | {error}"
            )

            logger.error(
                f"FAILED | "
                f"{name} | "
                f"{email} | "
                f"{error}"
            )

        time.sleep(
            DELAY_BETWEEN_EMAILS
        )