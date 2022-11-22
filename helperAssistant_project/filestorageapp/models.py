import datetime

from cloudinary.models import CloudinaryField
from django.db import models
from django.conf import settings


# Create your models here.
class Files(models.Model):
    title = models.CharField(max_length=100, null=True)
    path = models.FileField(upload_to='test/', blank=True)
    # image = CloudinaryField('image')
    size = models.IntegerField(default=0)
    type = models.CharField(max_length=50, null=True)
    uploaded_time = models.DateTimeField(default=datetime.datetime.now())
    global_bool = models.BooleanField(default=False)
    # user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title