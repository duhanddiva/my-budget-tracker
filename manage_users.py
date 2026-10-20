import argparse
from getpass import getpass

from auth_utils import create_password_record, load_users, save_users


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage authorized budget tracker users.")
    parser.add_argument("username", help="Username to authorize")
    args = parser.parse_args()

    username = args.username.strip()
    if not username:
        parser.error("username cannot be empty")

    password = getpass("Password: ")
    confirmation = getpass("Confirm password: ")
    if not password:
        parser.error("password cannot be empty")
    if password != confirmation:
        parser.error("passwords do not match")

    users = load_users()
    if username in users:
        parser.error(f"user {username!r} is already authorized")

    users[username] = create_password_record(password)
    save_users(users)
    print(f"Authorized {username!r} in users.json.")


if __name__ == "__main__":
    main()
