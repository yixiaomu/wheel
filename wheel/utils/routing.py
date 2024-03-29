# coding=utf8
#


def expose(url='/', methods=('GET', )):
    """
        Use this decorator to expose views in your views classes.

        `url`
            Relative URL for the view

        `methods`
            Allowed HTTP methods. By default on GET is allowed
    """
    def wrap(f):
        if not hasattr(f, '_urls'):
            f._urls = []
        f._urls.append((url, methods))
        return f

    return wrap