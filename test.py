#!/usr/bin/python3

from common.gig import Gig
from common.performance import Performance
from common.client import post_new_gig, post_new_token_req

gig1 = Gig(
    'Lukas Geniš',
    '',
    'http://www.philharmonia.spb.ru/upload/resize_cache/iblock/f88/100_100_2/Genushas.jpg',
    [
        Performance('Sonatine', 'Ravel'),
        Performance('Études-Tableaux', 'Rahmaninov'),
        Performance( 'Prelude and Fugue', 'Enescu'),
        Performance( 'Sonata h-moll', 'Franz Liszt'),
        Performance( 'sf know srcept', '')
    ],
    '2017-12-22T19:00:00+02:00',
    '2 hours',
    3,  # Musiikkitalo id
    ' http://www.philharmonia.spb.ru/en/afisha/176435/'
)
gig2 = Gig(
    'van Beethoven',
    '<p>PERFORMERS: <br/>Soloist: <a href="/en/company/orchestra/piano/mazo">Maria Mazo</a> (piano)<br/>The Mariinsky Orchestra <br/>Conductor: <a href="/en/company/conductors/damev">Mischa&nbsp;Damev</a></p> <p><br/>PROGRAMME: <br/>Ludwig van Beethoven <br/><em>Coriolan</em> Overture, Op. 62 <br/>Piano Concerto&nbsp;No.&nbsp;4 in G&nbsp;major, Op.&nbsp;58 <br/>Symphony&nbsp;No.&nbsp;7 in A&nbsp;major, Op.&nbsp;92</p><p>PERFORMERS: <br/>Soloist: <a href="/en/company/orchestra/piano/mazo">Maria Mazo</a> (piano)<br/>The Mariinsky Orchestra <br/>Conductor: <a href="/en/company/conductors/damev">Mischa&nbsp;Damev</a></p> <p><br/>PROGRAMME: <br/>Ludwig van Beethoven <br/><em>Coriolan</em> Overture, Op. 62 <br/>Piano Concerto&nbsp;No.&nbsp;4 in G&nbsp;major, Op.&nbsp;58 <br/>Symphony&nbsp;No.&nbsp;7 in A&nbsp;major, Op.&nbsp;92</p>',
    'https://www.mariinsky.ru/images/cms/data/235_concerts/kollaz/xmazo_damev.jpg.pagespeed.ic.3lJ_v6TLYH.jpg',
    [
        Performance( 'CoriolanOverture, Op. 62', 'Ludwig van Beethoven'),
        Performance( 'Piano Concerto No. 4 in G major, Op. 58', 'Ludwig van Beethoven'),
        Performance( 'Symphony No. 7 in A major, Op. 92', 'Ludwig van Beethoven'),
        Performance( 'Something here', '')
    ],
    '2017-12-22T19:00:00+02:00',
    '2 hours',
    2,  # Musiikkitalo id
    'https://www.mariinsky.ru/en/playbill/playbill/2017/11/2/3_1900/'
)

gig3 = Gig(
    'FRSO & Saraste & Tamestit',
    'Performing the viola concerto by German Jörg Widmann is Antoine Tamestit, Professor at the Paris Conservatory, who premiered it two years ago. We will thus have a chance to hear not only his ‘Mahler’ Stradivarius of 1672 but also a rainmaker, water gong, bass flute and metal chimes. Bruckner’s symphony measures time and space.',
    'https://www.musiikkitalo.fi/sites/default/files/styles/full_node_view/public/thumbnails/image/rso_2015.jpg?itok=-_PPBPCb',
    [
        Performance( 'Viola Concerto', 'Jörg Widmann'),
        Performance( 'Symphony No. 3', 'Anton Bruckner')
    ],
    '2017-12-22T19:00:00+02:00',
    '2 hours',
    1,  # Musiikkitalo id
    'https://www.musiikkitalo.fi/en/content/frso-saraste-tamestit'
)

response = post_new_token_req('admin@classical.dynu.net', 'adminsecret')
post_new_gig(gig1, response.json()['token'])
# post_new_gig(gig2, response.json()['token'])
# post_new_gig(gig3, response.json()['token'])
