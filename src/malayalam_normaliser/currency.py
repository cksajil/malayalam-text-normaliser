"""Currency amounts written with a rupee sign, 'Rs', or 'INR' before the number.

'₹1500' -> 'ആയിരത്തി അഞ്ഞൂറ് രൂപ'
'Rs 12.50' -> 'പന്ത്രണ്ട് രൂപ അമ്പത് പൈസ'

An amount that ends in 'രൂപ' already (for example '1500 രൂപ') is handled by
the number step, so only the prefix forms are matched here.
"""

from __future__ import annotations

import re

from .numbers import number_to_words, spell_number

# verify with a native speaker
RUPEE = "രൂപ"
PAISE = "പൈസ"

_CURRENCY_RE = re.compile(
    r"(?:₹|(?<![A-Za-z])(?i:rs)\.?|(?<![A-Za-z])INR)"
    r"\s*"
    r"((?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3}|\d+))"  # 1: integer part
    r"(?:\.(\d+))?"  # 2: decimal part
    r"(?![0-9A-Za-zഀ-ൿ])(?![.,/:\-]\d)"
)


def _currency_repl(m: re.Match[str]) -> str:
    int_text, dec_text = m.group(1), m.group(2)
    if dec_text is None or len(dec_text) > 2:
        if dec_text is not None:
            return f"{spell_number(int_text, dec_text)} {RUPEE}"
        return f"{spell_number(int_text)} {RUPEE}"

    digits = int_text.replace(",", "")
    if len(digits) > 1 and digits[0] == "0":
        return m.group(0)
    paise = int(dec_text.ljust(2, "0"))
    spoken = f"{spell_number(int_text)} {RUPEE}"
    if paise:
        spoken += f" {number_to_words(paise)} {PAISE}"
    return spoken


def convert_currency(text: str) -> str:
    """Convert rupee amounts. Run this before the number step."""
    return _CURRENCY_RE.sub(_currency_repl, text)
