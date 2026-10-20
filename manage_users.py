import argparse
from getpass import getpass

from auth_utils import create_password_record, load_users, save_users


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage authorized budget tracker users.")
    parser.add_argument("username", help="Username to add or update")
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update an existing user's password instead of adding a user",
    )
    parser.add_argument(
        "--new-username",
        help="Rename the user while updating their password",
    )
    args = parser.parse_args()

    username = args.username.strip()
    if not username:
        parser.error("username cannot be empty")
    if args.new_username is not None and not args.update:
        parser.error("--new-username can only be used with --update")

    new_username = args.new_username.strip() if args.new_username is not None else username
    if not new_username:
        parser.error("new username cannot be empty")

    users = load_users()
    if args.update:
        if username not in users:
            parser.error(f"user {username!r} is not authorized")
        if new_username != username and new_username in users:
            parser.error(f"user {new_username!r} is already authorized")
    elif username in users:
        parser.error(f"user {username!r} is already authorized")

    password = getpass("Password: ")
    confirmation = getpass("Confirm password: ")
    if not password:
        parser.error("password cannot be empty")
    if password != confirmation:
        parser.error("passwords do not match")

    if args.update:
        del users[username]

    users[new_username] = create_password_record(password)
    save_users(users)
    if args.update:
        print(f"Updated authorized account {username!r} as {new_username!r} in users.json.")
    else:
        print(f"Authorized {new_username!r} in users.json.")


if __name__ == "__main__":
    main()
