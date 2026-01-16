#!/usr/bin/env python3

from openai import OpenAI, OpenAIError
from .base import BaseOpenAIChat

from .utils import get_api_key

api_key = get_api_key('DEEPSEEK')


class DeepseekChat(BaseOpenAIChat, OpenAI):

    def __init__(self, model="deepseek-chat", *args, **kwargs):
        super().__init__(api_key=api_key, base_url="https://api.deepseek.com", model=model, *args, **kwargs)


if __name__ == "__main__":

    from utils import read_yaml, menu
    roles = read_yaml()
    role, description = menu(roles)
    with DeepseekChat(description=description, name=role) as chat:
        chat.run()
