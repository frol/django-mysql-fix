django-mysql-fix
================

This project contains optimizations (hacks) for MySQL for Django ORM.

It's based on Django 1.7 (master branch). It was started on PyCon 2014 Development Sprint.

We are going to test possible regressions that might appear in real projects.
This backend will pass all Django tests, but we still have to test it in real projects.


How to use
==========

Specify django-mysql-fix backend in your DATABASES setting in Django settings.py::

    DATABASES = {
        'default': {
            'ENGINE': 'django_mysql_fix.backends.mysql',
            ...
        },
    }


Fixed issues
============

For now there is only one optimization there.

* MySQL INNER JOIN with order fails to optimize query that ends up with seconds
  to get result, but STRAIGHT\_JOIN instead of INNER JOIN solves the issue and
  we can get result in 0.001 instead of 3+ seonds.
  https://code.djangoproject.com/ticket/22438
