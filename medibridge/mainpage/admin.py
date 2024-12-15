'''
Admin registeration of mainpage
'''

from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Quote)
admin.site.register(Doctor)
admin.site.register(Patient)
