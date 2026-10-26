# Bank Account Management System

A command-line Python project for creating and managing sample bank-account records stored in a local JSON file. Available operations include account creation, deposits, withdrawals, viewing or updating account details, and account deletion.

## Project files

- `Bank_management.py` — original interactive implementation.
- `streamlit.py` — a later cleaned-up rewrite of the command-line app with input-validation helpers.
- `data.json` — local JSON data file used by the app.

## Run locally

Python 3 is required. The scripts use Python's standard library, so no package installation is needed.

Run the cleaned-up implementation from the repository directory:

```bash
python streamlit.py
```

To run the original implementation instead:

```bash
python Bank_management.py
```

The program reads and writes `data.json` in the current working directory. Use sample data only; this educational project is not suitable for real financial or personal information.

## Note

The `streamlit.py` filename does not indicate a Streamlit web interface; the file contains an interactive command-line application.
