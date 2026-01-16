#!/usr/bin/env python3

from .base import ChatMixin
from groq import Groq, APIConnectionError

from .utils import get_api_key

api_key = get_api_key('GROQ')


class GroqChat(ChatMixin, Groq):

    def __init__(self, description='You are a very intelligent agent', history=[], name='Assistant', model="openai/gpt-oss-120b", *args, **kwargs):
        super().__init__(api_key=api_key, model=model, *args, **kwargs)
        self.description = description
        self.name = name
        self.model = model
        self.history = history
        self.chat_params = {}

    def _reply(self, messages, max_retries=20):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                return self.responses.create(
                        model=self.model,
                        messages=messages,
                        **self.chat_params)
            except APIConnectionError as e:
                k +=1
                if k >= max_retries:
                    print(f"💻System: An error occurred after {max_retries} attempts: {e}")
            except Exception as e:
                raise f"An unexpected error occurred: {e}"

