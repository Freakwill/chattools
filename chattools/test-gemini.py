#!/usr/bin/env python3

from chattools import GeminiChat
from utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)
chat = GeminiChat(description=description, name=role)
chat.run()
