import json
from time import time
from datetime import datetime
import launchpadlib
from launchpadlib.launchpad import Launchpad

##Installing the launchpad client library
##########################################
##sudo apt install python-launchpadlib (Ubuntu)

"""
Launchpad Proxy module containing all the necessary elements to create a Launchpad API Proxy,
encapsulating an API client instance.
The class LaunchpadProxy can be viewed as a specific implementation of a more generic class WebApiProxy
which will later be implemented.

The class offers all the necessary methods to retrieve the origins of all
publicly accessible git-based projects and forward them to the LaunchpadGitLister. The publicly accessible git-based
launchpad projects constitute around 5% of all publicly accessible launchpad projects
(around 3000 projects).

An extensible design is implemented to allow for future retrieval of non-git based projects,
mainly Bazaar-based projects, which constitute around 59% of all Launchpad projects
(around 25300 projects).

Note: Up till April 2019, around 35% of all publicly accessible projects on Launchpad (around 14,700)
are without VCS
"""

#Constants used to configure and parameterize the behavior of the LaunchpadProxy class
__launchpad = None
GIT_REPO_ID = "unique_name"
GIT_VCS = "Git"
DEFAULT_CACHE_PATH = ".launchpadlib/cache/"
DEFAULT_JSON_PATH = "index.json"
DEFAULT_JSON_INDENT = 4

class LaunchpadProxy:
    """
    A Launchpad Proxy class encapsulating a launchpad API client instance.
    It requires a cache directory where all fetched projects, collections and activities are cached

    The class is used to retrieve the git origins of publicly accessible launchpad projects, according to the response
    forwarded by the LaunchpadGitLister upon requesting a target endpoint URI with transport_request().
    As an initial implementation, we will focus mainly on the retrieval of git-based projects
    and the ingestion of their origins, since a git loader is already in place, whereas a Bazaar loader
    is yet to be implemented by the SWH community.

    Upon fetching the origins' metadata, the API client instance abstracts away all the transport details from the Launchpad lister.

    An anonymous login (read-only) is required by the API client instance to access the launchpad Web API.
    Upon connection, it can fetch top level collections such as projects, git repositories, etc.
    (cf. https://api.launchpad.net/devel/ for further details)

    Upon retrieving all publicly accessible git-based launchpad projects, the proxy can fetch
    the associated git repositories collections, from which it can extract the git origins entries
    and forward them to the Lister which will map them to their model and schedule tasks for their
    ingestion.

    A function is defined to export the extracted git entries into a local file
    with a specific path and format (by default JSON format).

    An importation function is also defined to import a list of git entries, previously exported
    into a file.
    """

    def __init__(self, cache_dir=DEFAULT_CACHE_PATH):
        """create a launchpad client proxy instance, using a cache directory path"""
        self.cache_dir = cache_dir

    def login(self, id, mode, version):
        """
        login anonymously (read-only) to the launchpad API via the
        launchpad client instance, specifying id, mode and API version
        """

        __launchpad = Launchpad.login_anonymously(id, mode, self.cache_dir, version=version)

    # def get_all_projects(self):
    #     """
    #     fetch the top level API publicly accessible projects collection, using the Launchpad client instance
    #
    #     Cannot be used before logging in
    #     """
    #
    #     return __launchpad.projects
    #
    # def get_projects(self, projects, vcs=GIT_VCS):
    #
    #     """
    #     fetch publicly accessible git-based launchpad projects, using the Launchpad client instance
    #     having a specific vcs (by default vcs = git)
    #
    #     Cannot be used before logging in
    #     """
    #
    #     for project in projects:
    #         if project.vcs == vcs:
    #             yield project

    def get_git_repos_collections(self, project):
        """
        fetch all git repositories collections of a publicly accessible
        git-based launchpad project using the launchpad client instance.

        Cannot be used before logging in.
        """

        return __launchpad.git_repositories.getRepositories(target=project.self_link)


    def get_git_repos(self, response):
        """
        fetch all the unique git repositories' entries from all
        git repositories collections from a list of publicly
        accessible launchpad git-based projects, encapsulated in a
        JSON response, using the launchpad client instance.

        Returns a list of git repositories.
        Cannot be used before logging in and prior to issuing a network request.
        """

        git_repos = []
        for project in response.entries:
            if project.vcs == "Git":
                for git_collection in self.get_git_repos_collections(response):
                    for git_repo in git_collection.entries:
                        if git_repo != None and not git_repo in git_repos:
                            git_repos.append(git_repo)

        return git_repos

    def export_git_entries(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        export all unique git repositories of publicly accessible git-based launchpad projects
        into a file having a specific format (by default, format = JSON) at a specific path

        Cannot be used before logging in.
        """

        git_repos = self.get_git_repos()
        if format == "json":
            with open(path, 'w') as file:
                json.dump(git_repos, file, indent=DEFAULT_JSON_INDENT)

        return git_repos

    def import_git_entries(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        import all the previously exported unique git repositories of publicly accessible
        git-based launchpad projects from a file having a specific format (by default, format = JSON)
        at a specific path.

        Cannot be used before logging in.
        """

        if format == "json":
            with(open(path, 'r')) as file:
                return json.load(file)

#TESTING THE PROXY CLASS
# if(__name__ == '__main__'):
#
#     cache_dir = '/home/anonbnr/.launchpadlib/cache/'
#     json_path = 'launchpad_git_repos.json'
#
#     ##Creating the proxy
#     print("Creating Launchpad proxy instance at {}".format(datetime.now()))
#     start_time = time()
#     proxy = LaunchpadProxy(cache_dir)
#     print("Created at {} (took {} seconds)".format(datetime.now(), time() - start_time))
#
#     ##Logging in to the API using the proxy
#     print("\nLogging in at {}".format(datetime.now()))
#     start_time = time()
#     proxy.login("SWH access", "production", "devel")
#     print("Logged in at {} (took {} seconds)".format(datetime.now(), time() - start_time))
