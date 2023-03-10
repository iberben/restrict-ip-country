=====
Usage
=====

``restrict-ip-country`` is a reusable Django app for restricting ip addresses and country areas from accessing site.

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
