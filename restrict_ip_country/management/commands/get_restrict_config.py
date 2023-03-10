from django.core.management.base import BaseCommand
from django.db import connection
from restrict_ip_country import models
from restrict_ip_country.constants import (
    RESTRICT_IP_CACHE_TIMEOUT,
    RESTRICT_IP_CACHE_KEY,
    RESTRICT_IP_TEMPLATE_PATH,
    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND
)
from restrict_ip_country.management.commands import create_file_handler, create_anon_handler
import logging


class Command(BaseCommand):
    help = 'Get the restrict-ip-country config.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, default="",
            help='Set full path to the logging output file.')

    def handle(self, *args, **options):
        file = options['file']
        verbosity = options['verbosity']

        logger = logging.getLogger('restrict_ip_country')

        # Send logged messages to the console.        
        handler = None
        if file:
            handler = create_file_handler(verbosity, file)
        else:
            handler = create_anon_handler(verbosity)

        logger.addHandler(handler)

        ips = models.RestrictIp.objects.all().values_list('ip')
        countries = models.RestrictCountry.objects.all().values_list('country')

        ips = list(ip_set[0] for ip_set in ips)
        countries = list(countries_set[0] for countries_set in countries)
        
        info = {
            'RESTRICT_IPS': ips,
            'RESTRICT_COUNTRIES': countries,
            'RESTRICT_IP_CACHE_KEY': RESTRICT_IP_CACHE_KEY,
            'RESTRICT_IP_CACHE_TIMEOUT': RESTRICT_IP_CACHE_TIMEOUT,
            'RESTRICT_IP_TEMPLATE_PATH': RESTRICT_IP_TEMPLATE_PATH,
            'RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND': RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND,
        }
        
        self.stdout.write(f'{info}')
                  
        if handler:
            logger.removeHandler(handler)

        # Stop superfluous "unexpected EOF on client connection" errors in
        # Postgres log files caused by the database connection not being
        # explicitly closed.
        connection.close()
