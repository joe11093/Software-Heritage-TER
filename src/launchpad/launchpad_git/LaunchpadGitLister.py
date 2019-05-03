import os
from time import time
from datetime import datetime

from swh.lister.core.lister_base import SWHListerBase
from swh.lister.launchpad_git.models import LaunchpadGitModel
from swh.lister.launchpad_git import LaunchpadProxy, DEFAULT_JSON_PATH

class LaunchpadGitLister(SWHListerBase):
	MODEL = LaunchpadGitModel
	LISTER_NAME = 'launchpad_git'
	#PROXY = None

	def __init__(self, override_config=None):
		#calling the parent constructor
		SWHListerBase.__init__(self, override_config)
		#instance of the proxy class
		self.api_proxy = new LaunchpadProxy()
		#logging in anonymously to the launchpad API
		self.api_proxy.login("SWH access", "production", "devel")
		#calling the proxy's indexing method
		#will call the right index building based on whether the index file exists or not
		if(os.path.isfile(DEFAULT_JSON_PATH)):
			print("\nLazy index building at {}".format(datetime.now()))
		    start_time = time()
		    self.api_proxy.lazy_index_build()
		    print("Built at {} (took {} seconds)".format(datetime.now(), time() - start_time))
		else:
			print("\nGreedy index building at {}".format(datetime.now()))
    		start_time = time()
    		self.api_proxy.greedy_index_build()
    		print("Built at {} (took {} seconds)".format(datetime.now(), time() - start_time))
    	#REMOVE THIS PART
    	#printing the first n elements of the index
    	self.api_proxy.index_head(n=2)


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
		for logging purposes.
		We don't need this function as we aren't logging.
		"""
		pass

	def transport_response_simplified(self, response):
		"""
		Convert the server response into list of a dict for each repo in the
            response, mapping columns in the lister's MODEL class to repo data.
		"""
		return [self.get_model_from_repo(response)]

	def get_model_from_repo(self, repo):
		'''
		gets the needed fields from the repo object
		'''
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
		'''
		Handles the server quota. We don't need this as we don't have a server.
		'''
		pass