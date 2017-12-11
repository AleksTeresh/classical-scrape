#!/usr/bin/python3

# import libraries
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from typing import List, Tuple
import datetime

from common.gig import Gig
from common.performance import Performance

# specify the url
QUOTE_PAGE = 'http://www.philharmonia.spb.ru/en/afisha/?'

def fetch_spb_philarmonia_gigs(
        year: int = datetime.datetime.now().year,
        month: int = datetime.datetime.now().month
) -> List[Gig]:
    quote_page = QUOTE_PAGE + 'ev_y=' + str(year) + '&ev_m=' + str(month)
    # query the website and return the html to the variable ‘page’
    page = urlopen(quote_page)

    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    gigs = []
    # all the event links
    event_links = soup.find_all('div', attrs={'class': 'afisha_list_item'})

    # all the images
    image_boxes = soup.find_all('div', attrs={'class': 'mer_item_img'})

    for i in range(len(event_links)):
        event_link = event_links[i]

        full_event_link = 'http://www.philharmonia.spb.ru' + event_link['data-scope-url']
        event_page = urlopen(full_event_link)
        event_soup = BeautifulSoup(event_page, 'html.parser')

        gig = Gig(
            __scrape_name(event_soup),
            "", # description
            __scrape_image_url(image_boxes, i),
            __scrape_performances(event_soup),
            __scrape_datetime(event_soup, year, month),
            "", # duration
            3,  # Spb philarmony id
            full_event_link
        )

        #print(gig.name)
        #print(gig.imageUrl)
        #print(gig.performances)
        #print(gig.timestamp)
        print('Gig was fetched')
        gigs.append(gig)
        time.sleep(1)

    return gigs

def __scrape_name (event_soup: object) -> str:
    title_field = event_soup.find('div', attrs={'class': 'afisha_element_title'})
    title = title_field.contents[1].contents[0].strip()

    return title

def __scrape_description (event_soup: object) -> str:
    description_field = event_soup.find('div', attrs={'class': 'field field--field-description'})
    description = description_field.text.strip()

    return description

def __scrape_image_url (image_fields: List[object], currentIndex: int) -> str:
    attrs = image_fields[0].attrs
    images = list(map(__extract_image_url, image_fields))

    return 'http://www.philharmonia.spb.ru' + images[currentIndex]

def __extract_image_url(image_field):
    attrs = image_field.attrs
    if len(attrs) > 2:
        return attrs['style'].strip()[23:-2]

    return ''


def __scrape_performances (event_soup: object) -> List[Performance]:
    performances = []
    repertoire_field = event_soup.find('div', attrs={'class': 'td ae_music'})
    if repertoire_field:
        for i in range(len(repertoire_field.contents)):
            child = repertoire_field.contents[i]

            # the last child is always empty
            if child != '\n' and i < len(repertoire_field.contents) - 3:
                composer = child.contents[1].text.strip()
                opus = ''
                # - \n
                # - <composer>
                # - \n
                # - <opus>
                # - \n
                # - <opus>
                # - \n
                for opus_index in range(len(child.contents)):
                    if opus_index % 2 == 1 and opus_index > 1:
                        opus = child.contents[opus_index].text.strip()
                        performances.append(Performance(opus, composer))

                # scrape only author name, if opus name is not present
                if len(child.contents) <= 3:
                    opus = ''
                    performances.append(Performance(opus, composer))


    return performances

def __scrape_datetime (event_soup: object, yeah: int, month: int) -> str:
    day = event_soup.find('div', attrs={'class': 'date_day'}).text.strip()
    time = event_soup.find('div', attrs={'class': 'afisha_element_h'}).text.strip()
    hours = time[:2]
    hoursInt = int(hours)
    minutes = time[3:-3]
    z = time[-2:] # AM or PM
    if z == 'PM' or z == 'pm':
        hoursInt += 12
        hours = str(hoursInt)

    return str(yeah) + '-' + str(month) + '-' + day + 'T' + hours + ':' + minutes + ':00+02:00'
