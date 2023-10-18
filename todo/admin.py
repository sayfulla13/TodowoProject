from django.contrib import admin
from .models import ToDo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('createdDate',)

admin.site.register(ToDo ,TodoAdmin)
