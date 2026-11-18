import unicodedata

import pytest

from malayalam_normaliser import normalise

PIPELINE_CASES = [
    # abbreviations
    ("Dr. Rao", "ഡോക്ടർ Rao"),
    ("5 km", "അഞ്ച് കിലോമീറ്റർ"),
    ("500ml", "അഞ്ഞൂറ് മില്ലിലിറ്റർ"),
    ("2.5 kg", "രണ്ട് പോയിന്റ് അഞ്ച് കിലോഗ്രാം"),
    ("No. 12", "നമ്പർ പന്ത്രണ്ട്"),
    ("A & B", "A ആൻഡ് B"),
    # numbers and symbols inside Malayalam sentences
    ("ഞാൻ 2 പുസ്തകങ്ങൾ വാങ്ങി", "ഞാൻ രണ്ട് പുസ്തകങ്ങൾ വാങ്ങി"),
    ("യോഗം 14:30", "യോഗം പതിനാല് മണി മുപ്പത് മിനിറ്റ്"),
    (
        "ഇന്ന് 15/08/2026 ആണ്",
        "ഇന്ന് പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ് ആണ്",
    ),
    (
        "15/08/2026 10:30",
        "പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ് പത്ത് മണി മുപ്പത് മിനിറ്റ്",
    ),
    ("താപനില -5 ആയിരുന്നു", "താപനില മൈനസ് അഞ്ച് ആയിരുന്നു"),
    ("ദൂരം 45% കൂടി", "ദൂരം നാൽപ്പത്തിയഞ്ച് ശതമാനം കൂടി"),
    # invalid date stays unchanged, including its digits
    ("31/02/2026", "31/02/2026"),
    # plain Malayalam is untouched
    ("മലയാളം", "മലയാളം"),
    ("", ""),
]


@pytest.mark.parametrize("text, expected", PIPELINE_CASES)
def test_pipeline(text, expected):
    assert normalise(text) == expected


def test_zwj_is_preserved():
    text = "മലയാളം‍സ"
    assert normalise(text) == text


def test_zwnj_is_preserved():
    text = "മലയാളം‌സ"
    assert normalise(text) == text


def test_chillu_characters_are_preserved():
    text = "ഞാൻ വരും, മരം, പെൺകുട്ടി"
    assert normalise(text) == text


def test_output_is_nfc():
    decomposed = "ൊ"  # vowel sign e + vowel sign aa
    result = normalise(decomposed)
    assert result == unicodedata.normalize("NFC", decomposed)
    assert result == "ൊ"


def test_non_string_rejected():
    with pytest.raises(TypeError):
        normalise(123)
