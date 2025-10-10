#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from mixin import ChatMixin

from utils import convert, read_yaml, menu


class DeepseekChat(ChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="deepseek-chat", *args, **kwargs):
        super().__init__(
            api_key="sk-7796b3cda6dd40abaf512835b76043fc",
            base_url="https://api.deepseek.com",
            *args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model
        self.chat_params = {}

    def _reply(self, user_input, n_loop=100):
        """The reply method of the AI chat assistant
        
        Args:
            user_input (str): the prompt inputed by the user
            n_loop (int, optional): the number of times to get response
        """

        message = {"role": "user", "content": user_input}
        self.history.append(message)

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


roles = read_yaml()
role, description = menu(roles)
print(f"System: you select {role}.")
chat = DeepseekChat(description=description, name=role)
chat.run()
