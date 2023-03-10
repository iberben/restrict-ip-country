===================
restrict-ip-country
===================

``restrict-ip-country`` is a reusable Django app for restricting ip addresses and country areas from accessing site.

Contents:

.. toctree::

    install
    usage
    settings


Configure GeoIP2 settings
===========================

Ensure you have setup `GeoIP2 <https://docs.djangoproject.com/en/3.2/ref/contrib/gis/geoip2/>`_ 
global variables in your ``settings.py``::

    GEOIP_PATH=os.path.join(BASE_DIR, 'data')

A string or pathlib.Path specifying the directory where the GeoIP data files are located. 
This setting is required.

    GEOIP_CITY='GeoLite2-City.mmdb'

The basename to use for the GeoIP city data file. Defaults to `'GeoLite2-City.mmdb' <https://git.io/GeoLite2-City.mmdb>`.
