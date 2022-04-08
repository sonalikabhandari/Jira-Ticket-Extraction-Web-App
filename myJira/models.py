from django.db import models
from datetime import datetime

# Create your models here.
class JiraTicket(models.Model):
    key = models.CharField(max_length=100)
    Summary = models.CharField(max_length=200,null=True)
    status = models.TextField(null=True)
    assignee = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(null=True)
    links = models.ManyToManyField('self', related_name = 'issue_links' , blank = True)

    def __str__(self):
        return self.key
