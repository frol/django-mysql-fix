from setuptools import setup, find_packages

from django_mysql_fix.version import __version__


setup(name='django_mysql_fix',
    version=__version__,
    description="This project contains optimizations (hacks) for MySQL for Django ORM",
    author="Vladyslav Frolov",
    author_email="frolvlad@gmail.com",
    url='http://prostoksi.com',
    packages=find_packages(),
    install_requires=('django', ),
)
