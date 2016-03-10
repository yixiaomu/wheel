# coding=utf8
#


from wheel.core.app import WheelModule
from wheel.modules.authors.views import AuthorListView, AuthorView
from wheel.modules.authors.utils import get_author
from wheel.modules.authors.utils import get_authors
from wheel.modules.authors.utils import get_author_contents


module = WheelModule("authors", __name__, template_folder="templates")
module.add_url_rule('/author/<author_id>/',
                    view_func=AuthorView.as_view('author'))
module.add_url_rule('/authors/',
                    view_func=AuthorListView.as_view('authors'))
module.add_app_template_global(get_author)
module.add_app_template_global(get_authors)
module.add_app_template_global(get_author_contents)
