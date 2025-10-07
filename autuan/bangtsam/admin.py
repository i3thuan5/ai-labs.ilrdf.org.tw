from axes.models import AccessAttempt, AccessLog, AccessFailureLog
from axes.admin import AccessAttemptAdmin, AccessLogAdmin, AccessFailureLogAdmin
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from password_policies.models import PasswordRecord

# Register your models here.


class AutaiSite(admin.AdminSite):
    site_header = "族語AI成果網站人員管理後台"


class PasswordRecordAutai(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_display_links = None
    list_per_page = 30
    list_filter = ('user',)
    search_fields = ['user__username', 'date', ]
    search_help_text = '搜尋說明：查詢帳號名稱或密碼修改日期，日期查詢格式為YYYY、YYYY-MM、YYYY-MM-DD。'
    date_hierarchy = 'date'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


autai_site = AutaiSite(name="adminautai")

autai_site.register(User, UserAdmin)
autai_site.register(Group)
autai_site.register(PasswordRecord, PasswordRecordAutai)
autai_site.register(AccessAttempt, AccessAttemptAdmin)
autai_site.register(AccessLog, AccessLogAdmin)
autai_site.register(AccessFailureLog, AccessFailureLogAdmin)
