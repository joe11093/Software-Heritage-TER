import launchpadlib
from launchpadlib.launchpad import Launchpad

cachedir = "/home/anonbnr/.launchpadlib/cache/" #cache directory
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel') #logging in anonymously to the API (read-only)

projects = launchpad.projects[:100]

repos = []
for project in projects:
    project_repos = launchpad.git_repositories.getRepositories(target=project.self_link)
    if project_repos:
        repos.append(project_repos)

for project_repos in repos:
    for repo in project_repos:
    #data fields = resource_type_link, total_size, start, entries
    #associated objects = next and previous
    #other associated objects = total_size and entry_
    #no methods
        print('''
        {}:
        Data fields: {}

        Associated objects: {}

        Other associated objects: {}

        Methods: {}
        '''.format(repo, repo.lp_attributes, repo.lp_collections, repo.lp_entries, repo.lp_operations))

# print(
# """repo at {}
# ressource_type_link = {}
# total_size = {}
# start = {}
# entries = {}
# """.format(repo.resource_type_link, repo.total_size, repo.start, repo.entries))
