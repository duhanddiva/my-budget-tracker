import hashlib
import hmac
import json
import os
import secrets
import tempfile
from pathlib import Path

USERS_FILE = Path(__file__).with_name("users.json")
SCRYPT_N = 2**14


def create_password_record(password: str) -> dict[str, str]:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=8,
        p=1,
        dklen=32,
    )
    return {"salt": salt.hex(), "password_hash": password_hash.hex()}


def load_users() -> dict[str, dict[str, str]]:
    if not USERS_FILE.exists():
        return {}

    data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("users.json must contain a JSON object.")

    users: dict[str, dict[str, str]] = {}
    for username, record in data.items():
        if (
            not isinstance(username, str)
            or not username
            or not isinstance(record, dict)
            or not isinstance(record.get("salt"), str)
            or not isinstance(record.get("password_hash"), str)
        ):
            raise ValueError("Each user must have a username, salt, and password_hash.")
        try:
            salt = bytes.fromhex(record["salt"])
            password_hash = bytes.fromhex(record["password_hash"])
        except ValueError as error:
            raise ValueError(f"Invalid password data for user {username!r}.") from error
        if len(salt) != 16 or len(password_hash) != 32:
            raise ValueError(f"Invalid password data for user {username!r}.")
        users[username] = record
    return users


def save_users(users: dict[str, dict[str, str]]) -> None:
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=USERS_FILE.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(users, temporary_file, indent=2)
            temporary_file.write("\n")
        os.chmod(temporary_path, 0o600)
        temporary_path.replace(USERS_FILE)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def verify_password(password: str, record: dict[str, str]) -> bool:
    expected_hash = bytes.fromhex(record["password_hash"])
    actual_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=bytes.fromhex(record["salt"]),
        n=SCRYPT_N,
        r=8,
        p=1,
        dklen=32,
    )
    return hmac.compare_digest(actual_hash, expected_hash)
