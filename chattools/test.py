#!/usr/bin/env python3

from deepseek import DeepseekChat
from utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)
print(f"System: you select {role}.")
chat = DeepseekChat(description=description, name=role)
chat.run()
