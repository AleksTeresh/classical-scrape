#!/usr/bin/python3

# import libraries
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import List, Tuple
import datetime

from common.gig import Gig
from common.performance import Performance

# specify the url
QUOTE_PAGE = 'https://www.mariinsky.ru/en/playbill/playbill?type=concert&'

def fetch_mariinsky_gigs (
        year: int = datetime.datetime.now().year,
        month: int = datetime.datetime.now().month
) -> List[Gig]:
    quote_page = QUOTE_PAGE + 'year=' + str(year) + '&month=' + str(month)
    # query the website and return the html to the variable ‘page’
    page = urlopen(quote_page)

    # parse the html using beautiful soap and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    gigs = []
    # all the event links
    event_boxes = soup.find_all('div', attrs={'class': 'spec_name'})

    # all the images
    # image_boxes = soup.find_all('div', attrs={'class': 'mer_item_img'})

    for i in range(len(event_boxes)):

        event_box = event_boxes[i]

        full_event_link = 'https://www.mariinsky.ru' + event_box.contents[0]['href']
        event_page = urlopen(full_event_link)
        event_soup = BeautifulSoup(event_page, 'html.parser')

        gig = Gig(
            __scrape_name(event_soup),
            __scrape_description(event_soup),
            __scrape_image_url(event_soup),
            __scrape_performances(event_soup),
            __scrape_datetime(event_soup, year, month),
            "", # duration
            2,  # Mariinsky id
            full_event_link
        )

        # print(gig.name)
        # print(gig.description)
        #print(gig.imageUrl)
        #print(gig.performances)
        #print(gig.timestamp)
        print('Gig was fetched')
        gigs.append(gig)
        time.sleep(1)

    return gigs

def __scrape_name (event_soup: object) -> str:
    title_field = event_soup.find('span', attrs={'itemprop': 'summary'})
    title = title_field.text.strip()

    return title

def __scrape_description (event_soup: object) -> str:
    description_field = event_soup.find('div', attrs={'class': 'description'})
    description = innerHTML(description_field)# str().strip()

    return description

def __scrape_image_url (event_soup: object) -> str:
    image_box = event_soup.find('div', attrs={'id': 'spec_img_cont'})
    image_url = image_box.contents[0]['src']

    return 'https://www.mariinsky.ru' + image_url

def __extract_image_url(image_field):
    attrs = image_field.attrs
    if len(attrs) > 2:
        return attrs['style'].strip()[23:-2]

    return ''


def __scrape_performances (event_soup: object) -> List[Performance]:
    performances = []
    # get the outer description box
    repertoire_field = event_soup.find('div', attrs={'class': 'description'})
    # if the description box exists
    if repertoire_field:
        # get all the <p> tags inside
        p_tags = repertoire_field.findAll('p')
        index = 0
        # skip all the <p> tags until we get to the "PROGRAMME:" part
        while index < len(p_tags) and\
                not ('PROGRAMME' in str(p_tags[index].contents[0]) or\
                             (len(p_tags[index].contents) > 1 and\
                                         'PROGRAMME' in str(p_tags[index].contents[1]))):
            index = index + 1

        # if we found "PROGRAMME:" part, go through it, entry by entry untill we encounter the next subheading i.e UPPERCASED text
        try:
            while index < len(p_tags) and ('PROGRAMME' in str(p_tags[index].contents[1]) or not str(p_tags[index].contents[1]).isupper()):
                # list to store all the string values
                strings = []
                string_idx = 0
                # text entries are separated by <br> tags
                if p_tags[index].contents[0] and isinstance(p_tags[index].contents[0], NavigableString):
                    strings.append(str(p_tags[index].contents[0]))
                    string_idx = string_idx + 1

                for br in p_tags[index].findAll('br'):
                    next_s = br.nextSibling
                    # if there is no text after this <br> tag, get to the next one
                    if not (next_s and next_s.name != 'br'):
                        continue

                    # otherwise store the text following the current <br> tag
                    strings.append(str(next_s).strip())
                    # check the following after the next sibling, if it is a text, append it
                    next2_s = next_s.nextSibling
                    if next2_s and next2_s.name != 'br':
                        strings[string_idx] = strings[string_idx] + str(next2_s).strip()
                        # check the 2nd following after the next sibling, if it is a text, append it
                        next3_s = next2_s.nextSibling
                        if next3_s and next3_s.name != 'br':
                            strings[string_idx] = strings[string_idx] + str(next3_s).strip()

                    string_idx = string_idx + 1

                # remove the PROGRAMME text if it exists
                strings = list(filter(lambda x: 'PROGRAMME' not in x, strings))

                composer = ''
                if len(strings) == 1 and strings[0] == 'Performed by':
                    performances.append(Performance(strings[0], ''))
                elif len(strings) > 0:
                    composer = strings[0]

                # if there are several opuses of a single composer, create multiple performance entries,
                # otherwise, if there are no opus names, but only the composer name,
                # create the "nameless" Performance of the composer
                if len(strings) > 1:
                    del strings[0]
                    opuses = strings
                    performances = performances + list(map(lambda x: Performance(x, composer), opuses))
                elif composer != '':
                    performances.append(Performance('', composer))

                index = index + 1
        except:
            index = index + 1

    return performances

def __scrape_datetime (event_soup: object, yeah: int, month: int) -> str:
    day = event_soup.find('div', attrs={'class': 'day'}).text.strip()
    time = event_soup.find('div', attrs={'class': 'hour'}).text.strip()

    if len(day) == 1:
        day = '0' + day

    return str(yeah) + '-' + str(month) + '-' + day + 'T' + time + ':00+02:00'

def innerHTML(element):
    if element is None:
        return ''

    return element.decode_contents(formatter="html")
