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


    def search(self, table_idx, term, value):
        if table_idx == Table.USER:
            us = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.users)

            
            for u in us:
                # get assignee tickets 
                a_tickets = filter(lambda x: ('assignee_id' in x and '_id' in u) and (int(x['assignee_id']) == int(u['_id'])), self.tickets)

                subjects = []
                for at in a_tickets:
                    subjects.append(at['subject'])
                
                u['assigned_tickets'] = subjects

                # get submitted tickets
                s_tickets = filter(lambda x: ('submitter_id' in x and '_id' in u) and (int(x['submitter_id']) == int(u['_id'])), self.tickets)

                subjects = []
                for st in s_tickets:
                    subjects.append(st['subject'])
                
                u['submitted_tickets'] = subjects

                # get org name
                org = filter(lambda x: ('_id' in x and 'organization_id' in u) and (int(x['_id']) == int(u['organization_id'])), self.orgs)

                org_name = ''
                for o in org:
                    org_name = o['name']
                    break
                
                u['organization_name'] = org_name

            return us

        if table_idx == Table.TICKET:
            ts = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.tickets)

            for t in ts:
                # get assignee name 
                usrs = filter(lambda x: ('_id' in x and 'assignee_id' in t) and (int(x['_id']) == int(t['assignee_id'])), self.users)

                for u in usrs:
                    t['assignee_name'] = u['name'] if not isinstance(u['name'], unicode) else unicodedata.normalize('NFKD', u['name']).encode('ascii','ignore')
                    break

                # get submitter name
                usrs = filter(lambda x: ('_id' in x and 'submitter_id' in t) and (int(x['_id']) == int(t['submitter_id'])), self.users)

                for u in usrs:
                    t['submitter_name'] = u['name'] if not isinstance(u['name'], unicode) else unicodedata.normalize('NFKD', u['name']).encode('ascii','ignore')
                    break

                # get org name
                os = filter(lambda x: ('_id' in x and 'organization_id' in t) and (int(x['_id']) == int(t['organization_id'])), self.orgs)

                for o in os:
                    t['organization_name'] = o['name'] if not isinstance(o['name'], unicode) else unicodedata.normalize('NFKD', o['name']).encode('ascii','ignore')
                    break

            return ts

        if table_idx == Table.ORG:
            os = filter(lambda x: ((term in x) and (isinstance(x[term], unicode)) and (value in unicodedata.normalize('NFKD', x[term]).encode('ascii','ignore'))) \
                                or ((term in x) and (not isinstance(x[term], unicode)) and (value in str(x[term]))), self.orgs)

            for o in os:
                # get all tickets
                o_tickets = filter(lambda x: ('organization_id' in x and '_id' in o) and (int(x['organization_id']) == int(o['_id'])), self.tickets)

                subjects = []
                for ot in o_tickets:
                    if ot['subject'] not in subjects:
                        subjects.append(ot['subject'])
                    
                o['tikets'] = subjects

                # get all users
                usrs = filter(lambda x: ('organization_id' in x and '_id' in o) and (int(x['organization_id']) == int(o['_id'])), self.users)

                user_names = []
                for u in usrs:
                    if u['name'] not in user_names:
                        user_names.append(u['name'])

                o['users'] = user_names

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

