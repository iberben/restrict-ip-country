========
Settings
========

Following is a list of settings which can be added to your Django settings
configuration. The ``RESTRICT_IP_TEMPLATE_PATH`` is required and other settings 
are optional and the default value is listed for each.


RESTRICT_IP_TEMPLATE_PATH
-------------------------

* The path where the template to be rendered is located when access is restricted to site,
defaults to ``errors/403.html``.

    RESTRICT_IP_TEMPLATE_PATH = "errors/403.html"

* Note: if template is not available or found. ``TemplateDoesNotExist`` exception is thrown.


RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND
------------------------------------

A function when called in your app returns a dictionary, the 
context data used in rendering the restricted template::

    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND = "your.actual.ContextBackend"

Defaults to ``None``.


RESTRICT_IP_CACHE_TIMEOUT
-------------------------

The time in seconds to cache the database restricted values, 
to minimize un-necessary calls per request especially in times of high traffic::

    RESTRICT_IP_TEMPLATE_CONTEXT_BACKEND = "your.actual.ContextBackend"

Defaults to ``300`` seconds. And ``0`` to not cache at all.


RESTRICT_IP_BLOCK_NOTFOUND
--------------------------------

Block any parsed ip address not found in the ``GEOIP_CITY`` database.

    RESTRICT_IP_BLOCK_NOTFOUND = False

Defaults to ``False``.

Note: you must have at least a restricted ip or country set in your database for it to work. 
This is for optimization purposes.