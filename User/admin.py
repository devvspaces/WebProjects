from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserRegisterForm
from .models import User, QA, Profile

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserUpdateForm
    add_form = UserRegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'admin',)
    list_filter = ('admin',)
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Profile info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('admin','staff','active','confirmed_email',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','name',)
    ordering = ('name',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(QA)
admin.site.register(Profile)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)