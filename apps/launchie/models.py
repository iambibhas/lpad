
from datetime import datetime
from django.db import models

class Project(models.Model):
    name = models.CharField(max_length = 50)
    summary = models.CharField(max_length = 500)
    active = models.CharField(max_length = 50)
    owner = models.CharField(max_length = 500)
    logo = models.CharField(max_length = 500)
    web_link = models.CharField(max_length = 500)
    programming_language = models.CharField(max_length = 50)
    updated_at = models.DateTimeField(default = datetime.now())
