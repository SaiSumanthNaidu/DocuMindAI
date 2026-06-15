import re


def analyze_document(text):

    text_upper = text.upper()

    if (
        "INCOME TAX DEPARTMENT" in text_upper
        or "PERMANENT ACCOUNT NUMBER CARD" in text_upper
        or "ACCOUNT NUMBER CARD" in text_upper
    ):

        result = {
            "document_type": "PAN Card"
        }

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        dob_match = re.search(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        if dob_match:
            result["dob"] = dob_match.group()

        pan_match = re.search(
            r"[A-Z]{5}[0-9]{4}[A-Z]",
            text
        )

        if pan_match:
            result["pan_number"] = pan_match.group()

        for i, line in enumerate(lines):

            if "FATHER" in line.upper():

                if i + 1 < len(lines):
                    result["father_name"] = lines[i + 1]

        ignore_words = [
            "GOVT",
            "INDIA",
            "INCOME",
            "DEPARTMENT",
            "ACCOUNT",
            "NUMBER",
            "CARD",
            "FATHER",
            "SIGNATURE"
        ]

        candidate_names = []

        for line in lines:

            upper_line = line.upper()

            if any(word in upper_line for word in ignore_words):
                continue

            if len(line.split()) >= 2:
                candidate_names.append(line)

        if candidate_names:

            candidate_names.sort(
                key=len,
                reverse=True
            )

            result["name"] = candidate_names[0]

        return result

    return {
        "document_type": "Unknown",
        "raw_text_preview": text[:500]
    }