from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AutaiSite(admin.AdminSite):
    site_header = "族語AI成果網站人員管理後台"


autai_site = AutaiSite(name="adminautaidddd")

autai_site.register(User, UserAdmin)
autai_site.register(Group)
