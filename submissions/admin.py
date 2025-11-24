from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'request', 'creator', 'is_paid', 'submitted_at']
    list_filter = ['is_paid', 'submitted_at']
    search_fields = ['creator__username', 'request__title']
    readonly_fields = ['preview_video', 'thumbnail', 'submitted_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('request', 'creator', 'description')
        }),
        ('파일', {
            'fields': ('original_video', 'preview_video', 'thumbnail')
        }),
        ('상태', {
            'fields': ('is_paid', 'submitted_at', 'updated_at')
        }),
    )