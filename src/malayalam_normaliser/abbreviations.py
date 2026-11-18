"""Fixed abbreviation table. One entry per line; keys are matched exactly.

Entries whose key starts or ends with a letter only match whole words, so
'km' does not match inside 'kmph'. Spellings are unverified; see README.
"""

from __future__ import annotations

import re

ABBREVIATIONS = {
    "Dr.": "ഡോക്ടർ",  # verify with a native speaker
    "Mr.": "മിസ്റ്റർ",  # verify with a native speaker
    "Mrs.": "മിസിസ്",  # verify with a native speaker
    "Ltd.": "ലിമിറ്റഡ്",  # verify with a native speaker
    "Rs": "രൂപ",  # verify with a native speaker
    "km": "കിലോമീറ്റർ",  # verify with a native speaker
    "kg": "കിലോഗ്രാം",  # verify with a native speaker
    "ml": "മില്ലിലിറ്റർ",  # verify with a native speaker
    "No.": "നമ്പർ",  # verify with a native speaker
    "&": "ആൻഡ്",  # verify with a native speaker
}


def _pattern_for(key: str) -> re.Pattern[str]:
    body = re.escape(key)
    if key[0].isalnum():
        body = r"(?<![A-Za-z])" + body
    if key[-1].isalnum():
        body = body + r"(?![A-Za-z])"
    return re.compile(body)


_PATTERNS = [(_pattern_for(key), spoken) for key, spoken in ABBREVIATIONS.items()]


def expand_abbreviations(text: str) -> str:
    """Replace each abbreviation from ABBREVIATIONS with its spoken form."""
    for pattern, spoken in _PATTERNS:
        text = pattern.sub(lambda _m, s=spoken: s, text)
    return text
