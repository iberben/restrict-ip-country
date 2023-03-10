from django.db import models
from django.utils.translation import gettext_lazy as _
from restrict_ip_country.mixin import TimeStampMixin
from restrict_ip_country.constants import COUNTRY_CHOICES, COUNTRY_CHOICES_DIC


class RestrictIp(TimeStampMixin):
    ip = models.GenericIPAddressField(_("IP address"), unique=True, help_text=_("Designates the restricted ip address."))
  
    class Meta:
        verbose_name = _('restricted ip')
        verbose_name_plural = _('Restricted IPs')

        ordering = ("-created_at",)
        
        db_table = "restrict_ip"

    def __unicode__(self):
        return str(self)
        
    def __str__(self):
        return self.ip
    

class RestrictCountry(TimeStampMixin):
    country = models.CharField(_("Country"),
                               max_length=2,
                               unique=True,
                               choices=COUNTRY_CHOICES, 
                               help_text=_("Designates the restricted country."))
    class Meta:
        verbose_name = _('restricted country')
        verbose_name_plural = _('Restricted Countries')

        ordering = ("-created_at",)
        
        db_table = "restrict_country"

    def __unicode__(self):
        return str(self)
        
    def __str__(self):
        return COUNTRY_CHOICES_DIC.get(self.country)
    
    