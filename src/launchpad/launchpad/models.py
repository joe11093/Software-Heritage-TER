from sqlalchemy import Column, String

from swh.lister.core.models import IndexingModelBase

class LaunchpadGitModel(IndexingModelBase):
  """a Launchpad git repository"""
  __tablename__ = "launchpad_git_repos"

  uid = Column(String, primary_key=True)
  indexable = Column(String, index=True)
