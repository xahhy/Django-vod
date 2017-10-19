from rest_framework.serializers import ModelSerializer
from epg.models import *

class ChannelListSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            'channel_id',
            'channel_name'
        ]


class ProgramListSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'channel',
            'start_time',
            'end_time',
            'url',
            'title'
        ]