from django.contrib import admin
from .models import Group, Subgroup, Note

# This special class makes the password look right in the admin panel
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    def save_model(self, request, obj, form, change):
        # This ensures the password is encrypted even when created in Admin
        if not obj.pk or 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Group, GroupAdmin)
admin.site.register(Subgroup)
admin.site.register(Note)

# Register your models here.
