from datetime import datetime
from django.db import models
from language.models import *

class Query(models.Model):
    language = models.ForeignKey(Language)
    text = models.CharField(max_length=100)
    searched_at = models.DateTimeField(default=datetime.now())
    from_ip = models.CharField(max_length=50, null=True)
    
    def __unicode__(self):
        return self.language.name + ', ' + self.text
    class Meta:
        verbose_name_plural = "Queries"
