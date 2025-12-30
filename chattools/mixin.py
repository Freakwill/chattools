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

MAX_LEN = 1000


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

    def reply(self, user_input, messages=[], memory_flag=True, show=True, max_retries=100):
        """The reply of the AI chat assistant
        
        Args:
            user_input (str): The query inputed by the user
            messages (list, optional): Additional information before user input
            memory_flag (bool, optional): save the messages
            show (bool, optional): display the reply
            max_retries (int, optional): The maximum of retries
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
            response = self._reply(messages + [message], max_retries=100)
            assistant_reply = response.choices[0].message.content
            if show:
                print(f"{self.name.capitalize()}: {assistant_reply}")

            if memory_flag:
                self.history.extend(messages + [
                    message,
                    {"role": "assistant", "content": assistant_reply
                    }])
                if len(self.history) > MAX_LEN:
                    self.history.pop(0)
            self.current_reply = assistant_reply

    def _reply(self, message, max_retries=100):
        """Wrapper of `chat.completions.create` method of LLM
        The reply method of the AI chat assistant
        as a mapping message --> response

        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                return self.chat.completions.create(
                        model=self.model,
                        messages=self.history + [message],
                        **self.chat_params)
            except OpenAIError as e:
                k +=1
                if k >= max_retries:
                    print(f"System: An error occurred after {max_retries} attempts:")
                    raise e
            except Exception as e:
                raise f"An unexpected error occurred: {e}"

    @property
    def history_size(self):
        return sum(len(d["content"]) for d in self.history)

    