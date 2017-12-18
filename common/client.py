#!/usr/bin/python3

import requests

from common.encoders.gig_encoder import GigEncoder
from common.gig import Gig

GIG_URL = 'https://classical.dynu.net/api/gig'
AUTH_URL = 'https://classical.dynu.net/api/auth'

myEncoder = GigEncoder()

def post_new_gig (new_gig: Gig, token: str) -> object:
    print('Sending a gig to the API')
    r = requests.post(
        GIG_URL,
        json=new_gig,
        headers={'Authorization': 'Bearer ' + token},
        cert=('cert.pem', 'cert.key'),
        verify=False
    )

    # print(r)
    return r

def post_new_token_req (username: str, password: str) -> str:
    print('Sending a request for a token')
    r = requests.post(
        AUTH_URL,
        json={'email': username, 'password': password},
        cert=('cert.pem', 'cert.key'),
        verify=False
    )

    # print(r)
    return r
