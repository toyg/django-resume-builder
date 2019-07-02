from django.contrib import admin

from . import models


@admin.register(models.ResumeItem)
class ResumeItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'company', 'start_date')
    ordering = ('user', '-start_date')


class ResumeItemLinkInline(admin.StackedInline):
    model = models.ResumeItemLink
    ordering = ('order',)
    extra = 1


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'label')
    ordering = ('user', '-updated_on')
    inlines = [ResumeItemLinkInline]
