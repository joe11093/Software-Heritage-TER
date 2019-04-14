from time import time
from datetime import datetime
import launchpadlib
from launchpadlib.launchpad import Launchpad

cachedir = "/home/anonbnr/.launchpadlib/cache/" #cache directory
launchpad = Launchpad.login_anonymously('just testing', 'production', cachedir, version='devel') #logging in anonymously to the API (read-only)

print("Started retrieving projects at {}".format(datetime.now()))
start_time = time()
projects = list(launchpad.projects)
print("Finished retrieving projects from API at {} (took {} seconds)".format(datetime.now(), time() - start_time))
total = len(projects)
print("Number of projects: {}".format(total))

bzr_ct = 0
git_ct = 0
none_ct = 0
others = []
other_ct = 0

print("\nStarted looping over projects to identify VCS types at {}".format(datetime.now()))
start_time = time()
for project in projects:
    if project.vcs == 'Git':
        git_ct += 1
    elif project.vcs == 'Bazaar':
        bzr_ct += 1
    elif project.vcs == None:
        none_ct += 1
    else:
        others.append(project.vcs)
        other_ct += 1
print("Finished looping over projects at {} (took {} seconds)".format(datetime.now(), time() - start_time))

print('\nNumber of git repositories : {} ({}%)'.format(git_ct, git_ct / total * 100))
print('Number of bzr repositories : {} ({}%)'.format(bzr_ct, bzr_ct / total * 100))
print('Number of repositories with no VCS : {} ({}%)'.format(none_ct, none_ct / total * 100))

print("\nOther types :")
for other in others:
    print(other)

print('\nNumber of repositories with other VCS : {} ({}%)'.format(other_ct, other_ct / total * 100))
