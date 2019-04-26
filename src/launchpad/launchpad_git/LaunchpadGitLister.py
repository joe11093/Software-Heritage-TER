
from swh.lister.core.lister_base import SWHListerBase
from swh.lister.launchpad_git.models import LaunchpadGitModel

class LaunchpadGitLister(SWHListerBase):
	MODEL = LaunchpadGitModel
	LISTER_NAME = 'launchpad_git'
	#PROXY = None

	def __init__(self, api_proxy, override_config=None):
		#instance of the proxy class
		self.api_proxy = api_proxy


	def transport_request(self, identifier):
		"""
		returns JSON of the object identified by identifier
		"""
		response = self.api_proxy.index[identifier]
		if response == None:
			raise FetchError(
				"Could not retrieve index for %s" % identifier
				)
		return response

	def transport_response_to_string(self, response):	
		"""
		returns a string version of the response of transport_request
		for logging purposes
		"""
		pass

	def transport_response_simplified(self, response):
		"""
		Convert the server response into list of a dict for each repo in the
            response, mapping columns in the lister's MODEL class to repo data.
		"""
		repos = response.json()
		return [self.get_model_from_repo(repo) for repo in repos]

	def get_model_from_repo(self, repo):
		return{
			'uid': repo['unique_name'], 
            'name': repo['name'],		
            'full_name': repo['unique_name'], 
            'html_url': repo['web_link'],	
            'origin_url': repo['git_https_url'], 
            'origin_type': 'git',			
            'description': repo['description'], 
		}

	def transport_quota_check(self, response):
		pass