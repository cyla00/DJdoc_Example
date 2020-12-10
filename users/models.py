from django.db import models

# Create your models here.
class Setting(models.Model):
    setting_name = models.CharField(max_length=200, null=True)
    setting_value = models.CharField(max_length=100, null=True)
    setting_description = models.TextField(default='null', null=True)