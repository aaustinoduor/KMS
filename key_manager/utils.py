import os
from uuid import uuid4, UUID
from bcrypt import hashpw, checkpw, gensalt


def hash_password(password: str) -> str:
    salt = gensalt()
    return hashpw(password.encode(), salt).decode()


def check_password(pass_hash: str, password: str) -> bool:
    return checkpw(password.encode(), pass_hash.encode())


def gen_uuid():
    """"""
    return uuid4()


def str_to_uuid(uuid: str) -> UUID:
    """"""
    return UUID(uuid)


def find_file(name, path):
    """"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)