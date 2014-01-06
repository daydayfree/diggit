#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.factory import add_or_get_user


if __name__ == '__main__':
    add_or_get_user('unittest-user')

