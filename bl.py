from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import time
import logging
import json
import unicodedata

from log_utils import setup_logging


class Table:
    USER = 1
    TICKET = 2
    ORG = 3


class BL(object):

    def __init__(self, orgs, tickets, users):
        super(BL, self).__init__()
        setup_logging()
        self.logger = logging.getLogger()

        self.orgs = orgs
        self.tickets = tickets
        self.users = users


    def print_readable_data(self, data):
        print("""
        ----------------------------------
        """)
        for k, v in data.iteritems():
            print('{}: {}'.format(k, v))


    def search(self, table_idx, term, value):
        if table_idx == Table.USER:
            us = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.users)
            return us

        if table_idx == Table.TICKET:
            ts = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.tickets)
            return ts

        if table_idx == Table.ORG:
            os = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.orgs)

            for o in os:
                o_tickets = filter(lambda x: ('organization_id' in x) and (x['organization_id'] == int(o[term])), self.tickets)
                subjects = []
                for ot in o_tickets:
                    subjects.append(ot['subject'])
                    
                o['tikets'] = subjects

            return os

        return []

    def all_searchable_fields(self):
        print("""
        ----------------------------------
        Search Users with
        """)
        map(print, self.users[0].keys())
        print("""
        ----------------------------------
        Search Tickets with
        """)
        map(print, self.tickets[0].keys())
        print("""
        ----------------------------------
        Search Organizations with
        """)
        map(print, self.orgs[0].keys())

