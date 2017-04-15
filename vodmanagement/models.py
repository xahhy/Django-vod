from django.db import models
from django.utils import timezone
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.utils.safestring import mark_safe

class VodManager(models.Manager):

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(VodManager, self)#.filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    VodModel = instance.__class__
    print('save')
    if VodModel.objects.count() is not 0:
        new_id = VodModel.objects.order_by("id").last().id + 1
    else:
        new_id = 0
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    print('save image')
    return "%s/%s" %(new_id, filename)
def default_description(instance):
    default=instance.title
    print(default)
    return 'The %s description'%default
# Create your models here.
class Vod(models.Model):
    title = models.CharField(max_length=120)
    # image = models.ImageField(upload_to=upload_location,
    #         null=True,
    #         blank=True,
    #         width_field="width_field",
    #         height_field="height_field")
    image = FilerImageField(null=True, blank=True,
                       related_name="image_name")
    video = FilerFileField(null=True,blank=True,related_name="video_name")
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=250,blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)#The first time added
    custome_time=models.DateTimeField(default=timezone.now)

    objects = VodManager()

    def save(self, *args, **kwargs):
        if self.description is None or self.description == "":
            self.description = default_description(self)
        # if not "http" in self.url:
        #     self.url = "http://" + self.url
        super(Vod, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="%s" width="150" height="200" />' % (self.image.url))


