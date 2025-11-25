# chattools

my tools for AI chat, such as gemini, deepseek

save the API keys in `.env.key` file in the current path.

## Example

run `python path/to/test.py` (deepseek)



run `python path/to/test-mistral.py`  to utilize mistral AI.



## Code



```python
from mixin import ChatMixin
from utils import get_api_key

# api_key = get_api_key


class YourChat(ChatMixin, YourLLM):

    def __init__(self, description=None, history=[], name='Assistant', model="mistral-small-latest", *args, **kwargs):
        super().__init__(api_key=api_key, *args, **kwargs)
        self.description = description
        self._history = history
        self.name = name
        self.model = model
        self.chat_params = {}

    def _reply(self, message, max_retries=100):
        """The reply method of the AI chat assistant
        
        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                # get the response of the model
                return response.choices[0].message.content
            except:
                ...
            

```

---

![](pic.jpg)