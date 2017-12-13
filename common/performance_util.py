#!/usr/bin/python3

from typing import List
from common.performance import Performance
from bs4 import BeautifulSoup

def filter_valid_performances (performances: List[Performance]) -> List[Performance]:
    valid_performances = []

    for perf in performances:
        name = perf.name
        author = perf.author

        author_tokens = author.split(' ')

        # if the author includes by, that means the entry is "Composed by" or "Performed by" and not a valid performance
        if (len(author_tokens) > 1 and author_tokens[1] == 'by'):
            continue

        num_of_capital_words = 0
        num_of_ord_words = 0
        for word in author_tokens:
            if word[0].isupper():
                num_of_capital_words = num_of_capital_words + 1
            else:
                num_of_ord_words = num_of_ord_words + 1

        # if the number of words with first letter not being capital is larger than those with the first capital letter
        # most likely the author name is invalid, remove the performance
        if num_of_ord_words > num_of_capital_words:
            continue

        author_plain_text = BeautifulSoup(author, 'html.parser').get_text()
        name_plain_text = BeautifulSoup(name, 'html.parser').get_text()
        # if the athon name or the perfromance name consists entirely of an html tag with no text in it, drop the performance
        if (author != '' and (author_plain_text is None or author_plain_text == '')) or\
                (name != '' and (name_plain_text is None or name_plain_text == '')):
            continue

        #otherwise, the performance is valid
        valid_performances.append(perf)


    return valid_performances






