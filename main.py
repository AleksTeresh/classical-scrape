#!/usr/bin/python3

from scrapers.mus_talo import fetch_musiikkitalo_gigs
from scrapers.philarmonia_spb import fetch_spb_philarmonia_gigs
from scrapers.mariinski import fetch_mariinsky_gigs
from common.client import post_new_gig, post_new_token_req
import datetime


def __get_next_month(x: datetime.datetime):
    x.replace(day=1)
    nextmonthdate = x
    if x.month == 12:
        nextmonthdate = x.replace(year=x.year + 1, month=1)
    else:
        nextmonthdate = x.replace(month=x.month + 1)

    return nextmonthdate


def __get_new_token():
    response = post_new_token_req('admin@classical.dynu.net', 'adminsecret')
    token = response.json()['token']

    return token


# has full composer names and follow standard international naming pretty well
# hence, should go first, to create authors with proper names
fetch_date = datetime.date.today()
# fetch 4 months ahead including the current
for x in range(0, 4):
    fetched_mariinsky_gigs = []

    try:
        fetched_mariinsky_gigs = fetch_mariinsky_gigs(fetch_date.year, fetch_date.month)
    except:
        fetched_mariinsky_gigs = []

    # make sure the token is not expired, since fetching might take a while
    token = __get_new_token()
    for gig in fetched_mariinsky_gigs:
      post_new_gig(gig, token)

    # increment month value to fetch further gigs
    fetch_date = __get_next_month(fetch_date)


# has full composer names, but spelling is often specific
fetched_musiikkitalo_gigs = []

try:
    fetched_musiikkitalo_gigs = fetch_musiikkitalo_gigs(10)
except:
    fetched_musiikkitalo_gigs = []

token = __get_new_token()
for gig in fetched_musiikkitalo_gigs:
    post_new_gig(gig, token)


# has only last names of composers, hence should go last,
# so that it will eventually match with one of the previously created composers
fetch_date = datetime.date.today()
# fetch 4 months ahead including the current
for x in range(0, 4):
    fetched_spb_philarmoni_gigs = []
    try:
        fetched_spb_philarmoni_gigs = fetch_spb_philarmonia_gigs(fetch_date.year, fetch_date.month)
    except:
        fetched_spb_philarmoni_gigs = []

    # make sure the token is not expired, since fetching might take a while
    token = __get_new_token()
    for gig in fetched_spb_philarmoni_gigs:
        post_new_gig(gig, token)

    # increment month value to fetch further gigs
    fetch_date = __get_next_month(fetch_date)
