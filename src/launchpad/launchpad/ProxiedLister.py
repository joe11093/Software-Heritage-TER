from .abstractattribute import AbstractAttribute

PROXY = AbstractAttribute("Any class that implements WebApiProxy")

class ProxiedLister(SWHListerBase):
    """
    Lister encapsulating a Web API proxy instance, to retrieve origins metadata
    and abstract away some of the transport details while doing so
    """
