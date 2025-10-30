#!/usr/bin/env python3

import pathlib
import yaml


history_file = pathlib.Path('history.yaml')


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
        # To chat with AI
        self.init(description=description)

        while True:
            user_input = input("User: ")
            if user_input.lower() in {'exit', 'quit', 'bye'}:
                print(f'{self.name}: Bye.')
                break
            self.reply(user_input)
            self.post_process()

    def post_process(self):
        max_len = 20
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

    def demo(self):
        self.init()
        for p in prompts:
            print(f"User: {p}")
            self.reply(p)

    def reply(self, user_input, n_loop=100):
        """The reply of the AI chat assistant
        """
        if user_input.startswith(':'):
            a, v = user_input[1:].split()
            self.chat_params[a] = convert(v)
            print(f'System: The parameter `{a}` is set to be `{v}`.')
        elif user_input.startswith('#'):
            a, v = user_input[1:].split()
            setattr(self, a, v)
            print(f'System: The attribute `{a}` is set to be `{v}`.')
        elif user_input.startswith('>'):
            self.execute(user_input[1:])
        elif user_input.startswith('!'):
            commands[user_input[1:].strip()](self)
        else:
            message = {"role": "user", "content": user_input}
            self.history.append(message)

            assistant_reply = self._reply(message, n_loop=100)
            self.history.append({"role": "assistant", "content": assistant_reply})
            print(f"{self.name.capitalize()}: {assistant_reply}")


    def _reply(self, user_input, n_loop=100):
        """The reply method of the AI chat assistant
        as a mapping user-input --> assistent-reply
        """
        raise NotImplemented

    @property
    def history_size(self):
        return sum(len(d["content"]) for d in self.history)

