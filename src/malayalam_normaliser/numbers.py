"""Number-to-words conversion for Malayalam, using Indian digit grouping.

Scale words: ആയിരം (thousand), ലക്ഷം (lakh = 10^5), കോടി (crore = 10^7).
A value is split as: crore part (0-99), lakh part (0-99), thousand part
(0-99), and the last three digits (0-999). Maximum: 99,99,99,999.

All word lists below were written from memory. They have NOT been checked
by a native speaker. See README "Known uncertainties".
"""

from __future__ import annotations

import re

MAX_VALUE = 999_999_999  # 99,99,99,999 in Indian grouping

# verify with a native speaker
DIGIT_WORDS = (
    "പൂജ്യം",
    "ഒന്ന്",
    "രണ്ട്",
    "മൂന്ന്",
    "നാല്",
    "അഞ്ച്",
    "ആറ്",
    "ഏഴ്",
    "എട്ട്",
    "ഒമ്പത്",
)

# verify with a native speaker: 10-19
_TEENS = {
    10: "പത്ത്",
    11: "പതിനൊന്ന്",
    12: "പന്ത്രണ്ട്",
    13: "പതിമൂന്ന്",
    14: "പതിനാല്",
    15: "പതിനഞ്ച്",
    16: "പതിനാറ്",
    17: "പതിനേഴ്",
    18: "പതിനെട്ട്",
    19: "പത്തൊമ്പത്",
}

# verify with a native speaker: tens words on their own (20, 30, ...)
_TENS = {
    2: "ഇരുപത്",
    3: "മുപ്പത്",
    4: "നാൽപ്പത്",
    5: "അമ്പത്",
    6: "അറുപത്",
    7: "എഴുപത്",
    8: "എൺപത്",
    9: "തൊണ്ണൂറ്",
}

# verify with a native speaker: tens words followed by a unit (21-99)
_TENS_BEFORE_UNIT = {
    2: "ഇരുപത്തി",
    3: "മുപ്പത്തി",
    4: "നാൽപ്പത്തി",
    5: "അമ്പത്തി",
    6: "അറുപത്തി",
    7: "എഴുപത്തി",
    8: "എൺപത്തി",
    9: "തൊണ്ണൂറ്റി",
}

# verify with a native speaker: unit forms that follow a tens word
_UNIT_AFTER_TENS = {
    1: "യൊന്ന്",
    2: "രണ്ട്",
    3: "മൂന്ന്",
    4: "നാല്",
    5: "യഞ്ച്",
    6: "യാറ്",
    7: "യേഴ്",
    8: "യെട്ട്",
    9: "യൊമ്പത്",
}

# verify with a native speaker: hundreds on their own
_HUNDREDS = {
    1: "നൂറ്",
    2: "ഇരുനൂറ്",
    3: "മുന്നൂറ്",
    4: "നാനൂറ്",
    5: "അഞ്ഞൂറ്",
    6: "അറുനൂറ്",
    7: "എഴുനൂറ്",
    8: "എണ്ണൂറ്",
    9: "തൊള്ളായിരം",
}

# verify with a native speaker: hundreds followed by more digits
_HUNDREDS_BEFORE_REST = {
    1: "നൂറ്റി",
    2: "ഇരുനൂറ്റി",
    3: "മുന്നൂറ്റി",
    4: "നാനൂറ്റി",
    5: "അഞ്ഞൂറ്റി",
    6: "അറുനൂറ്റി",
    7: "എഴുനൂറ്റി",
    8: "എണ്ണൂറ്റി",
    9: "തൊള്ളായിരത്തി",
}

# verify with a native speaker: contracted thousand multipliers.
# Multipliers 10-99 not listed here fall back to "<tens word> ആയിരം"
# (for example 25000 -> "ഇരുപത്തിയഞ്ച് ആയിരം").
_THOUSAND_MULTIPLIERS = {
    2: "രണ്ടായിരം",
    3: "മൂവായിരം",
    4: "നാലായിരം",
    5: "അയ്യായിരം",
    6: "ആറായിരം",
    7: "ഏഴായിരം",
    8: "എട്ടായിരം",
    9: "ഒമ്പതിനായിരം",
    10: "പതിനായിരം",
    20: "ഇരുപതിനായിരം",
    30: "മുപ്പതിനായിരം",
    40: "നാൽപ്പതിനായിരം",
    50: "അമ്പതിനായിരം",
    60: "അറുപതിനായിരം",
    70: "എഴുപതിനായിരം",
    80: "എൺപതിനായിരം",
    90: "തൊണ്ണൂറായിരം",
}


def _two_digit(n: int) -> str:
    """Words for 1-99."""
    if n < 10:
        return DIGIT_WORDS[n]
    if n < 20:
        return _TEENS[n]
    tens, unit = divmod(n, 10)
    if unit == 0:
        return _TENS[tens]
    return _TENS_BEFORE_UNIT[tens] + _UNIT_AFTER_TENS[unit]


def _below_thousand(n: int) -> str:
    """Words for 1-999."""
    hundreds, rest = divmod(n, 100)
    if hundreds == 0:
        return _two_digit(rest)
    if rest == 0:
        return _HUNDREDS[hundreds]
    return f"{_HUNDREDS_BEFORE_REST[hundreds]} {_two_digit(rest)}"


def _link(word: str) -> str:
    """Turn a scale word ending in 'ം' into its linked form ('...ത്തി')."""
    return word[:-1] + "ത്തി"


def _thousands_phrase(n: int, linked: bool) -> str:
    if n == 1:
        base = "ആയിരം"
    elif n in _THOUSAND_MULTIPLIERS:
        base = _THOUSAND_MULTIPLIERS[n]
    else:
        base = f"{_two_digit(n)} ആയിരം"
    return _link(base) if linked else base


def _lakhs_phrase(n: int, linked: bool) -> str:
    base = "ഒരു ലക്ഷം" if n == 1 else f"{_two_digit(n)} ലക്ഷം"
    return _link(base) if linked else base


def _crores_phrase(n: int) -> str:
    return "ഒരു കോടി" if n == 1 else f"{_two_digit(n)} കോടി"


def _join(first: str, rest: str) -> str:
    return f"{first} {rest}" if rest else first


def number_to_words(value: int) -> str:
    """Read an integer in the range 0..99,99,99,999 in Malayalam words."""
    if not 0 <= value <= MAX_VALUE:
        raise ValueError(f"value out of range: {value}")
    if value == 0:
        return DIGIT_WORDS[0]

    words = _below_thousand(value % 1000) if value % 1000 else ""

    thousands = (value // 1000) % 100
    if thousands:
        words = _join(_thousands_phrase(thousands, bool(words)), words)

    lakhs = (value // 100_000) % 100
    if lakhs:
        words = _join(_lakhs_phrase(lakhs, bool(words)), words)

    crores = value // 10_000_000
    if crores:
        words = _join(_crores_phrase(crores), words)

    return words


def digits_to_words(digits: str) -> str:
    """Read each digit separately: '2026' -> 'രണ്ട് പൂജ്യം ...'."""
    return " ".join(DIGIT_WORDS[int(ch)] for ch in digits)


def spell_number(int_text: str, dec_text: str | None = None) -> str:
    """Spell an integer part (commas allowed) with an optional decimal part.

    Leading zeros (for example '007') and values above MAX_VALUE are read
    digit by digit, so no digits are silently dropped.
    """
    digits = int_text.replace(",", "")
    if (len(digits) > 1 and digits[0] == "0") or int(digits) > MAX_VALUE:
        spoken = digits_to_words(digits)
    else:
        spoken = number_to_words(int(digits))
    if dec_text is not None:
        spoken = f"{spoken} പോയിന്റ് {digits_to_words(dec_text)}"
    return spoken


# A number may not touch letters, Malayalam characters, or other number
# punctuation such as 10-12, 1:2, 31/02/2026, 1,2,3. Those are left alone.
_LEFT = r"(?<![0-9A-Za-zഀ-ൿ])(?<!\d[.,/:\-])"
_RIGHT = (
    r"(?![0-9ഀ-ൿ])"
    r"(?!(?![Kk][Mm]\b|[Kk][Gg]\b|[Mm][Ll]\b)[A-Za-z])"  # allow km, kg, ml
    r"(?![.,/:\-]\d)"
)
_BODY = (
    r"(-?)"  # 1: optional minus sign
    r"((?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})*,\d{3}|\d+))"  # 2: integer part
    r"(?:\.(\d+))?"  # 3: decimal part
)
_NUMBER_RE = re.compile(_LEFT + _BODY + _RIGHT)
_PERCENT_RE = re.compile(_LEFT + _BODY + r"\s?%")


def _spoken_from_match(m: re.Match[str]) -> str:
    spoken = spell_number(m.group(2), m.group(3))
    if m.group(1):
        spoken = f"മൈനസ് {spoken}"
    return spoken


def _number_repl(m: re.Match[str]) -> str:
    spoken = _spoken_from_match(m)
    end = m.end()
    # keep a space before a unit such as 'km' that follows directly
    if end < len(m.string) and m.string[end].isascii() and m.string[end].isalpha():
        spoken += " "
    return spoken


def _percent_repl(m: re.Match[str]) -> str:
    return f"{_spoken_from_match(m)} ശതമാനം"


def convert_percentages(text: str) -> str:
    """'45%' -> 'നാൽപ്പത്തിയഞ്ച് ശതമാനം'."""
    return _PERCENT_RE.sub(_percent_repl, text)


def convert_numbers(text: str) -> str:
    """Convert every standalone number in text, in place."""
    return _NUMBER_RE.sub(_number_repl, text)
