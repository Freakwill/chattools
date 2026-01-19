#!/usr/bin/env python3

from .base import ChatMixin

import google.generativeai as genai

# Set API Key on https://aistudio.google.com/app/apikey
from .utils import get_api_key
api_key = get_api_key('GEMINI')
genai.configure(api_key=api_key)


class GeminiChat(ChatMixin, genai.GenerativeModel):

    def __init__(self, description='You are a very intelligent agent', history=[], name='Assistant',
        model="gemini-1.5-flash", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description
        self.name = name
        self.model = model
        self.history = history
        self.chat_params = {}

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, v):
        self._history = self.chat.history = v

    def _reply(self, messages, max_retries=10):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                return self.chat.complete(
                        model=self.model,
                        messages=messages,
                        **self.chat_params)
            except Exception as e:
                k +=1
                if k >= max_retries:
                    print(f"💻System: An error occurred after {max_retries} attempts: {e}")

