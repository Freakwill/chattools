#!/usr/bin/env python3

from chattools import *
from chattools.utils import read_yaml, menu

roles = read_yaml()
role, description = menu(roles)

with DeepseekChat(description=description, name=role) as chat:
	chat.run()
