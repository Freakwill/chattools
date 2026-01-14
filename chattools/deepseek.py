#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from .mixin import ChatMixin

from .utils import get_api_key

api_key = get_api_key('DEEPSEEK')


class DeepseekChat(ChatMixin, OpenAI):

    def __init__(self, description='You are a very intelligent agent', history=[], name='Assistant', model="deepseek-chat", *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.deepseek.com", *args, **kwargs)
        self.description = description
        self.name = name
        self.model = model
        self.chat_params = {}

        self.history = history


if __name__ == "__main__":

    from utils import read_yaml, menu
    roles = read_yaml()
    role, description = menu(roles)
    chat = DeepseekChat(description=description, name=role)
    chat.run()
