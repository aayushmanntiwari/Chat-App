from django.db import models

# Create your models here.
class GlobalSetting(models.Model):
    two_factor_api_key = models.TextField(blank=True,null=True)