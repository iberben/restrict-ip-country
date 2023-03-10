============
Installation
============

An obvious prerequisite of restrict-ip-country is Django - 3.2 is the
minimum supported version.


Installing restrict-ip-country
==========================

Download and install from http://github.com/ron4fun/restrict-ip-country.git

If you're using pip__ and a virtual environment, this usually looks like::

    pip install -e git+http://github.com/ron4fun/restrict-ip-country.git#egg=restrict-ip-country

.. __: http://pip.openplans.org/

Or for a manual installation, once you've downloaded the package, unpack it
and run the ``setup.py`` installation script::

    python setup.py install


Configuring your project
========================

In your Django project's settings module, add restrict_ip_country to your
``INSTALLED_APPS`` setting::
    
    INSTALLED_APPS = (
        ...
        'restrict_ip_country',
    )

More details can be found in the usage documentation.
