from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Comment

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )
    list_display = ['username', 'email', 'user_type', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_superuser']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'contact_name', 'email', 'phone', 'created_at', 'created_by']
    list_filter = ['created_at', 'created_by']
    search_fields = ['business_name', 'contact_name', 'email']
    inlines = [CommentInline]
    readonly_fields = ['created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'user', 'text', 'created_at']
    list_filter = ['created_at', 'user']
    readonly_fields = ['created_at']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Comment, CommentAdmin)