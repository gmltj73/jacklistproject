from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    #fields = ['name', 'summary', 'description', 'update_time', 'reg_date']
    #수정
    list_display = ['name', 'summary', 'description', 'update_time', 'reg_date']
    #수정E
admin.site.register(Project, ProjectAdmin)


# class UserAdmin(admin.ModelAdmin):
    # form = UserForm
    #
    # fieldsets =