from django.contrib import admin
from account.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'email_verified', 'phone_verified', 'is_active', 'updated_at']
    list_filter = ['email_verified', 'phone_verified', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'organization', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'organization')
        }),
        ('Preferences', {
            'fields': ('timezone', 'language')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
