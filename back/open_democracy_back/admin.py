from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from my_auth.models import User

admin.site.site_header = "Administration du Démomètre"
admin.site.index_title = "Administration du Démomètre"
admin.site.site_title = "Démomètre"

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
