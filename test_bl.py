#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import unittest
import json

from bl import BL, Table

class TestBL(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBL, self).__init__(*args, **kwargs)

    def setUp(self):
        self.orgs = json.loads(
            """
            [
                {
                    "_id": 1
                }
            ]
            """
        )
        self.tickets = json.loads(
            """
            [
                {
                    "_id": 2
                }
            ]
            """
        )
        self.users = json.loads(
            """
            [
                {
                    "_id": 3
                }
            ]
            """
        )
        self.bl = BL(self.orgs, self.tickets, self.users)
        

    def tearDown(self):
        pass


    def test_search_users(self):
        actual = self.bl.search(Table.USER, '_id', '1')
        expected = 0
        self.assertEqual(expected, len(actual))

        actual = self.bl.search(Table.USER, '_id', '3')
        expected = 1
        self.assertEqual(expected, len(actual))


if __name__ == '__main__':
    unittest.main()