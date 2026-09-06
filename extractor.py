import csv
import re
from pathlib import Path

import pandas as pd
import pdfplumber


EMAIL_REGEX = re.compile(
    r"[A-Za-z0-9._%+-]+"
    r"@"
    r"[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}"
)


# ============================================================
# HELPERS
# ============================================================

def normalize_column(column):

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def valid_email(email):

    return bool(
        EMAIL_REGEX.fullmatch(
            email.strip()
        )
    )


# ============================================================
# CSV
# ============================================================

def extract_csv(file_path):

    contacts = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:

            raise ValueError(
                "CSV does not contain headers."
            )

        columns = {
            normalize_column(column): column
            for column in reader.fieldnames
        }

        email_column = None
        name_column = None

        for normalized, original in columns.items():

            if normalized in [
                "email",
                "email_address",
                "mail",
                "e_mail"
            ]:

                email_column = original

            if normalized in [
                "name",
                "full_name",
                "candidate_name",
                "person_name"
            ]:

                name_column = original

        if not email_column:

            raise ValueError(
                "Could not find an email column."
            )

        for row in reader:

            email = str(
                row.get(email_column, "")
            ).strip()

            if not valid_email(email):

                continue

            name = "Sir/Madam"

            if name_column:

                name = str(
                    row.get(name_column, "")
                ).strip()

                if not name:

                    name = "Sir/Madam"

            contacts.append(
                (
                    name,
                    email.lower()
                )
            )

    return contacts


# ============================================================
# EXCEL
# ============================================================

def extract_excel(file_path):

    contacts = []

    df = pd.read_excel(file_path)

    columns = {
        normalize_column(column): column
        for column in df.columns
    }

    email_column = None
    name_column = None

    for normalized, original in columns.items():

        if normalized in [
            "email",
            "email_address",
            "mail",
            "e_mail"
        ]:

            email_column = original

        if normalized in [
            "name",
            "full_name",
            "candidate_name",
            "person_name"
        ]:

            name_column = original

    if not email_column:

        raise ValueError(
            "Could not find an email column."
        )

    for _, row in df.iterrows():

        email = str(
            row[email_column]
        ).strip()

        if email.lower() == "nan":

            continue

        if not valid_email(email):

            continue

        name = "Sir/Madam"

        if name_column:

            name = str(
                row[name_column]
            ).strip()

            if name.lower() == "nan":

                name = "Sir/Madam"

        contacts.append(
            (
                name,
                email.lower()
            )
        )

    return contacts


# ============================================================
# PDF
# ============================================================

def extract_pdf(file_path):

    contacts = []

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text() or ""

            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

            for index, line in enumerate(lines):

                emails = EMAIL_REGEX.findall(line)

                for email in emails:

                    name = "Sir/Madam"

                    # Example:
                    # Name: John Doe
                    name_match = re.search(
                        r"name\s*:\s*(.+)",
                        line,
                        re.IGNORECASE
                    )

                    if name_match:

                        possible_name = (
                            name_match.group(1)
                            .strip()
                        )

                        possible_name = (
                            possible_name
                            .replace(email, "")
                            .strip()
                        )

                        if possible_name:

                            name = possible_name

                    # Otherwise use previous line
                    elif index > 0:

                        previous_line = lines[
                            index - 1
                        ]

                        if (
                            not EMAIL_REGEX.search(
                                previous_line
                            )
                        ):

                            name = previous_line

                    contacts.append(
                        (
                            name,
                            email.lower()
                        )
                    )

    # Remove duplicates
    unique_contacts = {}

    for name, email in contacts:

        unique_contacts[email] = (
            name,
            email
        )

    return list(
        unique_contacts.values()
    )


# ============================================================
# MAIN EXTRACTOR
# ============================================================

def extract_contacts(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".csv":

        return extract_csv(file_path)

    elif extension in [
        ".xlsx",
        ".xls"
    ]:

        return extract_excel(file_path)

    elif extension == ".pdf":

        return extract_pdf(file_path)

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )