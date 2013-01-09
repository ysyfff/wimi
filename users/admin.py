from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import SBProfile

class SBProfileInline(admin.StackedInline):
    model = SBProfile
    can_delete = False
    verbose_name_plural = 'SBProfile'

class UserAdmin(UserAdmin):
    inlines = (SBProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)