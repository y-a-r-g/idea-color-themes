import random
import string
from django.db import models
from backend.logic.utils import escape_file_name


class Theme(models.Model):
    def archivePath(self, filename):
        return 'themes/%s' % escape_file_name(filename)

    name = models.CharField(max_length=64)
    elements = models.TextField(blank=True, default='')
    downloads = models.IntegerField(blank=True, default=0)
    date = models.DateField(blank=True, auto_now_add=True)
    author = models.CharField(blank=True, default='', max_length=64)
    website = models.CharField(blank=True, default='', max_length=512)
    ect = models.IntegerField(blank=True, default=-1)
    promote = models.BooleanField(blank=True, default=True)
    comment = models.TextField(blank=True, default="", max_length=2048)
    archive = models.FileField(blank=True, default='', max_length=260, upload_to=archivePath)
    moderating = models.BooleanField(blank=True, default=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, 'Moderating' if self.moderating else '')


def genToken():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(96))


class ShoppingToken(models.Model):
    date = models.DateField(blank=True, auto_now_add=True)
    value = models.CharField(blank=True, default=genToken, max_length=127)
    payed = models.BooleanField(blank=True, default=False)
