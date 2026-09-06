import logging

from config import (
    INPUT_FILE,
    MESSAGE_FILE,
    LOG_FILE
)

from database import (
    init_database,
    add_contact,
    get_statistics
)

from extractor import (
    extract_contacts
)

from mailer import (
    EmailSender
)

from scheduler import (
    run_sender
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


# ============================================================
# LOAD MESSAGE
# ============================================================

def load_message():

    with open(
        MESSAGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# SHOW STATUS
# ============================================================

def show_status(conn):

    print("\n==============================")
    print("DATABASE STATUS")
    print("==============================")

    statistics = get_statistics(
        conn
    )

    for row in statistics:

        print(
            f"{row['status']}: "
            f"{row['count']}"
        )

    print("==============================\n")


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        "========================================\n"
        "       BULK OUTREACH MAILER\n"
        "========================================\n"
    )

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    conn = init_database()

    # --------------------------------------------------------
    # Extract contacts
    # --------------------------------------------------------

    print(
        f"Reading: {INPUT_FILE}"
    )

    contacts = extract_contacts(
        INPUT_FILE
    )

    print(
        f"Found {len(contacts)} contacts."
    )

    # --------------------------------------------------------
    # Store contacts
    # --------------------------------------------------------

    for name, email in contacts:

        add_contact(
            conn,
            name,
            email
        )

    print(
        "Contacts stored in database."
    )

    show_status(conn)

    # --------------------------------------------------------
    # Message
    # --------------------------------------------------------

    message = load_message()

    # --------------------------------------------------------
    # Email sender
    # --------------------------------------------------------

    sender = EmailSender()

    try:

        print(
            "Connecting to SMTP..."
        )

        sender.connect()

        print(
            "SMTP connection successful."
        )

        # ----------------------------------------------------
        # Start sending
        # ----------------------------------------------------

        run_sender(
            conn,
            sender,
            message
        )

    finally:

        sender.close()

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    show_status(conn)

    conn.close()

    print(
        "\nDone."
    )


if __name__ == "__main__":

    main()