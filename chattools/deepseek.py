#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from mixin import ChatMixin

from utils import get_api_key

api_key = get_api_key('DEEPSEEK')


class DeepseekChat(ChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="deepseek-chat", *args, **kwargs):
        super().__init__(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            *args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model
        self.chat_params = {}

    def _reply(self, message, n_loop=100):
        """The reply method of the AI chat assistant
        
        Args:
            message (str): the prompt object inputed by the user
            n_loop (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                response = self.chat.completions.create(
                        model=self.model,
                        messages=self.history,
                        **self.chat_params)
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
        return assistant_reply


from utils import read_yaml, menu
roles = read_yaml()
role, description = menu(roles)
print(f"System: you select {role}.")
chat = DeepseekChat(description=description, name=role)
chat.run()
