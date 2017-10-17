from rest_framework import serializers
from rest_framework.serializers import *
# (
#     HyperlinkedIdentityField,
#     ModelSerializer,
#     SerializerMethodField
#     )
from vodmanagement.models import *
from easy_thumbnails.files import get_thumbnailer


class VodListSerializer(ModelSerializer):
    # category = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='name'
    #  )
    image = SerializerMethodField()
    category = SerializerMethodField()

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

    def get_category(self, obj):
        return str(obj.category)

    def get_image(self, obj):
        thumb_url = get_thumbnailer(obj.image)['avatar'].url
        return thumb_url


class VodDetailSubSetSerializer(ModelSerializer):
    class Meta:
        model = Vod
        fields = [
            'title',
            'description',
            'video'
        ]


class VodDetailSerializer(ModelSerializer):
    """
    VodDetailSerializer doc

    """
    # category = SerializerMethodField()
    definition = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    # video_list = serializers.SerializerMethodField()
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


# Category Serializers
class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = ['name']


class RegionListSerializer(ModelSerializer):
    class Meta:
        model = VideoRegion
        fields = ['name']


# class HomeListSerializer(Serializer):
#     videos = VodListSerializer()
#     category = CategoryListSerializer()
