from django.contrib import admin
from interact.models import *

# Register your models here.
admin.site.register([MaterialType, Material, Emotion])
