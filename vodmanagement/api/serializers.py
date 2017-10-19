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
        try:
            thumb_url = get_thumbnailer(obj.image)['avatar'].url
        except:
            thumb_url = 'Error'
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

"""
Backup Serializers
"""
class VideoBackupSubsetSerializer(ModelSerializer):
    category1 = serializers.SerializerMethodField()
    category2 = serializers.SerializerMethodField()
    class Meta:
        model = Vod
        fields = [
            'title',
            'image',
            'video',
            'definition',
            'save_path',
            'year',
            'description',
            'category1',
            'category2',
            'region'
        ]

    def get_category1(self, obj):
        level_1 = VideoCategory.objects.filter(subset__name=obj.category.name)
        return level_1.first().name

    def get_category2(self, obj):
        return obj.category.name

class VideoBackupSerializer(ModelSerializer):
    video_list = VideoBackupSubsetSerializer(many=True)
    category1 = serializers.SerializerMethodField()
    category2 = serializers.SerializerMethodField()
    class Meta:
        model = Vod
        fields = [
            'title',
            'image',
            'video',
            'definition',
            'save_path',
            'year',
            'description',
            'category1',
            'category2',
            'region',
            'video_list'
        ]

    def get_category1(self, obj):
        level_1 = VideoCategory.objects.filter(subset__name=obj.category.name)
        return level_1.first().name

    def get_category2(self, obj):
        return obj.category.name
# class HomeListSerializer(Serializer):
#     videos = VodListSerializer()
#     category = CategoryListSerializer()
