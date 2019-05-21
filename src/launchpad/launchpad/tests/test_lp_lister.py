# Copyright (C) 2017-2018 the Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import re
import unittest

from swh.lister.launchpad.lister import LaunchpadGitLister
from swh.lister.core.tests.test_lister import HttpListerTester


class LaunchpadListerTester(HttpListerTester, unittest.TestCase):
    Lister = LaunchpadGitLister
    test_re = re.compile(r'^.*/projects\?ws.size=\d+&memo=\d+&ws.start=(\d+)')
    lister_subdir = 'launchpad'
    good_api_response_file = 'api_response.json'
    bad_api_response_file = 'api_empty_response.json'
    first_index = 0
    last_index = 180
    entries_per_page = 75
