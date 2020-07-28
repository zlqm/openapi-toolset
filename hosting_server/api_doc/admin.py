from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Doc, Membership, Project


# Register your models here.
class HostingSite(admin.AdminSite):
    site_header = 'hosting server'

    # @never_cache
    # def index(self, request, extra_context=None):
    #     context = {
    #         **self.each_context(request),
    #         'title': 'project list',
    #         **(extra_context or {}),
    #     }
    #     query_filter = Q(members__user=request.user) | \
    #         Q(owner=request.user)
    #     projects = Project.objects.filter(query_filter
    #         ).order_by('-update_at')
    #     context['projects'] = projects
    #     return TemplateResponse('api_doc/index.html', context)


site = HostingSite(name='test')


class MemberInline(admin.TabularInline):
    extra = 0
    model = Membership


class DocInline(admin.TabularInline):
    extra = 0
    model = Doc

    def save_formset(self, *args, **kwargs):
        return super().save_model(*args, **kwargs)


class SimpleUserAdmin(UserAdmin):
    inlines = [MemberInline]
    fieldsets = (
        (None, {
            'fields': ('username', 'password'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )


class ProjectAdmin(admin.ModelAdmin):
    inlines = [MemberInline, DocInline]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user == obj.owner:
            return True
        if obj.is_maintainer(request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user == obj.owner


site.register(get_user_model(), SimpleUserAdmin)
site.register(Project, ProjectAdmin)
