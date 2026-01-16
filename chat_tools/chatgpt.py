#!/usr/bin/env python3

from openai import OpenAI
from .mixin import BaseOpenAIChat

from .utils import get_api_key

api_key = get_api_key('OPENAI')


class ChatGPTChat(BaseOpenAIChat):

    def __init__(self, *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.openai.com/v1", *args, **kwargs)


from utils import read_yaml, menu
roles = read_yaml()
role, description = menu(roles)
chat = ChatGPTChat(description=description, name=role)
chat.run()
