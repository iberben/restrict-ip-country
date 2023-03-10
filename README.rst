Restrict IPs & Countries 
------------------------

``restrict-ip-country`` is a reusable Django app for restricting ip addresses and country areas from accessing site.

Requirements
------------

* Django >= 3.2
* geoip2


============
Installation
============

An obvious prerequisite of restrict-ip-country is Django - 3.2 is the
minimum supported version.


Installing restrict-ip-country
==============================

Download and install from http://github.com/ron4fun/restrict-ip-country.git

If you're using pip__ and a virtual environment, this usually looks like::

    pip install -e git+http://github.com/ron4fun/restrict-ip-country.git#egg=restrict-ip-country

.. __: http://pip.openplans.org/

Or for a manual installation, once you've downloaded the package, unpack it
and run the ``setup.py`` installation script::

    python setup.py install


===========================
Configuring GeoIP2 settings
===========================

Ensure you have setup .. __GeoIP2: https://docs.djangoproject.com/en/3.2/ref/contrib/gis/geoip2/
global variables in your ``settings.py``::

    GEOIP_PATH=os.path.join(BASE_DIR, 'data')

A string or pathlib.Path specifying the directory where the GeoIP data files are located. 
This setting is required.

    GEOIP_CITY='GeoLite2-City.mmdb'

The basename to use for the GeoIP city data file. Defaults to `GeoLite2-City.mmdb <https://git.io/GeoLite2-City.mmdb>`_.


=====
Usage
=====

First, add ``restrict_ip_country`` to your ``INSTALLED_APPS`` in your ``settings.py``.
Run ``./manage.py migrate`` to install models.


Configuring your project
========================

In your Django project's settings module, add restrict_ip_country to your
``INSTALLED_APPS`` setting::
    
    INSTALLED_APPS = (
        ...
        'restrict_ip_country',
    )

Finally, add ``restrict_ip_country.middleware.RestrictIpMiddleware`` to your ``MIDDLEWARE`` in your ``settings.py``, 
ensure all configurations are properly done to avoid errors.


========
Settings
========

Following is a list of settings which can be added to your Django settings
configuration. The ``RESTRICT_IP_TEMPLATE_PATH`` is required and other settings 
are optional and the default value is listed for each.


Using RESTRICT_IP_TEMPLATE_PATH
-------------------------------

* The path where the template to be rendered is located when access is restricted to site,
defaults to ``errors/403.html``.

* Note: if template is not available or found. ``TemplateDoesNotExist`` exception is thrown.


Using RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND
------------------------------------------

A function when called in your app returns a dictionary, the 
context data used in rendering the restricted template::

    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND = "your.actual.ContextBackend"

Defaults to ``None``.


Using RESTRICT_IP_CACHE_TIMEOUT
-------------------------------

The time in seconds to cache the database restricted values, 
to minimize un-necessary calls per request especially in times of high traffic::

    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND = "your.actual.ContextBackend"

Defaults to ``300`` seconds. And ``0`` to not cache at all.


Command Extensions
==================

With restrict_ip_country in your ``INSTALLED_APPS``, there will be 2 new
``manage.py`` commands you can run:

* ``get_ip_info`` will get the city information of the given ip address.
  Use the ``-p``or ``--ip`` option to set the ip address.

* ``get_restrict_config`` will get the restrict-ip-country configs including 
  the restricted ip addresses and countries.


If you use `Windows OS` or alternatives, and find it difficult piping logging infos to output file or setting verbosity level
Use the ``-f`` or ``--file`` option to set the full path to the logging output file.
Use the ``-v`` or ``--verbosity`` option to set the verbosity level i.e, {0,1,2,3}.
