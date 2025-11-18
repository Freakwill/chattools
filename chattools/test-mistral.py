#!/usr/bin/env python3

from chattools import *
from utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)
chat = MistralChat(description=description, name=role)
chat.run()
