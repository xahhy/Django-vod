from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from epg.api.serializers import *
from vodmanagement.models import *

class ChannelListAPIView(ListAPIView):
    queryset = Channel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChannelListSerializer


class ProgramListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProgramListSerializer

    def get_queryset(self):
        programs = Record.objects.filter(active=1)
        channel = self.request.query_params.get('channel')
        if channel:
            programs = programs.filter(channel=channel)
        return programs


class ProgramDetailAPIView(RetrieveAPIView):
    lookup_field = 'id'
    permission_classes = [AllowAny]
    serializer_class = ProgramDetailSerializer
    queryset = Record.objects.all()
