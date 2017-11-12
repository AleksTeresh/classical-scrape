#!/usr/bin/python3

from json import JSONEncoder
import json

from common.gig import Gig
from common.encoders.performance_encoder import PerformanceEncoder

class GigEncoder(JSONEncoder):
    def default(self, o: Gig):
        perf_encoder = PerformanceEncoder();
        encoded_perfs = []
        for perf in o.performances:
            encoded_perfs.append(perf_encoder.encode(perf))

        return {
            'name': o.name,
            'description': o.description,
            'image_url': o.image_url,
            'timestamp': o.timestamp,
            'duration': o.duration,
            'venue': o.venue,
            'performances': encoded_perfs
        }
