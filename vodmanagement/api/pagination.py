from rest_framework.pagination import *
# (
# LimitOffsetPagination,
# PageNumberPagination,
# )
from vodmanagement.pagination import *
from wrapcache import wrapcache

from vodmanagement.utils import func_time


class VodLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class VodPageNumberPagination(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        year = self.request.query_params.get('year')
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('cur_page', self.page.number),
            ('num_pages', self.paginator.num_pages),
            ('page_range', self.paginator.pager_num_range()),
            ('year', year),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        page_size = self.get_page_size(request)
        if not page_size:
            return None
        cur_page = request.query_params.get(self.page_query_param)
        if not cur_page:
            cur_page = 1
        # paginator = self.django_paginator_class(queryset, page_size)
        self.paginator = CustomPaginator(cur_page, 5, queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = self.paginator.num_pages

        try:
            self.page = self.paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if self.paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
