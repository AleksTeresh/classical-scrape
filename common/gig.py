#!/usr/bin/python3

from typing import Any, List
from json import JSONEncoder

from common.performance import Performance

class Gig (dict):
    def __init__(
            self: Any,
            name: str,
            description: str = '',
            image_url: str = '',
            performances: List[Performance] = [],
            timestamp: str = '',
            duration: str = '',
            venue: int = 0,
            url: str = ''
    ) -> None:
        super().__init__()
        self.__dict__ = self
        self.name = name
        self.description = description
        self.imageUrl = image_url
        self.performances = performances
        self.timestamp = timestamp
        self.duration = duration
        self.venue = venue
        self.url = url



