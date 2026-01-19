#!/usr/bin/env python3

"""Chat with Deepseek

Attributes:
    api_key (str): API Key for deepseek (https://platform.deepseek.com/api_keys)

Examples:
    from chat_tools.utils import read_yaml, menu
    roles = read_yaml()
    role, description = menu(roles)
    with DeepseekChat(description=description, name=role) as chat:
        chat.run()
"""

from .base import BaseOpenAIChat

from .utils import get_api_key

api_key = get_api_key('DEEPSEEK')


class DeepseekChat(BaseOpenAIChat):

    def __init__(self, model="deepseek-chat", api_key=api_key, base_url="https://api.deepseek.com", *args, **kwargs):
        super().__init__(api_key=api_key, base_url=base_url, model=model, *args, **kwargs)
