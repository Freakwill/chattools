#!/usr/bin/env python3

from mixin import ChatMixin
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError

from utils import get_api_key

api_key = get_api_key('MISTRAL')


class MistralChat(ChatMixin, Mistral):

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
                response = self.chat.complete(
                        model=self.model,
                        messages=self.history + [message],
                        **self.chat_params)
                return response.choices[0].message.content
            except SDKError as e:
                k +=1
                if k >= max_retries:
                    print(f"System: An error occurred after {max_retries} attempts:")
                    raise e
            except Exception as e:
                raise f"An unexpected error occurred: {e}"

