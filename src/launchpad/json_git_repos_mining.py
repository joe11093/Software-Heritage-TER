import json
from time import time
from datetime import datetime

with open('../Resources/git_repos.json', 'r') as file:
    git_repos = json.load(file)
