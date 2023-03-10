from django.apps import AppConfig


class RestrictIpCountryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restrict_ip_country'
    verbose_name = 'Restrict IPs & Countries'
