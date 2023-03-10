from django.core.management.base import BaseCommand
from django.db import connection
from restrict_ip_country.middleware import RestrictIpCountryMiddleware
from restrict_ip_country.management.commands import create_file_handler, create_anon_handler
import logging

class Command(BaseCommand):
    help = 'Get the city information of the given ip address.'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--ip', type=str, default="127.0.0.1",
            help='Set to the ip address.')
        parser.add_argument('-f', '--file', type=str, default="",
            help='Set full path to the logging output file.')

    def handle(self, *args, **options):
        ip = options['ip']
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

        restrict_middleware = RestrictIpCountryMiddleware(lambda x: None)

        iso_code = restrict_middleware.get_info(ip)
        
        logger.debug(f'Information found on ip: {ip}')
        logger.debug(f'{iso_code}')
                  
        if handler:
            logger.removeHandler(handler)

        # Stop superfluous "unexpected EOF on client connection" errors in
        # Postgres log files caused by the database connection not being
        # explicitly closed.
        connection.close()
