from django.db import models


class Channel(models.Model):
    channel_id = models.CharField(max_length=50, unique=True)
    channel_name = models.CharField(max_length=50, null=True, blank=True)
    rtmp_url = models.CharField(max_length=100, null=True, blank=True)
    active = models.IntegerField(null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    PID = models.IntegerField(null=True, blank=True)
    PGID = models.IntegerField(null=True, blank=True)
    client_ip = models.CharField(max_length=50, null=True, blank=True)
    sort = models.IntegerField(null=False, blank=True, default=0)

    class Meta:
        managed = False
        db_table = 'channel'
        verbose_name = '频道'
        verbose_name_plural = '频道管理'

    def __str__(self):
        return self.channel_name + '(' + self.channel_id + ')'


class Program(models.Model):
    channel = models.ForeignKey(Channel, to_field='channel_id', null=True)
    start_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    finished = models.IntegerField(null=True, blank=True, default=0)
    event_id = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'program'
        verbose_name = '节目'
        verbose_name_plural = '节目管理'

    def __str__(self):
        return str(self.channel) + ':' + self.title
