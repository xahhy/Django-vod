from rest_framework.pagination import *
    # (
    # LimitOffsetPagination,
    # PageNumberPagination,
    # )



class VodLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class VodPageNumberPagination(PageNumberPagination):
    page_size = 3
    def get_paginated_response(self, data):
        year = self.request.query_params.get('year')
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('year',year),
            ('results', data)
        ]))


    