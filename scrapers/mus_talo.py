#!/usr/bin/python3

# import libraries
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List, Tuple

from common.gig import Gig
from common.performance import Performance
from common.performance_util import filter_valid_performances

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
        # if there is no url leading to the ull info event page, move to the next event
        try:
            event_url = event_link['href']
        except:
            continue

        if event_url == '' or event_url == '#':
            continue

        event_soup = ''
        try:
            full_event_link = 'https://www.musiikkitalo.fi' + event_link['href']
            event_page = urlopen(full_event_link)
            event_soup = BeautifulSoup(event_page, 'html.parser')
        except:
            continue

        gig_name = __scrape_name(event_soup)
        performances = __scrape_performances(event_soup)
        valid_performances = []
        try:
            valid_performances = filter_valid_performances(performances)
        except:
            valid_performances = performances

        if gig_name != '':
            gig = Gig(
                gig_name,
                __scrape_description(event_soup),
                __scrape_image_url(event_soup),
                valid_performances,
                __scrape_datetime(datetime_boxes, i),
                __scrape_duration(event_soup),
                1,  # Musiikkitalo id,
                full_event_link
            )

            print('Gig was fetched')
            gigs.append(gig)

        time.sleep(1.5)

    return gigs

def __scrape_name (event_soup: object) -> str:
    try:
        title_field = event_soup.find('div', attrs={'class': 'field field--title-field'})
        title = title_field.contents[1].text.strip()

        return title
    except:
        return ''

def __scrape_description (event_soup: object) -> str:
    try:
        description_field = event_soup.find('div', attrs={'class': 'field field--field-description'})
        description = description_field.text.strip()

        return description
    except:
        return ''


def __scrape_image_url (event_soup: object) -> str:
    try:
        image_field = event_soup.find('ul', attrs={'class': 'slides'})
        image_url = image_field.contents[0].contents[1].contents[1].contents[0]['src']

        return image_url
    except:
        return ''

def __scrape_duration (event_soup: object) -> str:
    try:
        duration_field = event_soup.find('span', attrs={'class': 'event-duration__duration'})
        duration = duration_field.text.strip()

        return duration
    except:
        return ''

def __scrape_performances (event_soup: object) -> List[Performance]:
    performances = []
    repertoire_field = event_soup.find('div', attrs={'class': 'field field--event-repertoires'})
    if repertoire_field is not None:
        try:
            for child in repertoire_field.children:
                try:
                    if hasattr(child, 'contents'):
                        composer = child.contents[1].text.strip()
                        opus = child.contents[3].text.strip()
                        performances.append(Performance(opus, composer))
                except:
                    continue

        except:
            return performances

    return performances

def __scrape_datetime (datetime_boxes: List[object], currentIndex: int) -> str:
    try:
        datetimes = list(map(lambda x: x['content'].strip(), datetime_boxes))

        return datetimes[currentIndex]
    except:
        return ''