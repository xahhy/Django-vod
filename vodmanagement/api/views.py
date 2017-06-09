from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from .serializers import *

from vodmanagement.models import *
from .pagination import *

class VodListAPIView(ListAPIView):
    serializer_class = VodListSerializer
    permission_classes = [AllowAny]
    pagination_class = VodPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Vod.objects.all() #filter(user=self.request.user)
        category = self.request.GET.get("category")
        if category:
            queryset_list = queryset_list.filter(category__name=category)
        # query = self.request.GET.get("q")
        # if query:
        #     queryset_list = queryset_list.filter(
        #             Q(title__icontains=query)|
        #             Q(content__icontains=query)|
        #             Q(user__first_name__icontains=query) |
        #             Q(user__last_name__icontains=query)
        #             ).distinct()
        search = self.request.GET.get("search")
        if search:
            queryset_list = queryset_list.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        

        return queryset_list


class VodDetailAPIView(RetrieveAPIView):
    queryset = Vod.objects.all()
    lookup_field = "id"
    serializer_class = VodDetailSerializer
    permission_classes = [AllowAny]

