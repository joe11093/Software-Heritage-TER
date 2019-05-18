import random

from celery import group
from swh.scheduler.celery_backend.config import app

from swh.lister.launchpad_git.lister import LaunchpadGitLister

# GROUP_SPLIT = 10000


def new_lister(api_baseurl='https://api.launchpad.net/devel'):
    return LaunchpadGitLister()

@app.task(name=__name__ + '.IncrementalLaunchpadGitLister')
def incremental_launchpad_git_lister():
    lister = new_lister()
    lister.run(min_bound=lister.db_last_index(), max_bound=None)


@app.task(name=__name__ + '.RangeLaunchPadGitLister')
def range_launchpad_git_lister(start, end):
    lister = new_lister()
    lister.run(min_bound=start, max_bound=end)


@app.task(name=__name__ + '.FullGitHubRelister', bind=True)
def full_github_relister(self, split=None, **lister_args):
    lister = new_lister(**lister_args)
    ranges = lister.db_partition_indices(split or GROUP_SPLIT)
    random.shuffle(ranges)
    promise = group(range_github_lister.s(minv, maxv, **lister_args)
                    for minv, maxv in ranges)()
    self.log.debug('%s OK (spawned %s subtasks)' % (self.name, len(ranges)))
    try:
        promise.save()  # so that we can restore the GroupResult in tests
    except (NotImplementedError, AttributeError):
        self.log.info('Unable to call save_group with current result backend.')
    return promise.id


@app.task(name=__name__ + '.ping')
def ping():
    return 'OK'
