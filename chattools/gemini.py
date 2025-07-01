#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from mixin import ChatMixin


class GeminiChat(ChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="gemini-1.5-flash", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model

    @property
    def history(self):
        return self.chat.history

    @history.setter
    def history(self, v):
        self.chat.history=v

    def _reply(self, user_input, n_loop=100):
        """The reply method of the AI chat assistant
        
        Args:
            user_input (str): the prompt inputed by the user
            n_loop (int, optional): the number of times to get response
        """

        if user_input.startswith(':'):
            a, v = user_input[1:].split()
            self.chat_params[a] = convert(v)
            print(f'System: The parameter `{a}` is set to be `{v}`.')
            return

        message = {"role": "user", "content": user_input}
        self.history.append(message)

        k = 0
        while True:
            try:
                response = self.chat.send_message(message)
                break
            except OpenAIError as e:
                k +=1
                if k >= n_loop:
                    print(f"System: An error occurred after {n_loop} attempts:")
                    raise e
            except Exception as e:
                print(f"An unexpected error occurred:")
                raise e

        assistant_reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_reply})
        print(f"{self.name}: {assistant_reply}")


import google.generativeai as genai

import pathlib
HISTORY_PATH = pathlib.Path('history.yaml')

# Set API Key on https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyApwghFN31zbE25qQz_tlFr7DGiP2van8s"
genai.configure(api_key=GEMINI_API_KEY)

roles = read_yaml()
role, description = menu(roles)
print(f"System: you select {role}.")
chat = DeepseekChat(description=description)
chat.run()