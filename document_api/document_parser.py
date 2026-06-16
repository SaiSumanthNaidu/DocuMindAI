import re


def analyze_document(text):

    text_upper = text.upper()

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # ==========================
    # PAN CARD
    # ==========================
    if (
        "INCOME TAX DEPARTMENT" in text_upper
        or "PERMANENT ACCOUNT NUMBER CARD" in text_upper
        or "ACCOUNT NUMBER CARD" in text_upper
    ):

        result = {
            "document_type": "PAN Card"
        }

        pan_match = re.search(
            r"[A-Z]{5}[0-9]{4}[A-Z]",
            text
        )

        if pan_match:
            result["pan_number"] = pan_match.group()

        dob_match = re.search(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        if dob_match:
            result["dob"] = dob_match.group()

        for i, line in enumerate(lines):

            if "FATHER" in line.upper():

                if i - 1 >= 0:
                    result["name"] = lines[i - 1]

                if i + 1 < len(lines):

                    father_name = re.sub(
                        r"\d+",
                        "",
                        lines[i + 1]
                    ).strip()

                    result["father_name"] = father_name

        return result

    # ==========================
    # AADHAAR CARD
    # ==========================
    elif (
        "AADHAAR" in text_upper
        or "UNIQUE IDENTIFICATION AUTHORITY" in text_upper
    ):

        result = {
            "document_type": "Aadhaar Card"
        }

        aadhaar_match = re.search(
            r"\d{4}\s\d{4}\s\d{4}",
            text
        )

        if aadhaar_match:
            result["aadhaar_number"] = aadhaar_match.group()

        dob_match = re.search(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        if dob_match:
            result["dob"] = dob_match.group()

        gender_match = re.search(
            r"MALE|FEMALE",
            text_upper
        )

        if gender_match:
            result["gender"] = gender_match.group().title()

        for line in lines:

            if (
                len(line.split()) >= 2
                and not any(
                    word in line.upper()
                    for word in [
                        "AADHAAR",
                        "INDIA",
                        "GOVERNMENT",
                        "DOB",
                        "MALE",
                        "FEMALE"
                    ]
                )
            ):
                result["name"] = line
                break

        return result

    # ==========================
    # RESUME
    # ==========================
    elif (
        "SKILLS" in text_upper
        or "EDUCATION" in text_upper
        or "EXPERIENCE" in text_upper
    ):

        result = {
            "document_type": "Resume"
        }

        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        if email_match:
            result["email"] = email_match.group()

        phone_match = re.search(
            r'\+?\d[\d\s-]{8,15}',
            text
        )

        if phone_match:
            result["phone"] = phone_match.group()

        if lines:
            result["name"] = lines[0]

        return result

    # ==========================
    # DRIVING LICENSE
    # ==========================
    elif (
        "DRIVING LICENCE" in text_upper
        or "DRIVING LICENSE" in text_upper
    ):

        result = {
            "document_type": "Driving License"
        }

        dl_match = re.search(
            r"[A-Z]{2}[0-9]{2}\s?[0-9]{11}",
            text_upper
        )

        if dl_match:
            result["license_number"] = dl_match.group()

        dob_match = re.search(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        if dob_match:
            result["dob"] = dob_match.group()

        return result

    # ==========================
    # PASSPORT
    # ==========================
    elif "PASSPORT" in text_upper:

        result = {
            "document_type": "Passport"
        }

        passport_match = re.search(
            r"[A-Z][0-9]{7}",
            text_upper
        )

        if passport_match:
            result["passport_number"] = passport_match.group()

        dob_match = re.search(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        if dob_match:
            result["dob"] = dob_match.group()

        return result

    # ==========================
    # UNKNOWN DOCUMENT
    # ==========================
    return {
        "document_type": "Unknown",
        "raw_text_preview": text[:500]
    }