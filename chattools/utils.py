#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from mixin import ChatMixin


def convert(v):
    if v in {'False', 'True'}:
        return bool(v)
    elif v == 'None':
        return None
    elif '.' in v:
        return float(v)
    elif v.isdigit():
        return int(v)
    else:
        raise TypeError(f'The input `{v}` should be False/True/None or a number!')


import yaml
from pathlib import Path

ROLES_PATH = Path(__file__).resolve().parent / 'roles.yml'

def read_yaml(roles_path=ROLES_PATH):
    if isinstance(roles_path, str): roles_path = Path(roles_path)
    if not roles_path.exists():
        raise FileNotFoundError(f"The file {roles_path} does not exist.")
    with open(roles_path, 'r', encoding='utf - 8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    return data


def menu(roles):
    print('System: please select one role from the following menu:')
    print('    -------------')
    for role, description in roles.items():
        print(f"{role:>16}: {description}")
    print('    -------------')
    r = input("User: ")

    for role, description in roles.items():
        if role.startswith(r):
            break
    return role, description

