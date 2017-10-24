from rest_framework.serializers import ModelSerializer
from epg.models import *
from vodmanagement.models import Record


class ChannelListSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'channel_id',
            'channel_name'
        ]


class ProgramListSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'channel',
            'title'
        ]

class ProgramDetailListSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'title',
            'start_time',
            'end_time',
            'video',
        ]


class ProgramDetailSerializer(ModelSerializer):
    video_list = ProgramDetailListSerializer(many=True)
    class Meta:
        model = Record
        fields = [
            'id',
            'channel',
            'start_time',
            'end_time',
            'video',
            'video_list'
        ]