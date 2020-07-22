from django.contrib import admin
from .models import Subject, Certification

# Register your models here.
admin.site.register(Subject),
admin.site.register(Certification)

verbose_name = 'Предмет'