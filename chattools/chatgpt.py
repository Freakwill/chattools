#!/usr/bin/env python3

from openai import OpenAI
from mixin import OpenAIChatMixin

from utils import get_api_key

api_key = get_api_key('OPENAI')


class ChatGPTChat(OpenAIChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="gpt-4o-mini", *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.openai.com/v1", *args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model
        self.chat_params = {}


    def _reply(self, message, n_loop=100):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            n_loop (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                response = self.chat.completions.create(
                        model=self.model,
                        messages=self.history + [message],
                        **self.chat_params)
                return response.choices[0].message.content
            except OpenAIError as e:
                k +=1
                if k >= n_loop:
                    print(f"System: An error occurred after {n_loop} attempts:")
                    raise e
            except Exception as e:
                raise f"An unexpected error occurred: {e}"


from utils import read_yaml, menu
roles = read_yaml()
role, description = menu(roles)
chat = ChatGPTChat(description=description, name=role)
chat.run()
