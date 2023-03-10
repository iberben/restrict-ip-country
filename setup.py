from distutils.core import setup
from restrict_ip_country import get_version


setup(
    name='restrict-ip-country',
    version=get_version(),
    description=("A reusable Django app for restricting ip addresses and country areas from accessing site."),
    long_description=open('docs/usage.rst', encoding='utf-8').read(),
    author='Mbadiwe Nnaemeka Ronald',
    author_email='ron2tele@gmail.com',
    url='http://github.com/ron4fun/restrict-ip-country',
    packages=[
        'restrict_ip_country',
        'restrict_ip_country.management',
        'restrict_ip_country.management.commands'
    ],
    classifiers=[
        "Development Status :: 6 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
    ],
    install_requires=[
        'Django >= 3.2',
        'geoip2',
    ],
)
