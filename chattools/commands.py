#!/usr/bin/env python3

import pathlib
import yaml


history_file = pathlib.Path('history.yaml')


class Commands:

    # the first argument should be the object of AI-chat

    def clear(obj):
        obj.history = []
        print(f'💻System: The history is cleared.')

    def save(obj):
        if not history_file.exists():     
            print("💻System: The history is stored in {history_file}!")
            history_file.write_text(yaml.dump(obj.history, allow_unicode=True))
        else:
            print("💻System: {history_file} is available! The history will not be stored")

    def load(obj):
        if history_file.exists():
            print('💻System: The history is loaded from {history_file}!')
            obj.history = yaml.safe_load(str(history_file))
        else:
            print('💻System: No history is loaded!')


def cmd(name=None):

    def dec(f):
        name = name or f.__name__
        setattr(Commands, name, f)
    return dec