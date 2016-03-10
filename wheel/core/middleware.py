# coding=utf8
#


from werkzeug import url_decode


class HTTPMethodOverrideMiddleware(object):
    """
        The HTTPMethodOverrideMiddleware middleware implements the hidden HTTP
        method. Not all web browsers support every HTTP method, such as DELETE
        and PUT. So this middleware allows clients to provide a method override 
        parameter via an HTTP header value or a querystring parameter.
    """

    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])
    default_http_methods = ['GET', 'HEAD', 'POST', 'DELETE',
                            'PUT', 'PATCH', 'OPTIONS']

    def __init__(self, app, header_name=None,
                 querystring_param=None, allowed_methods=None):
        header_name = header_name or 'X-HTTP-METHOD-OVERRIDE'

        self.app = app
        self.header_name = 'HTTP_' + header_name.replace('-', '_')
        self.querystring_param = querystring_param or '__METHOD__'
        self.allowd_methods = frozenset(allowed_methods or default_http_methods)

    def _get_from_querystring(self, environ):
        if self.querystring_param in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            return args.get(self.querystring_param)

        return None

    def _get_method_override(self, environ):
        return environ.get(self.header_name) or \
                self._get_from_querystring(self.querystring_param) or ''

    def __call__(self, environ, start_response):
        method = self._get_method_override(environ).upper()

        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method

        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'

        return self.app(environ, start_response)