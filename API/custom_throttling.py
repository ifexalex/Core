from rest_framework.throttling import UserRateThrottle,ScopedRateThrottle

class CustomThrottle(ScopedRateThrottle):

    """
    If the user is authenticated, use the `from_` field in the request data as the cache key. Otherwise,
    use the `get_ident` function
    
    :param request: The request object
    :param view: The view instance that is being called
    :return: The cache key.
    """

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.data.get('from_')
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }