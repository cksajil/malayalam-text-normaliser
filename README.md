# malayalam-text-normaliser

A small, pure-Python package that turns written Malayalam and mixed Malayalam/English text into the form a speech system should read aloud (TTS), or compare against (ASR evaluation).

- No runtime dependencies, no model downloads, no network access.
- Python 3.10+.
- Numbers, currency, dates, times, percentages, a fixed abbreviation table, and NFC normalisation.
- Out of scope: Manglish transliteration, spelling correction, sandhi rules, ML models, APIs.

**The Malayalam word lists were written from memory and have not been checked by a native speaker.** Each list is marked `# verify with a native speaker` in the code. See [Known uncertainties](#known-uncertainties).

## Examples

| Input | Output |
|---|---|
| `₹1500` | `ആയിരത്തി അഞ്ഞൂറ് രൂപ` |
| `Rs 12.50` | `പന്ത്രണ്ട് രൂപ അമ്പത് പൈസ` |
| `ഇന്ന് 15/08/2026 ആണ്` | `ഇന്ന് പതിനഞ്ച് ഓഗസ്റ്റ് രണ്ടായിരത്തി ഇരുപത്തിയാറ് ആണ്` |
| `യോഗം 14:30` | `യോഗം പതിനാല് മണി മുപ്പത് മിനിറ്റ്` |
| `2:30 pm` | `വൈകുന്നേരം രണ്ട് മണി മുപ്പത് മിനിറ്റ്` |
| `45%` | `നാൽപ്പത്തിയഞ്ച് ശതമാനം` |
| `3.14` | `മൂന്ന് പോയിന്റ് ഒന്ന് നാല്` |
| `-5` | `മൈനസ് അഞ്ച്` |
| `1,00,00,000` | `ഒരു കോടി` |
| `31/02/2026` | `31/02/2026` (invalid date, unchanged) |
| `Dr. Rao` | `ഡോക്ടർ Rao` |
| `5 km` | `അഞ്ച് കിലോമീറ്റർ` |

## Install

```bash
pip install .
```

For development (adds pytest):

```bash
pip install ".[dev]"
```

## Usage

```python
from malayalam_normaliser import normalise

normalise("ഞാൻ 2 പുസ്തകങ്ങൾ വാങ്ങി")
# 'ഞാൻ രണ്ട് പുസ്തകങ്ങൾ വാങ്ങി'
```

`normalise(text: str) -> str` is the only public function.

## What it does

The pipeline runs in this order. The order matters, because currency and dates must be read before the bare number step sees their digits.

1. **Currency**: `₹`, `Rs`, `Rs.`, `INR` before an amount. Paise are read for two-digit decimals.
2. **Dates**: `dd/mm/yyyy` and `dd-mm-yyyy`, read as day, month name, year. Invalid dates are left unchanged (leap years are checked).
3. **Times**: `hh:mm` (24-hour) and `h:mm am/pm` (12-hour).
4. **Percentages**: `45%` becomes `... ശതമാനം`.
5. **Numbers**: integers up to 99,99,99,999 with Indian grouping (ആയിരം, ലക്ഷം, കോടി). Decimals are read digit by digit after `പോയിന്റ്`. A minus sign becomes `മൈനസ്`. Commas are accepted in both Indian (`1,00,000`) and Western (`1,000,000`) grouping.
6. **Abbreviations**: the table in `src/malayalam_normaliser/abbreviations.py`, one entry per line.
7. **Unicode**: the output is NFC-normalised. Chillu characters, ZWJ and ZWNJ are kept as they appear in the input.

Text that is not a number, date, time, currency amount or listed abbreviation is not changed. Mixed text is converted in place.

## Behaviour choices

- Leading zeros (`007`) and integers above 999,999,999 are read digit by digit, so no digits are dropped.
- Numbers joined to other numbers with `-`, `/`, `:`, `.` or `,` (such as `10-12`, `1:2`, `1,2,3`) are left unchanged. This keeps dates and times intact, but it also means ranges are not expanded.
- `5km`, `500ml` and `2 kg` convert the number and expand the unit.
- A minus sign only counts at the start of a token or after a space, so `10-12` is not read as "ten minus twelve".

## Running the tests on Kaggle

Tests and sample runs happen on Kaggle, not locally. The Kaggle notebook clones this repository from GitHub (`main`), installs it, runs pytest, and prints the sample table. Push your changes to `main` before you push the Kaggle kernel.

Requirements: the Kaggle CLI, with an API token in `~/.kaggle/kaggle.json` or the environment. Never commit the token.

```bash
kaggle config view
kaggle kernels push -p kaggle/
kaggle kernels status <kaggle-username>/malayalam-normaliser-tests
kaggle kernels output <kaggle-username>/malayalam-normaliser-tests -p kaggle/output/
```

`kaggle/output/` is git-ignored. The log in that folder holds the pytest output and the sample table.

## Repository layout

```
src/malayalam_normaliser/   the package (numbers, dates, currency, abbreviations, normalise)
tests/                      pytest suite
notebooks/                  Kaggle notebook (same file as kaggle/)
kaggle/                     kernel-metadata.json and the notebook for `kaggle kernels push`
```

## Known uncertainties

These are choices I made without a native-speaker check. Please review them before relying on the output for production TTS or evaluation.

- **Spelling of 40 and 50**: I used `നാൽപ്പത്` and `അമ്പത്`. Other forms, `നാല്പത്` and `അൻപത്`, are also in use.
- **Tens before a unit**: I used the full form, for example `ഇരുപത്തിയഞ്ച്` (25), `നാൽപ്പത്തിയഞ്ച്` (45). Contracted forms such as `ഇരുപത്തഞ്ച്` are also common.
- **Thousand multipliers 10-99 not in the table**: 25000 becomes `ഇരുപത്തിയഞ്ച് ആയിരം`. Contracted forms such as `ഇരുപത്തയ്യായിരം` are not generated.
- **Linking words**: `ആയിരത്തി` and `ലക്ഷത്തി` are used before the rest of the number. `കോടി` is followed by a space, with no linker.
- **Hundreds for 9xx**: 900 is `തൊള്ളായിരം` and 950 is `തൊള്ളായിരത്തി അഞ്ഞൂറ്`.
- **Years**: a year such as 2026 is read as a full number (`രണ്ടായിരത്തി ഇരുപത്തിയാറ്`), not as two pairs.
- **Times of day**: `രാവിലെ` for am, `വൈകുന്നേരം` for pm, `ഉച്ചയ്ക്ക്` for 12 pm, and `രാത്രി` for 12 am. Hour and minute words are added with `മണി` and `മിനിറ്റ്`.
- **Month names**: standard Malayalam month names are used. `മേയ്` is used for May.
- **Abbreviation spellings**: `ഡോക്ടർ`, `മിസ്റ്റർ`, `മിസിസ്`, `ലിമിറ്റഡ്`, `കിലോമീറ്റർ`, `കിലോഗ്രാം`, `മില്ലിലിറ്റർ`, `നമ്പർ`, and `ആൻഡ്` for `&`. Each could be a different transliteration.
- **Paise**: `പൈസ` is used for the paise part of a rupee amount. Amounts with three or more decimal places read the decimals with `പോയിന്റ്` instead.
- **Digits read one by one**: a leading-zero number such as `007` is read `പൂജ്യം പൂജ്യം ഏഴ്`. Some speakers read `007` as "ഏഴ്". Choose the policy that suits your data.

## Limits

- Only Indian and Western comma grouping and plain digit strings are recognised. Other separators (spaces, `.` as a thousands separator) are not.
- Dates are only `dd/mm/yyyy` and `dd-mm-yyyy` with a four-digit year. Other formats are left unchanged.
- Times are only `hh:mm` with an optional am/pm. Seconds are not read.
- Ordinal forms (`5ാം`, `1st`) are not converted.
- Abbreviations are a fixed table. Unknown abbreviations are passed through unchanged.
- Negative currency amounts are not handled.
