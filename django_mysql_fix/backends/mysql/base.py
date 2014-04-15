from django.db.backends.mysql.base import *
from django.db.backends.mysql.base import DatabaseOperations as BaseDatabaseOperations
from django.db.backends.mysql.base import DatabaseWrapper as BaseDatabaseWrapper


class DatabaseOperations(BaseDatabaseOperations):
    compiler_module = "django_mysql_fix.backends.mysql.compiler"


class DatabaseWrapper(BaseDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.ops = DatabaseOperations(self)
 
