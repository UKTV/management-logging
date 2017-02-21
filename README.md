Management Logging
==========

Django app that will allow you to track the output's from management commands.

============
Installation
============

* Add ``management_logging`` to ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        'management_logging',
    )


* Include ``management_logging.urls`` in your ``urls.py``:

.. code-block:: python

    urlpatterns += patterns('',
        url(r'^management-logging/', include('management_logging.urls')),
    )

Run migrations to create database tables::

    python manage.py migrate management_logging

=====
Usage
=====

Adding logging to management commands
-------------------------------------

.. code-block:: python

    from management_logging.command import CommandwithLogging

    class MyCommand(CommandwithLogging):
        name = 'Name of my command'

Logging when using ``django-rq`` rqscheduler
--------------------------------------------

.. code-block:: python

    pip install django-rq
    pip install git+git://github.com/UKTV/django-rq-scheduler@v1.1.2#egg=django-rq-scheduler-1.1.2

    INSTALLED_APPS = (
        # other apps
        'django_rq',
        'scheduler',
    )

    python manage.py rqworker default --worker-class=management_logging.worker.LoggingWorker

--------------
Logging Report
--------------

The report will show you the status of the latest run of each management command. You have to be logged in to see the report

=========
Changelog
=========

Version 0.1
-------------

* Initial setup