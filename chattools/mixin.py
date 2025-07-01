#!/usr/bin/env python3

import pathlib
import yaml


def _clear(obj):
    obj.history = []
    print(f'System: The history is cleared.')


def _save(obj):
    if history_file.exists():
        print("The available history file will be covered!")
    history_file.write_text(yaml.dump(obj.history, allow_unicode=True))

def _load(obj):
    if history_file.exists():
        obj.history = yaml.safe_load(str(history_file))
    else:
        print('No history is loaded!')


commands = {
  "clear": _clear,
  "load": _load,
  "save": _save
}


class ChatMixin:

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, v):
        self._history = v

    def execute(self, *args, **kwargs):
        # call python compiler
        return exec(*args, **kwargs)

    def init(self, description=None):
        description = description or self.description
        if description is not None:
            message = {"role": "system", "content": description}
            self.history.insert(0, message)

    def run(self, description=None):
        # To chat with deepseek
        self.init(description=description)

        history_file = pathlib.Path('history.yaml')

        while True:
            user_input = input("User: ")
            if user_input in {'exit', 'quit', 'bye'}:
                print(f'{self.name}: Bye.')
                break
            elif user_input.startswith('>'):
                self.execute(user_input[1:])
            elif user_input.startswith('!'):
                commands[user_input[1:].strip()](self)
            elif user_input.startswith('#'):
                a, v = user_input[1:].split()
                setattr(self, a, v)
                print(f'System: The attribute `{a}` is set to be `{v}`.')
            else:
                self._reply(user_input)

    def demo(self):
        self.init()
        for p in prompts:
            print(f"User: {p}")
            self._reply(p)

