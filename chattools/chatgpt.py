#!/usr/bin/env python3

from openai import OpenAI
from .mixin import OpenAIChatMixin

from .utils import get_api_key

api_key = get_api_key('OPENAI')


class ChatGPTChat(OpenAIChatMixin, OpenAI):

    def __init__(self, description=None, history=[], name='Assistant', model="gpt-4o-mini", *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.openai.com/v1", *args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model
        self.chat_params = {}


from utils import read_yaml, menu
roles = read_yaml()
role, description = menu(roles)
chat = ChatGPTChat(description=description, name=role)
chat.run()
