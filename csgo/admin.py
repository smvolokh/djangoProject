from django.contrib import admin
from django.db.models import Max
from . import models


class RifleAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(created_at_=Max('created_at'))

    def created_at(self, obj):
        return obj.created_at

    created_at.admin_order_field = 'created_at'
    list_display = ('title', 'created_at')
    ordering = ('title', )


class SkinAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(created_at_=Max('created_at'))

    def created_at(self, obj):
        return obj.created_at

    created_at.admin_order_field = 'created_at'
    list_display = ('rifles', 'subject', 'text', 'created_at')
    ordering = ('rifles', )


# Register your models here.
admin.site.register(models.Rifle, RifleAdmin)
admin.site.register(models.Skin, SkinAdmin)
