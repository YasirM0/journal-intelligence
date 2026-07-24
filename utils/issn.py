"""
ISSN parsing/normalization shared by all importers.
"""

import re


def normalize_issn(raw):
    """
    Normalize an ISSN into standard XXXX-XXXX form. Accepts values with
    or without a hyphen, and a final check digit of 0-9 or X. Returns
    None if the value isn't a plausible 8-character ISSN.
    """
    if raw is None:
        return None

    cleaned = re.sub(r"[^0-9Xx]", "", str(raw)).upper()

    if len(cleaned) != 8:
        return None

    return f"{cleaned[:4]}-{cleaned[4:]}"


def extract_issns(raw):
    """
    Extract all normalized ISSNs from a field that may contain more than
    one, separated by commas/semicolons (e.g. SCImago's combined column).
    """
    if raw is None:
        return []

    parts = re.split(r"[;,]", str(raw))

    issns = [normalize_issn(part) for part in parts]

    return [issn for issn in issns if issn]
