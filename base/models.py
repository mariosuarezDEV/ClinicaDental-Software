from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created', on_delete=models.PROTECT, null=False, blank=False)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated', on_delete=models.PROTECT, null=False, blank=False)
    status = models.BooleanField(default=True)
    class Meta:
        abstract = True