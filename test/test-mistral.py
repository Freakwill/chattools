#!/usr/bin/env python3

from chattools import MistralChat
from chattools.utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)

with MistralChat(description=description, name=role) as chat:
    chat.run()
