import pytest

from malayalam_normaliser.currency import convert_currency
from malayalam_normaliser.normalise import normalise

CURRENCY_CASES = [
    ("₹1500", "ആയിരത്തി അഞ്ഞൂറ് രൂപ"),
    ("Rs 1500", "ആയിരത്തി അഞ്ഞൂറ് രൂപ"),
    ("Rs.100", "നൂറ് രൂപ"),
    ("INR 10", "പത്ത് രൂപ"),
    ("₹1,50,000", "ഒരു ലക്ഷത്തി അമ്പതിനായിരം രൂപ"),
    ("₹12.50", "പന്ത്രണ്ട് രൂപ അമ്പത് പൈസ"),
    ("₹12.5", "പന്ത്രണ്ട് രൂപ അമ്പത് പൈസ"),
    ("₹12.00", "പന്ത്രണ്ട് രൂപ"),
]


@pytest.mark.parametrize("text, expected", CURRENCY_CASES)
def test_currency_prefix_forms(text, expected):
    assert convert_currency(text) == expected


@pytest.mark.parametrize("text, expected", CURRENCY_CASES)
def test_currency_through_pipeline(text, expected):
    assert normalise(text) == expected


def test_malayalam_rupee_suffix_converts_number_only():
    assert normalise("1500 രൂപ") == "ആയിരത്തി അഞ്ഞൂറ് രൂപ"


def test_currency_inside_sentence():
    assert normalise("ഇന്ന് ₹1500 ചെലവ്") == "ഇന്ന് ആയിരത്തി അഞ്ഞൂറ് രൂപ ചെലവ്"


def test_rs_without_amount_becomes_rupee_word():
    assert normalise("Rs") == "രൂപ"
