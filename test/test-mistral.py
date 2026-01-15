#!/usr/bin/env python3

from chat_tools import MistralChat
from chat_tools.utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)

with MistralChat(description=description, name=role) as chat:
    chat.run()
