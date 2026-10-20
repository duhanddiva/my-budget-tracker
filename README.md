# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

Prerequisite: install `uv` if you don't already have it.

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Sync the dependencies

   ```
   $ uv sync
   ```

2. Run the app

   ```
   $ uv run streamlit run streamlit_app.py
   ```

### Managing authorized users

Add an authorized account from the project directory:

```
$ uv run python manage_users.py alice
```

The command prompts for a password and confirmation, then stores a salted
password hash in `users.json`. The file is local and ignored by Git; create
accounts on the machine where the app runs. Do not store plain-text passwords
in the file or commit it. This local file-based setup is intended for a
single-host app, not production or multi-instance authentication.
