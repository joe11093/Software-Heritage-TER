# Copyright (C) 2017-2018 the Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import re
import time

from swh.lister.core.indexing_lister import SWHIndexingHttpLister
from swh.lister.launchpad.models import LaunchpadGitModel
from swh.lister.launchpad import LaunchpadProxy

class LaunchpadGitLister(SWHIndexingHttpLister):
    PATH_TEMPLATE = '/projects?ws_size=75&memo=%d&ws.start=%d'
    MODEL = LaunchpadGitModel
    API_URL_INDEX_RE = re.compile(r'^.*/projects\?ws.size=\d+&memo=\d+&ws.start=(\d+)')
    LISTER_NAME = 'launchpad_git'

    def __init__(self, api_baseurl=None, override_config=None):
        SWHIndexingHttpLister.__init__(self, api_baseurl=api_baseurl, override_config=override_config)
        self.api_proxy = LaunchpadProxy()
        self.api_proxy.login("SWH access", "production", "devel")

    def request_uri(self, identifier):
        """Get the full request URI given the transport_request identifier."""
        path = self.PATH_TEMPLATE % (identifier, identifier)
        return self.api_baseurl + path

    def get_next_target_from_response(self, response):
        try:
            if response.next_collection_link != None:
                next_url = response.next_collection_link
                return int(self.API_URL_INDEX_RE.match(next_url).group(1))
        except:
            return None

    def get_model_from_repo(self, repo):
        return{
            'indexable': repo['unique_name'],
			'uid': repo['unique_name'],
            'name': repo['name'],
            'full_name': repo['unique_name'],
            'html_url': repo['web_link'],
            'origin_url': repo['git_https_url'],
            'origin_type': 'git',
            'description': repo['description'],
		}

    def transport_response_simplified(self, response):
        repos = self.api_proxy.get_git_repos(response)
        return [self.get_model_from_repo(repo) for repo in repos]
