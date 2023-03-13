#!/usr/bin/env python
import os
import sys
import warnings

import django, os
from pathlib import Path
from django.conf import settings
from django.test.utils import get_runner

warnings.simplefilter("always", DeprecationWarning)
warnings.simplefilter("always", PendingDeprecationWarning)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "restrict_ip_country",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    SITE_ID=1,
    SECRET_KEY="notasecret",
    MIDDLEWARE_CLASSES=[
        'restrict_ip_country.middleware.RestrictIpCountryMiddleware',
    ],
    # GEOIP_PATH=os.path.join(BASE_DIR, 'data'),
    # GEOIP_CITY='GeoLite2-City.mmdb',
    RESTRICT_IP_CACHE_TIMEOUT=0,
    RESTRICT_IP_TEMPLATE_PATH = 'errors/403.html',
    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND='restrict_ip_country.utils.build_template_context'
)


def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if not test_args:
        test_args = ['tests']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == "__main__":
    runtests(*sys.argv[1:])
