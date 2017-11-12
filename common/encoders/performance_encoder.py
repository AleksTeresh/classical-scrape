#!/usr/bin/python3

from json import JSONEncoder

from common.performance import Performance

class PerformanceEncoder(JSONEncoder):
    def default(self, o: Performance):
        return {
            'name': o.name,
            'author': o.author
        }
