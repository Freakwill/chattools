#!/usr/bin/env python3

from .base import BaseOpenAIChat

import google.generativeai as genai
# Set API Key on https://aistudio.google.com/app/apikey
from .utils import get_api_key
api_key = get_api_key('GEMINI')
genai.configure(api_key=api_key)


class GeminiChat(BaseOpenAIChat):

    def __init__(self, model="gemini-1.5-flash", *args, **kwargs):
        super().__init__(api_key=api_key, model=model, *args, **kwargs)

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, v):
        self._history = self.chat.history = v

