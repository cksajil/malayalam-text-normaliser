import pytest

from malayalam_normaliser.numbers import (
    convert_numbers,
    convert_percentages,
    number_to_words,
    spell_number,
)

WORD_CASES = [
    (0, "പൂജ്യം"),
    (1, "ഒന്ന്"),
    (10, "പത്ത്"),
    (11, "പതിനൊന്ന്"),
    (21, "ഇരുപത്തിയൊന്ന്"),
    (45, "നാൽപ്പത്തിയഞ്ച്"),
    (99, "തൊണ്ണൂറ്റിയൊമ്പത്"),
    (100, "നൂറ്"),
    (101, "നൂറ്റി ഒന്ന്"),
    (500, "അഞ്ഞൂറ്"),
    (900, "തൊള്ളായിരം"),
    (1000, "ആയിരം"),
    (1001, "ആയിരത്തി ഒന്ന്"),
    (1500, "ആയിരത്തി അഞ്ഞൂറ്"),
    (2000, "രണ്ടായിരം"),
    (100000, "ഒരു ലക്ഷം"),
    (1000000, "പത്ത് ലക്ഷം"),
    (10000000, "ഒരു കോടി"),
    (
        999999999,
        "തൊണ്ണൂറ്റിയൊമ്പത് കോടി തൊണ്ണൂറ്റിയൊമ്പത് ലക്ഷത്തി "
        "തൊണ്ണൂറ്റിയൊമ്പത് ആയിരത്തി തൊള്ളായിരത്തി തൊണ്ണൂറ്റിയൊമ്പത്",
    ),
]


@pytest.mark.parametrize("value, expected", WORD_CASES)
def test_number_to_words(value, expected):
    assert number_to_words(value) == expected


def test_out_of_range_rejected():
    with pytest.raises(ValueError):
        number_to_words(1_000_000_000)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("3.14", "മൂന്ന് പോയിന്റ് ഒന്ന് നാല്"),
        ("0.5", "പൂജ്യം പോയിന്റ് അഞ്ച്"),
        ("-5", "മൈനസ് അഞ്ച്"),
        ("1,00,000", "ഒരു ലക്ഷം"),
        ("1,000,000", "പത്ത് ലക്ഷം"),
        ("007", "പൂജ്യം പൂജ്യം ഏഴ്"),
        ("1000000000", "ഒന്ന് " + " ".join(["പൂജ്യം"] * 9)),
    ],
)
def test_convert_numbers_in_text(text, expected):
    assert convert_numbers(text) == expected


def test_spell_number_leading_zero_is_digit_by_digit():
    assert spell_number("007") == "പൂജ്യം പൂജ്യം ഏഴ്"


def test_hyphen_between_numbers_is_not_minus():
    # Ranges such as 10-12 are left unchanged; the hyphen is not a minus sign.
    assert convert_numbers("10-12") == "10-12"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("45%", "നാൽപ്പത്തിയഞ്ച് ശതമാനം"),
        ("12.5%", "പന്ത്രണ്ട് പോയിന്റ് അഞ്ച് ശതമാനം"),
        ("-5%", "മൈനസ് അഞ്ച് ശതമാനം"),
    ],
)
def test_percentages(text, expected):
    assert convert_percentages(text) == expected
