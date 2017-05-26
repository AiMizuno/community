from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from Control.models import *


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'account'


class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Community)
admin.site.register(Activity)
admin.site.register(Private_Message)
admin.site.register(Community_Message)
admin.site.register(Blog)
admin.site.register(Twit)
admin.site.register(Account_Community)
admin.site.register(Account_Activity)

admin.site.register(MT_Tables)
admin.site.register(MT_Fields)
admin.site.register(MT_Data)