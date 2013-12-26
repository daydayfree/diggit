# coding: utf-8

import unittest
from corelib.store import clear_db

class DiggitTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        clear_db()
        pass

