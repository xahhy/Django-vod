from django.db.models import Q
import itertools
from rest_framework.views import APIView
from wrapcache import wrapcache

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


# @wrapcache(10 * 60)
def get_all_videos(main_category):
    if main_category:
        return Vod.objects.filter(category__subset__name=main_category)
    return Vod.objects.all()


@wrapcache(10 * 60)
def get_filter_videos(query_set, category=None, year=None, region=None):
    if category:query_set = query_set.filter(category__name=category)
    if year:query_set = query_set.filter(year=year)
    if region:query_set = query_set.filter(region__name=region)
    return query_set


def checked_query_param(param:str):
    return param if (param != '全部' and param != '') else None


class VodListAPIView(ListAPIView):
    """
    VodListAPIView doc
    """
    serializer_class = VodListSerializer
    permission_classes = [AllowAny]
    pagination_class = VodPageNumberPagination  # PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        main_category = self.request.query_params.get('main_category')
        queryset_list = get_all_videos(main_category)
        category = checked_query_param(self.request.query_params.get('category'))
        year = checked_query_param(self.request.query_params.get('year'))
        region = checked_query_param(self.request.query_params.get('region'))
        queryset_list = get_filter_videos(queryset_list, category=category, year=year, region=region)
        # query = self.request.GET.get("q")
        # if query:
        #     queryset_list = queryset_list.filter(
        #             Q(title__icontains=query)|
        #             Q(content__icontains=query)|
        #             Q(user__first_name__icontains=query) |
        #             Q(user__last_name__icontains=query)
        #             ).distinct()
        search = self.request.GET.get("search")
        if search is not None and search != '':
            queryset_list = queryset_list.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset_list


class VodDetailAPIView(RetrieveAPIView):
    """
    VodDetailAPIView doc

    """
    # queryset = Vod.objects.all()
    lookup_field = "id"
    serializer_class = VodDetailSerializer
    permission_classes = [HasPermission]

    def get_queryset(self, *args, **kwargs):
        query_set =  Vod.objects.filter(active=1)
        return query_set


@wrapcache(1)
def gen_categories():
    print('Gen Categories')
    categories = {}
    for level_1 in VideoCategory.objects.filter(level=1):
        children = level_1.subset.all()
        categories[level_1.name] = CategoryListSerializer(children, many=True).data
    return categories


class CategoryListAPIView(APIView):
    """
    CategoryListAPIView doc
    """
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny]
    queryset = VideoCategory.objects.all()

    def get(self, request, format=None):
        return Response(gen_categories())


# class YearListAPIView(APIView):
#     """
#     YearListAPIView doc
#     """
#     permission_classes = [AllowAny]
#     def get(self, request, format=None):
#         """
#         Return a list of all years associate with 'Category'.
#         """
#         category = request.query_params.get('category')
#         years = get_years(category)
#         return Response(years)
class YearListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        category = self.request.query_params.get('category')
        if category is None:
            return Response('Error. The category parameter should be one of the level-1 categories', 500)
        year_list = get_years(category)
        return Response(year_list)


class RegionListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegionListSerializer

    def get_queryset(self, *args, **kwargs):
        return VideoRegion.objects.all()


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
