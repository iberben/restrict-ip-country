from django.contrib import admin, messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from restrict_ip_country.models import RestrictIp, RestrictCountry
from restrict_ip_country.constants import RESTRICT_IP_CACHE_TIMEOUT

from datetime import datetime, timedelta


class RestrictIpAdmin(admin.ModelAdmin):
    list_display = ("ip", "created_at",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    search_fields = ("ip",)
    exclude = ("updated_at",)
    ordering = ["ip", "created_at"]

    def response_add(self, request, obj, post_url_continue=None):
        msg = f"Changes may take up to {naturaltime(datetime.now() + timedelta(0, RESTRICT_IP_CACHE_TIMEOUT+1))} to reflect."
        self.message_user(request, msg, level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)


class RestrictCountryAdmin(admin.ModelAdmin):
    list_display = ("country", "created_at",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    search_fields = ("country",)
    exclude = ("updated_at",)
    ordering = ["country", "created_at"]

    def response_add(self, request, obj, post_url_continue=None):
        msg = f"Changes may take up to {naturaltime(datetime.now() + timedelta(0, RESTRICT_IP_CACHE_TIMEOUT+1))} to reflect."
        self.message_user(request, msg, level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)


admin.site.register(RestrictIp, RestrictIpAdmin)
admin.site.register(RestrictCountry, RestrictCountryAdmin)
