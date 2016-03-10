#!/usr/bin/env python
# coding=utf8
#


from flask.views import MethodView
from wheel.core.templates import render_template
from wheel.modules.authors.utils import get_author
from wheel.modules.authors.utils import get_authors
from wheel.modules.authors.utils import get_author_contents


class AuthorListView(MethodView):
    """
    Show a full list of authors
    """

    def get(self):
        return render_template('authors/list.html', authors=get_authors())


class AuthorView(MethodView):
    """
    Show specific author profile
    """

    def get(self, author_id):
        author = get_author(author_id)
        contents = get_author_contents(author)
        return render_template('authors/detail.html',
                               author=author, contents=contents)
