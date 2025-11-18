#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from mixin import ChatMixin

import google.generativeai as genai
# Set API Key on https://aistudio.google.com/app/apikey
from utils import get_api_key
api_key = get_api_key('GEMINI')
genai.configure(api_key=api_key)


class GeminiChat(ChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="gemini-1.5-flash", *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__init__(api_key=api_key, base_url="https://api.deepseek.com", *args, **kwargs)
        self.description = description
        self._history = self.chat.history = history
        self.name = name
        self.model = model

    def _reply(self, message='', max_retries=100):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                response = self.chat.send_message(message)
                return response.choices[0].message.content
            except OpenAIError as e:
                k +=1
                if k >= max_retries:
                    raise f"System: An error occurred after {max_retries} attempts: {e}"
            except Exception as e:
                raise f"An unexpected error occurred: {e}"
