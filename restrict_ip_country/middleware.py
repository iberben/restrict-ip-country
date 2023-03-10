import logging 

from restrict_ip_country.constants import (
    RESTRICT_IP_CACHE_KEY, 
    RESTRICT_IP_CACHE_TIMEOUT,
    RESTRICT_IP_TEMPLATE_PATH,
    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND
)

from django.template.loader import render_to_string
from django.http.response import HttpResponse

from restrict_ip_country.models import RestrictIp, RestrictCountry

from django.utils.module_loading import import_string

from django.core.cache import cache

from django.contrib.gis.geoip2 import GeoIP2


logger = logging.getLogger('restrict_ip_country.middleware')


class RestrictIpCountryMiddleware(object):
    def __init__(self, get_response):
        super(RestrictIpCountryMiddleware, self).__init__()

        self.__geoip = GeoIP2()

        self.__ipsDeny = None
        self.__isoCodeDeny = None

        self.get_response = get_response

    def __call__(self, request):       
        response = self.process_request(request)

        if not response:
            return self.get_response(request)
        
        return response

    def __get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_info(self, ip):
        try:
            iso_code = self.__geoip.city(ip)['country_code']
        except:
            iso_code = "##"
            logger.warning(f'IP address {ip} was not found in database')
        
        return iso_code
    
    def get_fresh_blocked_ips_countries(self):
        cache_dic = cache.get_many([RESTRICT_IP_CACHE_KEY.format('IPS'), RESTRICT_IP_CACHE_KEY.format('COUNTRIES')])

        ips = cache_dic.get(RESTRICT_IP_CACHE_KEY.format('IPS'), None)
        countries = cache_dic.get(RESTRICT_IP_CACHE_KEY.format('COUNTRIES'), None)
        
        if ips is None:
            ips = RestrictIp.objects.all().values_list('ip')
            countries = RestrictCountry.objects.all().values_list('country')

            ips = list(ip_set[0] for ip_set in ips)
            countries = list(countries_set[0] for countries_set in countries)

            # cache recent db data
            cache.set(RESTRICT_IP_CACHE_KEY.format('IPS'), ips, timeout=RESTRICT_IP_CACHE_TIMEOUT)
            cache.set(RESTRICT_IP_CACHE_KEY.format('COUNTRIES'), countries, timeout=RESTRICT_IP_CACHE_TIMEOUT)

        self.__ipsDeny = ips
        self.__isoCodeDeny = countries

    def process_request(self, request):
        ip = self.__get_client_ip(request)
   
        request.META['REMOTE_ADDR'] = ip

        self.get_fresh_blocked_ips_countries()

        if self.__ipsDeny or self.__isoCodeDeny:
            iso_code = self.get_info(ip)                

            if ip in self.__ipsDeny or iso_code in self.__isoCodeDeny:
                logger.debug('Unauthorized access, IP address was ' + ip)
                
                context = {}
                if RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND is not None:
                    func = import_string(RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND)
                    context = func()

                response = render_to_string(RESTRICT_IP_TEMPLATE_PATH, context)
                return HttpResponse(response, status=403)    

        return None
