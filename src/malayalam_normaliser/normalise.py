"""The normalisation pipeline. Order matters:

1. currency      ('₹1500' before the bare number is read)
2. dates, times  (before '/', '-' and ':' are lost to the number step)
3. percentages   ('45%' before the bare number is read)
4. numbers
5. abbreviations
6. NFC           (applied to the final output)
"""

from __future__ import annotations

import unicodedata

from .abbreviations import expand_abbreviations
from .currency import convert_currency
from .dates import convert_dates, convert_times
from .numbers import convert_numbers, convert_percentages


def normalise(text: str) -> str:
    """Return text with numbers, currency, dates, times and symbols spoken in Malayalam.

    Other text, including Malayalam letters, chillu characters and ZWJ/ZWNJ,
    is left as it appears in the input (the output is NFC-normalised).
    """
    if not isinstance(text, str):
        raise TypeError(f"normalise() expects str, got {type(text).__name__}")

    out = convert_currency(text)
    out = convert_dates(out)
    out = convert_times(out)
    out = convert_percentages(out)
    out = convert_numbers(out)
    out = expand_abbreviations(out)
    return unicodedata.normalize("NFC", out)
