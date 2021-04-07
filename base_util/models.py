from django.db import models
from django.contrib.auth.models import User
from river.models.fields.state import  StateField
# Create your models here.
class Base(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_createdby_set")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_updatedby_set",blank=True,null=True)
    updated_on = models.DateTimeField(blank=True,null=True)
    status=StateField()
    # history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True