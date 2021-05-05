from django.db import models
from Data_manage.models import WeldSpot
# Create your models here.


class AppDataset(models.Model):
    spot_id = models.ForeignKey('WeldSpot', on_delete=models.CASCADE),
    file_name = models.CharField(max_length=64, null=True, default='')
    folder = models.CharField(max_length=64, null=True, default='')
    type = models.IntegerField()

