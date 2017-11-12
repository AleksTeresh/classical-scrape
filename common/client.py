#!/usr/bin/python3

import requests

from common.encoders.gig_encoder import GigEncoder
from common.gig import Gig

URL = 'http://classical.dynu.net/api/gig'
myEncoder = GigEncoder()

def post_new_gig (new_gig: Gig) -> object:
    print('Sending a gig to the API')
    r = requests.post(URL, json=new_gig)

    print('A gig was sucessfully sent')
    return r

