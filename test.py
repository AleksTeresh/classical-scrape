#!/usr/bin/python3

from common.gig import Gig
from common.performance import Performance
from common.client import post_new_gig, post_new_token_req

gig = Gig(
    'RSO & Lintu & Finley',
    'Kaija Saariahon True Fire baritonille ja orkesterille kietoo kuulijan luonnon ja kosmoksen rihmastoon, elämän syvintä olemusta aistimaan. Solistina laulaa Gerald Finley, joka muistetaan Kansallisoopperan (2004) Kaukaisen rakkauden trubaduuri Jaufréna. Valoa ja liekkejä löytyy Klamin ja Stravinskyn baleteistakin.Teksti: Susanna Välimäkim',
    'https://www.musiikkitalo.fi/sites/default/files/styles/full_node_view/public/thumbnails/image/rso_2015.jpg?itok=-_PPBPCb',
    [
        Performance('Pyörteitä', 'Uuno Klami'),
        Performance('True fire', 'Kaija Saariaho'),
        Performance('Petrushka', 'Igor Stravinsky')
    ],
    '2017-12-13T19:00:00+02:00',
    '2 hours',
    1,  # Musiikkitalo id
    'https://www.musiikkitalo.fi'
)

response = post_new_token_req('admin@classical.dynu.net', 'adminsecret')
post_new_gig(gig, response.json()['token'])
