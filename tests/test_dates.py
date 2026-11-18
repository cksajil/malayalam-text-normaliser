import pytest

from malayalam_normaliser.dates import convert_dates, convert_times
from malayalam_normaliser.normalise import normalise

DATE_CASES = [
    ("15/08/2026", "പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ്"),
    ("15-08-2026", "പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ്"),
    ("01/01/2000", "ഒന്ന് ജനുവരി രണ്ടായിരം"),
    ("29/02/2024", "ഇരുപത്തിയൊമ്പത് ഫെബ്രുവരി രണ്ടായിരത്തി ഇരുപത്തിനാല്"),
    ("5/8/2026", "അഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ്"),
]

INVALID_DATES = [
    "31/02/2026",  # February has no 31st
    "29/02/2026",  # 2026 is not a leap year
    "15/13/2026",  # no 13th month
    "00/05/2026",  # no day 0
]

TIME_CASES = [
    ("14:30", "പതിനാല് മണി മുപ്പത് മിനിറ്റ്"),
    ("09:05", "ഒമ്പത് മണി അഞ്ച് മിനിറ്റ്"),
    ("10:00", "പത്ത് മണി"),
    ("2:30 pm", "വൈകുന്നേരം രണ്ട് മണി മുപ്പത് മിനിറ്റ്"),
    ("9:15am", "രാവിലെ ഒമ്പത് മണി പതിനഞ്ച് മിനിറ്റ്"),
    ("12:00 pm", "ഉച്ചയ്ക്ക് പന്ത്രണ്ട് മണി"),
]

INVALID_TIMES = ["25:00", "13:00 am", "10:60"]


@pytest.mark.parametrize("text, expected", DATE_CASES)
def test_valid_dates(text, expected):
    assert convert_dates(text) == expected


@pytest.mark.parametrize("text", INVALID_DATES)
def test_invalid_dates_unchanged(text):
    assert normalise(text) == text


@pytest.mark.parametrize("text, expected", TIME_CASES)
def test_times(text, expected):
    assert convert_times(text) == expected


@pytest.mark.parametrize("text", INVALID_TIMES)
def test_invalid_times_unchanged(text):
    assert normalise(text) == text
