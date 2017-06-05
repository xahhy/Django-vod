from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )



class VodLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class VodPageNumberPagination(PageNumberPagination):
    page_size = 2
    