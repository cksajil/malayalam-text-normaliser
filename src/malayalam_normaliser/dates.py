"""Dates (dd/mm/yyyy, dd-mm-yyyy) and times (hh:mm, 24h or 12h with am/pm).

Invalid dates and times (31/02/2026, 25:00) are returned unchanged. The
number step also leaves them alone, because numbers next to '/', '-' or ':'
are skipped there.
"""

from __future__ import annotations

import datetime
import re

from .numbers import number_to_words, spell_number

# verify with a native speaker
MONTHS = (
    "ജനുവരി",
    "ഫെബ്രുവരി",
    "മാർച്ച്",
    "ഏപ്രിൽ",
    "മേയ്",
    "ജൂൺ",
    "ജൂലൈ",
    "ഓഗസ്റ്റ്",
    "സെപ്റ്റംബർ",
    "ഒക്ടോബർ",
    "നവംബർ",
    "ഡിസംബർ",
)

# verify with a native speaker: time-of-day words
_MORNING = "രാവിലെ"
_NOON = "ഉച്ചയ്ക്ക്"
_EVENING = "വൈകുന്നേരം"
_NIGHT = "രാത്രി"
_HOUR_WORD = "മണി"
_MINUTE_WORD = "മിനിറ്റ്"

_DATE_RE = re.compile(
    r"(?<![\d/.\-])(\d{1,2})([/-])(\d{1,2})\2(\d{4})(?!\d)(?![/-]\d)"
)
_TIME_RE = re.compile(
    r"(?<![\d:])(\d{1,2}):(\d{2})"
    r"(?:\s*([AaPp])\.?[Mm]\.?(?![A-Za-z]))?"
    r"(?![\d:])"
)


def _date_repl(m: re.Match[str]) -> str:
    day, month, year = int(m.group(1)), int(m.group(3)), int(m.group(4))
    if year < 1000:
        return m.group(0)
    try:
        datetime.date(year, month, day)
    except ValueError:
        return m.group(0)
    return f"{spell_number(str(day))} {MONTHS[month - 1]} {spell_number(str(year))}"


def _time_repl(m: re.Match[str]) -> str:
    hour, minute = int(m.group(1)), int(m.group(2))
    meridiem = m.group(3)
    if minute > 59:
        return m.group(0)

    period = ""
    if meridiem:
        if not 1 <= hour <= 12:
            return m.group(0)
        if meridiem in "Aa":
            period = _NIGHT if hour == 12 else _MORNING
        else:
            period = _NOON if hour == 12 else _EVENING
    elif hour > 23:
        return m.group(0)

    parts = [period] if period else []
    parts.append(f"{number_to_words(hour)} {_HOUR_WORD}")
    if minute:
        parts.append(f"{number_to_words(minute)} {_MINUTE_WORD}")
    return " ".join(parts)


def convert_dates(text: str) -> str:
    """'15/08/2026' -> 'പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ്'."""
    return _DATE_RE.sub(_date_repl, text)


def convert_times(text: str) -> str:
    """'14:30' -> 'പതിനാല് മണി മുപ്പത് മിനിറ്റ്'."""
    return _TIME_RE.sub(_time_repl, text)
