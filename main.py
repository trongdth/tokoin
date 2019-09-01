# -*- coding: utf-8 -*-
# Your code goes below this line

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import logging
import sys
import time
import json

from log_utils import setup_logging
from bl import BL


orgs = []
tickets = []
users = []
table_idx = 0
term = ''
value = ''

with open('data/organizations.json') as json_file:
    orgs = json.load(json_file)

with open('data/tickets.json') as json_file:
    tickets = json.load(json_file)

with open('data/users.json') as json_file:
    users = json.load(json_file)


bl = BL(orgs, tickets, users)

class State:
    BEGIN = 0
    TERM = 1
    VALUE = 2


def __build_search(state):

    if state == State.BEGIN:
        text = input("""
        Select 1) Users or 2) Tickets or 3) Organizations
        """)
        if text in [1, 2, 3]:
            global table_idx
            table_idx = text
            __build_search(State.TERM)

    if state == State.TERM:
        text = raw_input("""
        Enter search term
        """)

        global term
        term = text
        __build_search(State.VALUE)

    if state == State.VALUE:
        text = raw_input("""
        Enter search value
        """)

        global value
        value = text
        response = bl.search(table_idx, term, value)

        for r in response:
            bl.print_readable_data(r)


def __build():
    text = input("""
        Select search options:
            . Press 1 to search 
            . Press 2 to view a list of searchable fields
            . Type 'quit' to exit
        """)

    if text == 1:
        __build_search(State.BEGIN)

    elif text == 2:
        bl.all_searchable_fields()
    

def main():
    setup_logging()
    logger = logging.getLogger()

    try:
        __build()

    except (KeyboardInterrupt, Exception) as e:
        logger.warn("Stopping tokoin: %s", e)


if __name__ == '__main__':
    main()