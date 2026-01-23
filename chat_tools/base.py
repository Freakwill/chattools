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
        while len(self.history) > max_len:
            self.history = self.pop(1)

    def demo(self, prompts):
        self.init()
        for p in prompts:
            print(f"👨User: {p}")
            self.reply(p)

    def reply(self, user_input, messages=[], memory_flag=True, show=True, max_retries=10):
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
                print(f"💻System: Command `{cmd}` is not registered yet!")
            except Exception as e:
                print(f"💻System: The execution of `{cmd}` raise an error: {e}!")
        else:
            message = {"role": "user", "content": user_input}
            messages.append(message)
            try:
                response = self._reply(self.history + messages)
                assistant_reply = self.__class__.get_reply(response)
                if show:
                    print(f"🤖{self.name.capitalize()}: {assistant_reply}")

                if memory_flag:
                    messages.append({"role": "assistant", "content": assistant_reply})
                    self.history.extend(messages)
                self.current_reply = assistant_reply
            except Exception as e:
                print(e)

    def response(self, messages):
        # Wrapper of `.responses.create` method
        response = self.responses.create(
            model=self.model,
            instructions=self.description,
            input = self.get_text(messages)
        )
        return response.output_text

    def get_text(self, messages):
        return [{"type": "text", "text": message["content"]} for message in messages]

    @property
    def history_size(self):
        return sum(len(d["content"]) for d in self.history)

    def execute(self, *args, **kwargs):
        # call python compiler
        return exec(*args, **kwargs)

    # def load_commands(self, commands=Commands):
    #     self._commands = commands

    # def get_command(self, cmd_name):
    #     return getattr(self._commands, cmd_name)


from openai import OpenAI

default_description = 'You are a very intelligent agent'

class BaseOpenAIChat(ChatMixin, OpenAI):
    # Chat agent with OpenAI API style

    def __init__(self, description=default_description, history=[], name='Assistant', model="gpt-4o-mini",
        base_url="https://api.openai.com/v1", *args, **kwargs):
        super().__init__(base_url=base_url, max_retries=10, *args, **kwargs)
        self.description = description
        self.name = name
        self.model = model
        self.history = history
        self.chat_params = {}

    def _reply(self, messages):
        """Wrapper of `.chat.completions.create` method of LLM
        The reply method of the AI chat assistant
        as a mapping message --> response
        """

        from openai import OpenAIError
        try:
            return self.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    **self.chat_params)
        except OpenAIError as e:
            print(f"💻System: An error occurred after {self.max_retries} attempts: {e}")
        except Exception as e:
            raise e
