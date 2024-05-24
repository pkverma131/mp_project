from django.contrib import admin
from .models import (
    Industry, Product, Lead, LeadMeta, LeadCatalogue,
    ContactPerson, User, Activity, Email, Call, Task, Note
)

@admin.register(Industry)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'description')
    search_fields = ('name',)
    list_filter = ('industry',)

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'industry', 'website', 'address', 'phone', 'email')
    search_fields = ('company_name', 'industry')
    list_filter = ('industry',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(LeadMeta)
class LeadMetaAdmin(admin.ModelAdmin):
    list_display = ('lead', 'additional_info')
    search_fields = ('lead__company_name',)

@admin.register(LeadCatalogue)
class LeadCatalogueAdmin(admin.ModelAdmin):
    list_display = ('lead', 'product')
    search_fields = ('lead__company_name', 'product__name')

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'position', 'lead')
    search_fields = ('first_name', 'last_name', 'email', 'lead__company_name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'lead', 'user', 'scheduled_at', 'completed_at', 'created_at', 'updated_at')
    search_fields = ('activity_type', 'lead__company_name', 'user__username')
    list_filter = ('activity_type',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'lead', 'user', 'status', 'sent_at', 'created_at')
    search_fields = ('subject', 'lead__company_name', 'user__username', 'status')
    list_filter = ('status',)
    readonly_fields = ('created_at',)

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'call_time', 'duration', 'outcome', 'lead', 'user', 'created_at')
    search_fields = ('phone_number', 'lead__company_name', 'user__username', 'outcome')
    list_filter = ('outcome',)
    readonly_fields = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'user', 'due_date', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'lead__company_name', 'user__username', 'status')
    list_filter = ('status', 'due_date')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content', 'lead', 'user', 'created_at', 'updated_at')
    search_fields = ('content', 'lead__company_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
