from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikedItemManager(models.Manager):
    def get_like_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return LikedItem.objects.select_related('user').filter(content_type=content_type, object_id=obj_id)


class LikedItem(models.Model):
    objects = LikedItemManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return self.user.first_name
