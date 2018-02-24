# coding: utf-8
"""
Pagination serializers determine the structure of the output that should
be used for paginated responses.
"""
from __future__ import unicode_literals
from base64 import b64encode, b64decode
from collections import namedtuple
from django.core.paginator import InvalidPage, Paginator as DjangoPaginator
from django.template import Context, loader
from django.utils import six
from django.utils.six.moves.urllib import parse as urlparse
from django.utils.translation import ugettext_lazy as _
#from rest_framework.compat import OrderedDict
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils.urls import (
    replace_query_param, remove_query_param
)
import warnings
from django.conf import settings

def _get_displayed_page_numbers(current, final):
    """
    This utility function determines a list of page numbers to display.
    This gives us a nice contextually relevant set of page numbers.

    For example:
    current=14, final=16 -> [1, None, 13, 14, 15, 16]

    This implementation gives one page to each side of the cursor,
    or two pages to the side when the cursor is at the edge, then
    ensures that any breaks between non-continous page numbers never
    remove only a single page.

    For an alernativative implementation which gives two pages to each side of
    the cursor, eg. as in GitHub issue list pagination, see:

    https://gist.github.com/tomchristie/321140cebb1c4a558b15
    """
    assert current >= 1
    assert final >= current

    if final <= 5:
        return list(range(1, final + 1))

    # We always include the first two pages, last two pages, and
    # two pages either side of the current page.
    included = set((
        1,
        current - 1, current, current + 1,
        final
    ))

    # If the break would only exclude a single page number then we
    # may as well include the page number instead of the break.
    if current <= 4:
        included.add(2)
        included.add(3)
    if current >= final - 3:
        included.add(final - 1)
        included.add(final - 2)

    # Now sort the page numbers and drop anything outside the limits.
    included = [
        idx for idx in sorted(list(included))
        if idx > 0 and idx <= final
    ]

    # Finally insert any `...` breaks
    if current > 4:
        included.insert(1, None)
    if current < final - 3:
        included.insert(len(included) - 1, None)
    return included

Cursor = namedtuple('Cursor', ['offset', 'reverse', 'position'])
PageLink = namedtuple('PageLink', ['url', 'number', 'is_active', 'is_break'])

PAGE_BREAK = PageLink(url=None, number=None, is_active=False, is_break=True)

def _get_page_links(page_numbers, current, url_func):
    """
    Given a list of page numbers and `None` page breaks,
    return a list of `PageLink` objects.
    """
    page_links = []
    for page_number in page_numbers:
        if page_number is None:
            page_link = PAGE_BREAK
        else:
            page_link = PageLink(
                url=url_func(page_number),
                number=page_number,
                is_active=(page_number == current),
                is_break=False
            )
        page_links.append(page_link)
    return page_links

class BasePagination(object):
    display_page_controls = False

    def paginate_queryset(self, queryset, request, view=None):  # pragma: no cover
        raise NotImplementedError('paginate_queryset() must be implemented.')

    def get_paginated_response(self, data):  # pragma: no cover
        raise NotImplementedError('get_paginated_response() must be implemented.')

    def to_html(self):  # pragma: no cover
        raise NotImplementedError('to_html() must be implemented to display page controls.')

    def get_results(self, data):
        return data['results']

class PageNumberPagination(BasePagination):
    """
    A simple page number based style that supports page numbers as
    query parameters. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100
    """
    # The default page size.
    # Defaults to `None`, meaning pagination is disabled.
    page_size = settings.PAGE_SIZE

    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = None

    last_page_strings = ('last',)

    template = 'rest_framework/pagination/numbers.html'

    invalid_page_message = _('Invalid page "{page_number}": {message}.')

    def _handle_backwards_compat(self, view):
        """
        Prior to version 3.1, pagination was handled in the view, and the
        attributes were set there. The attributes should now be set on
        the pagination class, but the old style is still pending deprecation.
        """
        assert not (
            getattr(view, 'pagination_serializer_class', None) or
            getattr(api_settings, 'DEFAULT_PAGINATION_SERIALIZER_CLASS', None)
        ), (
            "The pagination_serializer_class attribute and "
            "DEFAULT_PAGINATION_SERIALIZER_CLASS setting have been removed as "
            "part of the 3.1 pagination API improvement. See the pagination "
            "documentation for details on the new API."
        )

        for (settings_key, attr_name) in (
            ('PAGINATE_BY', 'page_size'),
            ('PAGINATE_BY_PARAM', 'page_size_query_param'),
            ('MAX_PAGINATE_BY', 'max_page_size')
        ):
            value = getattr(api_settings, settings_key, None)
            if value is not None:
                setattr(self, attr_name, value)
                warnings.warn(
                    "The `%s` settings key is pending deprecation. "
                    "Use the `%s` attribute on the pagination class instead." % (
                        settings_key, attr_name
                    ),
                    PendingDeprecationWarning,
                )

        for (view_attr, attr_name) in (
            ('paginate_by', 'page_size'),
            ('page_query_param', 'page_query_param'),
            ('paginate_by_param', 'page_size_query_param'),
            ('max_paginate_by', 'max_page_size')
        ):
            value = getattr(view, view_attr, None)
            if value is not None:
                setattr(self, attr_name, value)
                warnings.warn(
                    "The `%s` view attribute is pending deprecation. "
                    "Use the `%s` attribute on the pagination class instead." % (
                        view_attr, attr_name
                    ),
                    PendingDeprecationWarning,
                )

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self._handle_backwards_compat(view)

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = DjangoPaginator(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.count > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_html_context(self):
        base_url = self.request.build_absolute_uri()

        def page_number_to_url(page_number):
            if page_number == 1:
                return remove_query_param(base_url, self.page_query_param)
            else:
                return replace_query_param(base_url, self.page_query_param, page_number)

        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = _get_displayed_page_numbers(current, final)
        page_links = _get_page_links(page_numbers, current, page_number_to_url)

        return {
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link(),
            'page_links': page_links
        }

    def to_html(self):
        template = loader.get_template(self.template)
        context = Context(self.get_html_context())
        return template.render(context)