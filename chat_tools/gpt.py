#!/usr/bin/env python3

from .base import BaseOpenAIChat

from .utils import get_api_key

api_key = get_api_key('CHATANYWHERE')


class GPTChat(BaseOpenAIChat):

    def __init__(self, base_url="https://api.chatanywhere.tech", *args, **kwargs):
        super().__init__(api_key=api_key, base_url=base_url, *args, **kwargs)

