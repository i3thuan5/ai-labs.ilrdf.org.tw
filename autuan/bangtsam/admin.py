from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AutaiSite(admin.AdminSite):
    site_header = "族語AI成果網站系統管理後台"


autai_site = AutaiSite(name="adminautai")

autai_site.register(User, UserAdmin)
autai_site.register(Group)
