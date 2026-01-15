#!/usr/bin/env python3

from chat_tools import GeminiChat
from chat_tools.utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)
chat = GeminiChat(description=description, name=role)
chat.run()
