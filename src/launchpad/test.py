import json
from launchpadlib.launchpad import Launchpad

cachedir = "/home/anonbnr/.launchpadlib/cache/"
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel')

projects = launchpad.projects[:100]
repos = []
for project in projects:
    project_repos = launchpad.git_repositories.getRepositories(target=project.self_link)
    if project_repos:
        repos.append(project_repos)

for repo in repos:
    print(repo)
