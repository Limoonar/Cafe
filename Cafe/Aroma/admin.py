from django.contrib import admin

from .models import *

admin.site.register(Users)
admin.site.register(Product)
admin.site.register(Storage)
admin.site.register(Orders)


