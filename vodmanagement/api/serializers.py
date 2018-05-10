from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from easy_thumbnails.files import get_thumbnailer

from vodmanagement.models import Vod, VideoCategory, VideoRegion
from vodmanagement.utils import try_or_error


class VodListSerializer(ModelSerializer):
    image = SerializerMethodField()
    category = SerializerMethodField()
    definition = SerializerMethodField()

    class Meta:
        model = Vod
        fields = [
            'id',
            'title',
            'image',
            'category',
            'definition',
            'duration',
            'slug',
        ]

    @try_or_error
    def get_definition(self, obj):
        return obj.get_definition_display()

    @try_or_error
    def get_category(self, obj):
        return obj.category.name

    @try_or_error
    def get_image(self, obj):
        thumb_url = get_thumbnailer(obj.image)['avatar'].url
        return thumb_url


class VodHomeListSerializer(ModelSerializer):
    image = SerializerMethodField()
    category = SerializerMethodField()
    definition = SerializerMethodField()

    class Meta:
        model = Vod
        fields = [
            'id',
            'title',
            'image',
            'category',
            'definition',
            'duration',
            'slug',
        ]

    @try_or_error
    def get_definition(self, obj):
        return obj.get_definition_display()

    @try_or_error
    def get_category(self, obj):
        return obj.category.name

    @try_or_error
    def get_image(self, obj):
        thumb_url = get_thumbnailer(obj.image)['big_avatar'].url
        return thumb_url


class VodDetailSubSetSerializer(ModelSerializer):
    class Meta:
        model = Vod
        fields = [
            'title',
            'description',
            'video',
            'select_name'
        ]


class VodDetailSerializer(ModelSerializer):
    """
    VodDetailSerializer doc

    """
    definition = SerializerMethodField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    video_list = VodDetailSubSetSerializer(many=True)

    class Meta:
        model = Vod
        fields = [
            'title',
            'image',
            'video',
            'category',
            'description',
            'definition',
            'video_list'
        ]

    def get_category(self, obj):
        return str(obj.category)

    def get_definition(self, obj):
        return obj.get_definition_display()


# Category Serializers
class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ['name']


class RegionListSerializer(ModelSerializer):
    class Meta:
        model = VideoRegion
        fields = ['name']
