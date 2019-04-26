from sqlalchemy import Column, Boolean, Integer

from swh.lister.core.models import ModelBase

class LaunchpadGitModel(ModelBase):
  """a Launchpad git repository"""
  __tablename__ = "launchpad_git_repos"

  uid = Column(Integer, primary_key=True)
