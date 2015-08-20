============
Installation
============

Requirements
------------
- Python v.2.7+ (no Python 3 support yet!)
- `Django v.1.4 <https://www.djangoproject.com/>`_
- `Hackstack v.2.0 <http://haystacksearch.org/>`_ (Search module for Django)
- `Whoosh v.2.4 <https://pypi.python.org/pypi/Whoosh/>`_ (Full-text search enginge used for django-haystack)
- `Pillow <https://pypi.python.org/pypi/Pillow/2.9.0>`_

Manual Installation
-------------------
- Clone source repository from `GitHub <https://github.com/holgerd77/django-website-showroom>`_
- Create a virtual environment with ``virtualenv``
- Install the requirements with ``pip install -r requirements.txt``
- Manually link the ``website_showroom`` folder to the ``site-packages`` folder of your environment

Setup
-----
- Create a separate ``Django`` project
- Add ``website_showroom`` to the ``INSTALLED_APPS`` in ``settings.py``
- Customize your site's title, subtitle,... via settings.py (see opendata-showroom-org GitHub project as example)
- Create desired categories, websites via admin interface