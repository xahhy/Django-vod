from django.db.models import Q
import itertools
from rest_framework.views import APIView
from vodmanagement.views import get_years
from rest_framework.response import Response
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
from .permissions import *


class VodListAPIView(ListAPIView):
    """
    VodListAPIView doc
    """
    serializer_class = VodListSerializer
    permission_classes = [AllowAny]
    pagination_class = VodPageNumberPagination  # PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Vod.objects.all()  # filter(user=self.request.user)
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
        # search year
        year = self.request.GET.get('year')
        if year is not None and year != "":
            queryset_list = queryset_list.filter(year=year)

        return queryset_list


class VodDetailAPIView(RetrieveAPIView):
    """
    VodDetailAPIView doc

    """
    queryset = Vod.objects.all()
    lookup_field = "id"
    serializer_class = VodDetailSerializer
    permission_classes = [HasPermission]


class CategoryListAPIView(ListAPIView):
    """
    CategoryListAPIView doc
    """
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    queryset = VideoCategory.objects.all()


class YearListAPIView(APIView):
    """
    YearListAPIView doc
    """
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        years = get_years()
        return Response(years)


class HomeListAPIView(APIView):
    """
    HomeListAPIView doc
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        preview_categories = []
        for category in VideoCategory.objects.all():
            videos = Vod.objects.filter(category__name=category.name)[:6]
            preview_categories.append(
                {
                    'category': category.name,
                    'videos': VodListSerializer(videos, many=True).data
                }
            )
        return Response(preview_categories)
