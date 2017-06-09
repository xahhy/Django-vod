from rest_framework import serializers
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )
from vodmanagement.models import *


class VodListSerializer(ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )

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

    def get_category(self,obj):
        return str(obj.category)


class VodDetailSerializer(ModelSerializer):
    # category = SerializerMethodField()
    definition = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Vod
        fields = [
            'title',
            'image',
            'video',
            'category',
            'description',
            'definition',
        ]

    def get_category(self,obj):
        return str(obj.category)