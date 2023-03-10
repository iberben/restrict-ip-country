# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import TemplateDoesNotExist
from django.core.management import call_command
from django.test import TestCase

import restrict_ip_country
from restrict_ip_country.middleware import RestrictIpCountryMiddleware
from mock import patch, Mock, MagicMock
from restrict_ip_country.models import *


class RestrictIpCountryMiddlewareTests(TestCase):    
    def setUp(self):
        self.request = Mock()
        self.request.META = {}
        self.request.path = '/testURL/'
        self.request.session = {}    

    def set_request_ip_address(self, ip='127.0.0.1'):
        self.request.META = { 
            "HTTP_X_FORWARDED_FOR": ip, 
            "REMOTE_ADDR": ip, 
        }
        return self.request
    
    def block_ip_address(self, ip='127.0.0.1'):
        return RestrictIp.objects.create(ip=ip)
    
    def block_country(self, country="US"):
        return RestrictCountry.objects.create(country=country)

    def test_with_no_blocked_ips_countries(self):
        with patch.object(restrict_ip_country.middleware, 'GeoIP2') as GeoIP2_patch:
            with patch.object(restrict_ip_country.middleware, 'render_to_string') as render_to_string_patch:
                get_response = MagicMock()
                
                self.assertEqual(RestrictIp.objects.count(), 0)
                self.assertEqual(RestrictCountry.objects.count(), 0)

                middleware = RestrictIpCountryMiddleware(get_response)
                
                middleware.get_info = MagicMock()

                middleware.process_request(self.set_request_ip_address())
                
                middleware.get_info.assert_not_called()
                GeoIP2_patch.assert_called_once()
                render_to_string_patch.assert_not_called()

    def test_with_blocked_ips(self):
        with patch.object(restrict_ip_country.middleware, 'GeoIP2') as GeoIP2_patch:
            with patch.object(restrict_ip_country.middleware, 'render_to_string') as render_to_string_patch:
                get_response = MagicMock()
                
                self.block_ip_address()

                self.assertEqual(RestrictIp.objects.count(), 1)
                self.assertEqual(RestrictCountry.objects.count(), 0)

                middleware = RestrictIpCountryMiddleware(get_response)
                
                middleware.get_info = MagicMock()

                middleware.process_request(self.set_request_ip_address())
                middleware.process_request(self.set_request_ip_address('196.122.133.8'))

                self.assertEqual(middleware.get_info.call_count, 2)
                render_to_string_patch.assert_called_once()

                self.block_ip_address('196.122.133.8')

                middleware.process_request(self.set_request_ip_address())
                middleware.process_request(self.set_request_ip_address('196.122.133.8'))
                middleware.process_request(self.set_request_ip_address('204.5.111.2'))
                
                self.assertEqual(RestrictIp.objects.count(), 2)
                self.assertEqual(RestrictCountry.objects.count(), 0)
                
                self.assertEqual(middleware.get_info.call_count, 5)
                self.assertEqual(render_to_string_patch.call_count, 3)

                GeoIP2_patch.assert_called_once()

    def test_with_blocked_countries(self):
        with patch.object(restrict_ip_country.middleware, 'GeoIP2') as GeoIP2_patch:
            with patch.object(restrict_ip_country.middleware, 'render_to_string') as render_to_string_patch:
                get_response = MagicMock()
                
                self.block_country()

                self.assertEqual(RestrictIp.objects.count(), 0)
                self.assertEqual(RestrictCountry.objects.count(), 1)

                middleware = RestrictIpCountryMiddleware(get_response)
                
                middleware.get_info = MagicMock()

                middleware.get_info.return_value = "US"

                middleware.process_request(self.set_request_ip_address())

                middleware.get_info.assert_called_once()
                render_to_string_patch.assert_called_once()

                self.block_country('NL')

                middleware.get_info.return_value = "NL"

                middleware.process_request(self.set_request_ip_address())
                
                self.assertEqual(RestrictIp.objects.count(), 0)
                self.assertEqual(RestrictCountry.objects.count(), 2)
                
                self.assertEqual(middleware.get_info.call_count, 2)
                self.assertEqual(render_to_string_patch.call_count, 2)

                GeoIP2_patch.assert_called_once()

    def test_throws_template_error_when_not_found(self):
        with patch.object(restrict_ip_country.middleware, 'GeoIP2') as GeoIP2_patch:
            get_response = MagicMock()
            
            self.block_ip_address()

            self.assertEqual(RestrictIp.objects.count(), 1)
            self.assertEqual(RestrictCountry.objects.count(), 0)

            middleware = RestrictIpCountryMiddleware(get_response)
            
            middleware.get_info = MagicMock()

            func = lambda: middleware.process_request(self.set_request_ip_address())

            self.assertRaises(TemplateDoesNotExist, func)

    def test_with_commands_no_throw(self):
        call_command('get_ip_info', ip="127.0.0.1", verbosity='0')
        call_command('get_ip_info', ip="127.0.0.1", verbosity='0')

