from django.contrib import admin
from .models import University, Company, Internship, Application


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["short_name", "name", "website"]
    search_fields = ["name", "short_name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "company_type", "university", "is_verified", "created_at"]
    list_filter = ["company_type", "is_verified", "university"]
    search_fields = ["name"]
    list_editable = ["is_verified"]
    actions = ["verify_companies"]

    def verify_companies(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f"Проверено {queryset.count()} компаний.")
    verify_companies.short_description = "Верифицировать выбранные компании"


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "field", "format", "is_active", "deadline", "created_at", "display_image"]
    list_filter = ["field", "format", "is_active", "company"]
    search_fields = ["title", "company__name"]
    list_editable = ["is_active"]
    filter_horizontal = ["university_partnership"]

    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover;border-radius:4px" />'
        return "-"
    display_image.allow_tags = True
    display_image.short_description = "Фото"


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["applicant", "internship", "status", "university", "created_at"]
    list_filter = ["status", "university"]
    search_fields = ["applicant__username", "applicant__first_name", "internship__title"]
    list_editable = ["status"]
    readonly_fields = ["created_at", "updated_at"]
