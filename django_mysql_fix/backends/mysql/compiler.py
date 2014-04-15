from django.db.backends.mysql.compiler import SQLCompiler as BaseSQLCompiler
from django.db.backends.mysql.compiler import SQLInsertCompiler, \
    SQLDeleteCompiler, SQLUpdateCompiler, SQLAggregateCompiler, \
    SQLDateCompiler, SQLDateTimeCompiler


class SQLCompiler(BaseSQLCompiler):
    
    def get_ordering(self):
        """
        Returns a tuple containing a list representing the SQL elements in the
        "order by" clause, and the list of SQL elements that need to be added
        to the GROUP BY clause as a result of the ordering.
        
        Also sets the ordering_aliases attribute on this instance to a list of
        extra aliases needed in the select.
        
        Determining the ordering SQL can change the tables we need to include,
        so this should be run *before* get_from_clause().

        The method is overrided to save the result
        """
        # We might want to notify people to not order by columns from different
        # tables as there is no index across tables. They may create proxy
        # model to do filtering with subquery.
        result, params, group_by = super(SQLCompiler, self).get_ordering()
        self.__ordering = result
        return result, params, group_by

    def get_from_clause(self):
        """
        Returns a list of strings that are joined together to go after the
        "FROM" part of the query, as well as a list any extra parameters that
        need to be included. Sub-classes, can override this to create a
        from-clause via a "select".
        
        This should only be called after any SQL construction methods that
        might change the tables we need. This means the select columns,
        ordering and distinct must be done first.
        """
        result, from_params = super(SQLCompiler, self).get_from_clause()
        return result, from_params
