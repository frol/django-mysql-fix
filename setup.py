from setuptools import setup, find_packages

from django_mysql_fix.version import __version__

with open('README.md') as long_description_file:
    long_description = long_description_file.read()

setup(name='django-mysql-fix',
    version=__version__,
    description="This project contains optimizations (hacks) for MySQL for Django ORM",
    long_description=long_description,
    author="Vladyslav Frolov",
    author_email="frolvlad@gmail.com",
    url='https://github.com/frol/django-mysql-fix',
    packages=find_packages(),
    install_requires=('django', ),
)
