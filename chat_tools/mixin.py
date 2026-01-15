#!/usr/bin/env python3

import shlex
from .commands import Commands


MAX_LEN = 1000


class ChatMixin:

    get_reply = lambda response: response.choices[0].message.content

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, v):
        self._history = v

    def init(self, description=None):
        description = description or self.description
        if description is not None:
            message = {"role": "system", "content": description}
            self.history.insert(0, message)

    def run(self, description=None):
        # To chat with AI
        self.init(description=description)

        while True:
            user_input = input("👨User: ")
            if user_input.strip().lower() in {'exit', 'quit', 'bye'}:
                print(f'🤖{self.name.capitalize()}: Bye.')
                break
            self.reply(user_input)
            self.post_process()

    def post_process(self):
        max_len = 20
        if len(self.history) > max_len:
            self.history = self.history[-max_len:]

    def demo(self, prompts):
        self.init()
        for p in prompts:
            print(f"👨User: {p}")
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
            print(f'💻System: The parameter `{a}` of chat method is set to be `{v}`.')
        elif user_input.startswith('#'):
            a, v = user_input[1:].split()
            setattr(self, a, v)
            print(f'💻System: The attribute `{a}` of chat object is set to be `{v}`.')
        elif user_input.startswith('>'):
            self.execute(user_input.lstrip('> '))
        elif user_input.startswith('!'):
            cmd = user_input.lstrip('! ')
            cmd, *args = shlex.split(cmd)
            try:
                getattr(Commands, cmd)(self, *args)
            except AttributeError:
                print(f"💻System: {cmd} is not registered yet!")
            except Exception as e:
                print(e)
        else:
            message = {"role": "user", "content": user_input}
            messages.append(message)
            response = self._reply(self.history + messages, max_retries=100)
            assistant_reply = self.__class__.get_reply(response)
            if show:
                print(f"🤖{self.name.capitalize()}: {assistant_reply}")

            if memory_flag:
                messages.append({"role": "assistant", "content": assistant_reply
                    })
                self.history.extend(messages)
                if len(self.history) > MAX_LEN:
                    self.history.pop(0)
            self.current_reply = assistant_reply

    def _reply(self, messages, max_retries=100):
        """Wrapper of `chat.completions.create` method of LLM
        The reply method of the AI chat assistant
        as a mapping message --> response
        """

        k = 0
        while True:
            try:
                return self.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        **self.chat_params)
            except OpenAIError as e:
                k +=1
                if k >= max_retries:
                    print(f"💻System: An error occurred after {max_retries} attempts: {e}")
            except Exception as e:
                raise f"An unexpected error occurred: {e}"

    @property
    def history_size(self):
        return sum(len(d["content"]) for d in self.history)

    def execute(self, *args, **kwargs):
        # call python compiler
        return exec(*args, **kwargs)

    def load_commands(self, commands=Commands):
        self._commands = commands

    def get_command(self, cmd_name):
        return getattr(self._commands, cmd_name)

    