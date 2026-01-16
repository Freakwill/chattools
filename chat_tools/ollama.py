#!/usr/bin/env python3

from .base import ChatMixin
import ollama
from ollama import Client, ResponseError

from .utils import get_api_key

api_key = get_api_key('OLLAMA')

class ModelNotFoundError(Exception):
    """
    Do not find the model locally
    """
    def __init__(self, model):
        self.model = model
        super().__init__(f"Model `{self.model}` is not found in locally!")


class OllamaChat(ChatMixin, Client):
    # see https://github.com/ollama/ollama-python

    get_reply = lambda response: response.message.content

    def __init__(self, description='You are a very intelligent agent', history=[], name='Assistant', model='gpt-oss:120b', api_key=api_key, *args, **kwargs):
        if ':' not in model:
            model += ':latest'
        if api_key:
            super().__init__(host='https://ollama.com',
                headers={'Authorization': 'Bearer ' + api_key}, *args, **kwargs)
        else:
            super().__init__(model=model, *args, **kwargs)
            if any(self.model==m.model for m in ollama.list().models):
                raise ModelNotFoundError(self.model)
        self.description = description
        self.name = name
        self.model = model
        self.history = history
        self.chat_params = {}

    def _reply(self, messages, max_retries=20):
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
                    raise Exception(f"System: An error occurred after {max_retries} attempts: {e}")
            except Exception as e:
                raise e

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
        if any(self.model==m.model for m in ollama.list().models):
            raise ModelNotFoundError(self.model)

        super().init(*args, **kwargs)

