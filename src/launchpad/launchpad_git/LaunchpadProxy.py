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
The class LaunchpadProxy can be viewed as a specific implementation of a more generic class APIProxy
which will later be implemented.

The class offers all the necessary methods to ingest the origins of all
publicly accessible git-based projects into the SWH archive. The publicly accessible git-based
launchpad projects constitute around 5% of all publicly accessible launchpad projects
(around 3000 projects).

An extensible design is implemented to allow for future ingesting of non-git based projects,
mainly Bazaar-git based projects, which constitute around 59% of all Launchpad projects
(around 25300 projects).

Note: Up till April 2019, around 35% of all publicly accessible projects on Launchpad (around 14,700)
are without VCS
"""

#Constants used to configure and parameterize the behavior of the LaunchpadProxy class
__launchpad = None
GIT_REPO_ID = "unique_name"
GIT_VCS = "Git"
DEFAULT_JSON_PATH = "index.json"
DEFAULT_JSON_INDENT = 4

class LaunchpadProxy:
    """
    A Launchpad Proxy class encapsulating a launchpad API client instance.
    It requires a cache directory where all fetched projects, collections and activities are logged
    as JSON objects.

    The class is used to request the metadata of all publicly accessible launchpad projects.
    As an initial implementation, we will focus mainly on the retrieval of git-based projects
    and the ingestion of their origins, since a git loader is already in place, whereas a Bazaar loader
    is yet to be implemented by the SWH community.

    The API client instance abstracts away all the transport details from the Launchpad lister, and
    thus no direct API requests/reponses are required from a Launchpad lister to fetch the origins'
    metadata.

    An anonymous login (read-only) is required by the API client instance to access the launchpad API.
    Upon connection, it can fetch top level collections such as projects, git repositories, etc.
    (cf. https://api.launchpad.net/devel/ for further details)

    Upon retrieving all publicly accessible git-based launchpad projects, the proxy can fetch
    the associated git repositories collections, from which it can extract the git origins entries
    to build an index.

    The index is queried by the Launchpad lister to fetch information about git origins and
    schedule the proper tasks necessary to ingest them later on into the SWH archive.
    All entries in the index have the form <GIT_REPO_ID, JSON representation of git repo>

    A function is defined to export the extracted git entries into a local file
    with a specific path and format (by default JSON format).

    An importation function is also defined to import a list of git entries, previously exported
    into a file.

    Consequently, an index can be constructed either directly from the exported file (lazy approach)
    or by updating the exported file's contents prior to the construction (greedy approach).
    """

    def __init__(self, cache_dir):
        """
        create a launchpad proxy instance, using a cache directory path
        and initialize the index as an empty dictionary
        """

        self.cache_dir = cache_dir
        self.index = {}

    def login(self, id, mode, version):
        """
        login anonymously (read-only) to the launchpad API via the
        launchpad API client instance, specifying id, mode and API version
        """

        __launchpad = Launchpad.login_anonymously(id, mode, self.cache_dir, version=version)

    def get_all_projects(self):
        """
        fetch all projects of launchpad using the launchpad API client instance

        Cannot be used before logging in
        """

        return __launchpad.projects

    def get_projects(self, vcs=GIT_VCS):

        """
        fetch publicly accessible launchpad projects using the launchpad API client instance
        having a specific vcs (by default vcs = git)

        Cannot be used before logging in
        """

        for project in self.get_all_projects():
            if project.vcs == vcs:
                yield project

    def get_git_repos(self):
        """
        fetch all git repositories collections associated to publicly accessible launchpad
        git-based projects using the launchpad API client instance.

        Cannot be used before logging in.
        """

        for project in self.get_projects(vcs=GIT_VCS):
            yield __launchpad.git_repositories.getRepositories(target=project.self_link)

    def get_git_entries(self):
        """
        fetch all git entries associated to git repositories collections of publicly
        accessible launchpad git-based projects using the launchpad API client instance.

        Returns a list of git entries.
        Cannot be used before logging in.
        """

        git_entries = []
        for git_repos in self.get_git_repos():
            for git_entry in git_repos.entries:
                if git_entry != None and not git_entry in git_entries:
                    git_entries.append(git_entry)

        return git_entries

    def export_git_entries(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        export all unique git entries of publicly accessible git-based launchpad projects
        into a file having a specific format (by default, format = JSON) at a specific path

        Cannot be used before logging in.
        """

        git_entries = self.get_git_entries()
        if format == "json":
            with open(path, 'w') as file:
                json.dump(git_entries, file, indent=DEFAULT_JSON_INDENT)

        return git_entries

    def import_git_entries(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        import all the previously exported unique git entries of publicly accessible
        git-based launchpad projects  from a file having a specific format (by default, format = JSON)
        at a specific path.

        Cannot be used before logging in.
        """

        if format == "json":
            with(open(path, 'r')) as file:
                return json.load(file)

    def __build_index(self, git_entries):
        """
        a private method that abstracts away the details of index building

        Must not be called explicitly.
        """

        for git_entry in git_entries:
            self.index[git_entry[GIT_REPO_ID]] = git_entry

    def lazy_index_build(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        build an index of all unique git entries associated to publicly accessible git-based
        launchpad projects, previously exported into a file having a specific format
        (by default format = JSON)
        with a specific path

        Cannot be used before logging in.
        """

        git_entries = self.import_git_entries(path, format=format)
        self.__build_index(git_entries)

    def greedy_index_build(self, path=DEFAULT_JSON_PATH, format="json"):
        """
        build an index of all unique git entries associated to publicly accessible git-based
        launchpad projects, but update the contents of the exported file from which
        to build the index prior to building.

        Cannot be used before logging in.
        """

        git_entries = self.export_git_entries(path, format)
        self.__build_index(git_entries)

    def index_head(self, n=10, format="json"):
        """
        display the first n (by default, n = 10) lines of the built index
        in a specific format (by default, format = JSON)

        Cannot be used before logging in and before the index is built.
        """

        output = """
        Length of index: {}
        First {} entries of the index:\n
        """.format(len(self.index), n)

        if format == "json":
            for index, entry in enumerate(self.index.items()):
                if index > n:
                    break
                output += "{}: {}\n".format(entry[0], json.dumps(entry[1], indent=DEFAULT_JSON_INDENT))

        print(output)

#TESTING THE PROXY CLASS
if(__name__ == '__main__'):

    cache_dir = '/home/anonbnr/.launchpadlib/cache/'
    json_path = 'launchpad_git_repos.json'

    ##Creating the proxy
    print("Creating Launchpad proxy instance at {}".format(datetime.now()))
    start_time = time()
    proxy = LaunchpadProxy(cache_dir)
    print("Created at {} (took {} seconds)".format(datetime.now(), time() - start_time))

    ##Logging in to the API using the proxy
    print("\nLogging in at {}".format(datetime.now()))
    start_time = time()
    proxy.login("SWH access", "production", "devel")
    print("Logged in at {} (took {} seconds)".format(datetime.now(), time() - start_time))

    ##Greedy index building
    print("\nGreedy index building at {}".format(datetime.now()))
    start_time = time()
    proxy.greedy_index_build(json_path)
    print("Built at {} (took {} seconds)".format(datetime.now(), time() - start_time))
    proxy.index_head()

    ##Lazy index building
    print("\nLazy index building at {}".format(datetime.now()))
    start_time = time()
    proxy.lazy_index_build(json_path)
    print("Built at {} (took {} seconds)".format(datetime.now(), time() - start_time))
    proxy.index_head()
