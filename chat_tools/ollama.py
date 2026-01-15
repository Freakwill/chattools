#!/usr/bin/env python3

from .mixin import ChatMixin
import ollama
from ollama import Client, ResponseError

from .utils import get_api_key

api_key = get_api_key('OLLAMA')


class OllamaChat(ChatMixin, Client):
    # see https://github.com/ollama/ollama-python

    get_reply = lambda response: response.message.content

    def __init__(self, description=None, history=[], name='Assistant', model='gpt-oss:120b', api_key=api_key, *args, **kwargs):
        if api_key:
            super().__init__(host='https://ollama.com',
    headers={'Authorization': 'Bearer ' + api_key}, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
        self.description = description
        self.name = name
        if ':' not in model:
            model += ':latest'
        self.model = model
        self.chat_params = {}
        self.history = history

    def _reply(self, messages, max_retries=100):
        """Wrapper of `chat.completions.create` method of LLM
        The reply method of the AI chat assistant
        as a mapping message --> response

        Args:
            message: the prompt object inputed by the user
            max_retries (int, optional): the number of times to get response
        """

        k = 0
        while True:
            try:
                return self.chat(model=self.model, messages=messages, **self.chat_params)
            except ResponseError as e:
                k +=1
                if k >= max_retries:
                    print(f"System: An error occurred after {max_retries} attempts:")
                    raise e
            except Exception as e:
                raise f"An unexpected error occurred: {e}"

    def __enter__(self, *args, **kwargs):
        import sh
        sh.brew.services.start.ollama()
        return self

    def __exit__(self, *args, **kwargs):
        import sh
        sh.brew.services.stop.ollama()


class LocalOllamaChat(OllamaChat):

    def __init__(self, model='gemma3', *args, **kwargs):
        super().__init__(model=model, api_key=None, *args, **kwargs)
    
    def init(self, *args, **kwargs):

        model_list = [m.model for m in ollama.list().models]
        if self.model not in model_list:
            raise f'{self.model} is not found!'

        super().init(*args, **kwargs)

