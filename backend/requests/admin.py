from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'requester', 'status', 'reward', 'created_at']
    list_filter = ['status', 'request_type']
    search_fields = ['title', 'requester__username']