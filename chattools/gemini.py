#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from .mixin import ChatMixin

import google.generativeai as genai
# Set API Key on https://aistudio.google.com/app/apikey
from .utils import get_api_key
api_key = get_api_key('GEMINI')
genai.configure(api_key=api_key)


class GeminiChat(ChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="gemini-1.5-flash", *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.deepseek.com", *args, **kwargs)
        self.description = description
        self.history = [{"role": "system", "content":self.description}] + history
        self.name = name
        self.model = model

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, v):
        self._history = self.chat.history = v

    def _reply(self, messages, max_retries=100):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                return self.chat.completions.create(messages)
            except OpenAIError as e:
                k +=1
                if k >= max_retries:
                    raise f"System: An error occurred after {max_retries} attempts: {e}"
            except Exception as e:
                raise f"An unexpected error occurred: {e}"
