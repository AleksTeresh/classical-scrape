#!/usr/bin/python3

from typing import Any

class Performance (dict):
    def __init__(
            self: Any,
            name: str,
            author: str = ''
    ) -> None:
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.author = author