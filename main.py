#!/usr/bin/python3

from scrapers.mus_talo import fetch_musiikkitalo_gigs
from scrapers.philarmonia_spb import fetch_spb_philarmonia_gigs
from common.client import post_new_gig, post_new_token_req

fetched_musiikkitalo_gigs = fetch_musiikkitalo_gigs()
fetched_spb_philarmoni_gigs = fetch_spb_philarmonia_gigs()

response = post_new_token_req('admin@classical.dynu.net', 'adminsecret')
token = response.json()['token']

for gig in fetched_musiikkitalo_gigs:
  post_new_gig(gig, token)

for gig in fetched_spb_philarmoni_gigs:
    post_new_gig(gig, token)
