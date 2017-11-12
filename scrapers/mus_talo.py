#!/usr/bin/python3

# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List, Tuple

from common.gig import Gig
from common.performance import Performance

# specify the url
QUOTE_PAGE = 'https://www.musiikkitalo.fi/en/events/calendar?pg='

def fetch_musiikkitalo_gigs(page_number: int = 1) -> List[Gig]:
    quote_page = QUOTE_PAGE + str(page_number)
    # query the website and return the html to the variable ‘page’
    page = urlopen(quote_page)

    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')
    # find all date-time boxes (since datetime is represented here better than in an event's detailed view)
    datetime_boxes = soup.find_all('span', attrs={'class': 'date-display-single'})

    gigs = []
    # all the event links
    event_links = soup.find_all('a', attrs={'class': 'node_liftup__link'})

    for i in range(len(event_links)):
        event_link = event_links[i]

        full_event_link = 'https://www.musiikkitalo.fi' + event_link['href']
        event_page = urlopen(full_event_link)
        event_soup = BeautifulSoup(event_page, 'html.parser')

        gig = Gig(
            __scrape_name(event_soup),
            __scrape_description(event_soup),
            __scrape_image_url(event_soup),
            __scrape_performances(event_soup),
            __scrape_datetime(datetime_boxes, i),
            __scrape_duration(event_soup),
            1,  # Musiikkitalo id,
            full_event_link
        )

        print('Gig was fetched')
        gigs.append(gig)

    return gigs

def __scrape_name (event_soup: object) -> str:
    title_field = event_soup.find('div', attrs={'class': 'field field--title-field'})
    title = title_field.contents[1].text.strip()

    return title

def __scrape_description (event_soup: object) -> str:
    description_field = event_soup.find('div', attrs={'class': 'field field--field-description'})
    description = description_field.text.strip()

    return description

def __scrape_image_url (event_soup: object) -> str:
    image_field = event_soup.find('ul', attrs={'class': 'slides'})
    image_url = image_field.contents[0].contents[1].contents[1].contents[0]['src']

    return image_url

def __scrape_duration (event_soup: object) -> str:
    duration_field = event_soup.find('span', attrs={'class': 'event-duration__duration'})
    duration = duration_field.text.strip()

def __scrape_performances (event_soup: object) -> List[Performance]:
    performances = []
    repertoire_field = event_soup.find('div', attrs={'class': 'field field--event-repertoires'})
    if repertoire_field:
        for child in repertoire_field.children:
            if hasattr(child, 'contents'):
                composer = child.contents[1].text.strip()
                opus = child.contents[3].text.strip()
                performances.append(Performance(opus, composer))

    return performances

def __scrape_datetime (datetime_boxes: List[object], currentIndex: int) -> str:
    datetimes = list(map(lambda x: x['content'].strip(), datetime_boxes))

    return datetimes[currentIndex]