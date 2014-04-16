django-mysql-fix
================

This project contains optimizations (hacks) for MySQL for Django ORM.

It's based on Django 1.7 (master branch). It was started on PyCon 2014 Development Sprint.

We are going to test possible regressions that might appear in real projects.
This backend will pass all Django tests, but we still have to test it in real projects.


How does it affect me?
======================

There are two very simple ways to cacth INNER JOIN bug:

* Once you specify field from foreign table in `list_display` in your Django Admin model;
* Once you try to sort (order) by field from foreign table.

In these cases even if you limit query by 1 it will join whole tables, order them and only after that it will slice it to limit. Thus if you have i.e. 400k records in two tables it would take 3+ seconds to get small slice. STRAIGHT_JOIN forces MySQL work as we expect: order -> slice -> join.


How to use
==========

Specify django-mysql-fix backend in your DATABASES setting in Django settings.py::

    DATABASES = {
        'default': {
            'ENGINE': 'django_mysql_fix.backends.mysql',
            ...
        },
    }


Compatibility
=============

Tested with Django master branch and Django 1.6.0+.

It doesn't work with Django <= 1.5.x.


Fixed issues
============

For now there is only one optimization there.

* MySQL INNER JOIN with order fails to optimize query that ends up with seconds
  to get result, but STRAIGHT\_JOIN instead of INNER JOIN solves the issue and
  we can get result in 0.001 instead of 3+ seconds.
  https://code.djangoproject.com/ticket/22438
