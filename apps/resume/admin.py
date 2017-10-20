from django.contrib import admin

from . import models


@admin.register(models.ResumeItem)
class ResumeItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'company', 'start_date')
    ordering = ('user', '-start_date')
