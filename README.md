# chattools

The most simple tool for AI chat, such as gemini, deepseek, ollama

plz save the API keys in `.env.key` file in the current path.

## Example

run `python path/to/test.py` (deepseek)



run `python path/to/test-mistral.py`  to utilize mistral AI.


## Make CLI

create ollama-chat.py
```python
#!/usr/bin/env python3

# default model is `gpt-oss:120b`

from chattools import OllamaChat

description="Intelligent enough to help me for anything."
name="Asistant"

with OllamaChat(description=description, name=name) as chat:
    chat.run()
```

run `chmod` dommand and `ollama-chat.py`


## Code


```python
# import YourLLM API 
from mixin import ChatMixin
from utils import get_api_key

# api_key = get_api_key


class YourChat(ChatMixin, YourLLM):

    def __init__(self, description=None, history=[], name='Assistant', model="model-name", *args, **kwargs):
        super().__init__(api_key=api_key, *args, **kwargs)  # init method of super class
        self.description = description
        self.name = name
        self.model = model
        self.chat_params = {}

        self.history = history

    def _reply(self, messages, max_retries=100):
        """The wrapper method of the original `chat` method
        """

        k = 0
        while True:
            # try `max_retries` times
            try:
                """
                get the response of the model. such as 
                self.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        **self.chat_params)
                """
            except:
                ...

```

## Commands

register a command as follows
```
from chat_tools.commands import Commands

@Commands.register("read")
def read_history(obj, path):
    # obj.history = read from `path`
    pass
```

use the command in the chat as `!read path`

---

![](pic.jpg)