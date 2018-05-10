from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from epg.api.serializers import *


class ChannelListAPIView(ListAPIView):
    queryset = Channel.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ChannelListSerializer
