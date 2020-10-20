# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Image,Comment,Like

# Register your models here.
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)


