from .abstractattribute import AbstractAttribute

class WebApiProxy(abc.ABC):
    """
    WebApiProxy interface, providing a git repositories retrieval task
    interface for all concrete Web API classes to implement
    """

    @abc.abstractmethod
    def login(**kwargs):
        """Given logging in parameters to configure logging in to the API, try to login (anonymously or with authentication)
        and send back the client proxy instance obtained upon success

        Implementation of this method determines the network request protocol

        Args:
            kwargs: keyword parameters, used to configure the logging in process to the API
            such as id, mode, version, etc.
        Returns:
            the client proxy instance
        """
        pass

    @abc.abstractmethod
    def get_git_repos(self, response):
        """Given a response to a target endpoint identifier query, try to retrieve all unique git repositories associated with the target.

        Implementation of this method determines the network request protocol.

        Args:
            response: an abstract attribute whose type determines the process of
            git repos retrieval
                e.g. If the service offers an endpoint for retrieval of repositories
                collectively, then this response would contain a paginated/indexed response for example
        Returns:
            the entire list of repositories
        """
        pass

    @abc.abstractmethod
    def export_git_repos(self, path, format):
        """Try to export git repos into a file having a format"""
        pass

    @abc.abstractmethod
    def import_git_repos(self, path, format):
        """Try to import all the previously exported unique git repositories
        from a file having a specific format at a specific path."""
        pass
