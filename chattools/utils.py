#!/usr/bin/env python3

from openai import OpenAI, OpenAIError


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


HISTORY_FOLDER = Path(__file__).resolve().parent / 'history'
ROLES_PATH = Path(__file__).resolve().parent / 'roles.yml'
CHAT_PATH = Path('~/Programming/Python/mywork/chattools').expanduser()

def read_yaml(roles_path=ROLES_PATH):
    if isinstance(roles_path, str): roles_path = Path(roles_path)
    if not roles_path.exists():
        raise FileNotFoundError(f"The file {roles_path} does not exist.")
    with open(roles_path, 'r', encoding='utf - 8') as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    return data


def menu(roles):
    from fuzzywuzzy import fuzz

    print('System: please select one role from the following menu:')
    print('    -------------')
    for role, description in roles.items():
        print(f"{role:>16}: {description}")
    print('    -------------')
    r = input("User: ")
    role = max(roles.keys(), key=lambda x: fuzz.ratio(r, x))
    print(f"System: you select {role}.")
    return role, roles[role]


def get_api_key(model):
    from dotenv import dotenv_values
    config = dotenv_values(CHAT_PATH/".env.key")
    return config.get(f'{model.upper()}_API_KEY', '')

