from django.db.backends.mysql.compiler import SQLCompiler as BaseSQLCompiler
from django.db.backends.mysql.compiler import SQLInsertCompiler, \
    SQLDeleteCompiler, SQLUpdateCompiler, SQLAggregateCompiler, \
    SQLDateCompiler, SQLDateTimeCompiler


class SQLCompiler(BaseSQLCompiler):
    STRAIGHT_INNER = 'STRAIGHT_JOIN'
    
    def get_ordering(self):
        """
        Returns a tuple containing a list representing the SQL elements in the
        "order by" clause, and the list of SQL elements that need to be added
        to the GROUP BY clause as a result of the ordering.
        
        Also sets the ordering_aliases attribute on this instance to a list of
        extra aliases needed in the select.
        
        Determining the ordering SQL can change the tables we need to include,
        so this should be run *before* get_from_clause().

        The method is overrided to save the result to reuse it in
        get_from_clause().
        """
        # We might want to notify people to not order by columns from different
        # tables as there is no index across tables. They may create proxy
        # model to do filtering with subquery.
        result, params, group_by = super(SQLCompiler, self).get_ordering()
        self.__ordering_group_by = group_by
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
        
        Patch query with STRAIGHT_JOIN if there is ordering and all joins in
        query are INNER joins.
        """
        straight_join_patch_applied = False
        if self.__ordering_group_by \
          and len(self.query.tables) > 1 \
          and all(join_info.join_type is None \
                  or join_info.join_type == self.query.INNER
                    for join_info in self.query.alias_map.itervalues()):
            # Get ordering table name from get_ordering()
            # XXX: let's pretend that we believe in luck! :)
            ordering_table = self.__ordering_group_by[0][0].split('.', 1)[0][1:-1]

            # Save query tables and alias mapping to patch and restore them.
            query_tables = _query_tables = self.query.tables
            query_alias_map = self.query.alias_map
            _query_alias_map = query_alias_map.copy()

            try:
                ordering_table_index = query_tables.index(ordering_table)
            except ValueError:
                # Is this possible? Fallback without patching
                pass
            else:
                # STRAIGHT_JOIN forces MySQL read from the first table in
                # a query, thus we must be sure that the first table is that
                # we apply ordering to.
                if ordering_table_index > 0:
                    _first_table = query_tables[0]
                    # Move ordering table to the begining
                    _query_tables = [ordering_table] \
                        + [table for table in query_tables if table != ordering_table]

                    _ordering_join_info = _query_alias_map[ordering_table]
                    # Fix JoinInfo
                    # XXX: It's unsufficient, it recreates objects.
                    _query_alias_map[_first_table] = _query_alias_map[_first_table]\
                        ._replace(
                        join_type=self.STRAIGHT_INNER,
                        join_cols=[join_cols[::-1]
                            for join_cols in _ordering_join_info.join_cols],
                        join_field=_ordering_join_info.join_field,
                        lhs_alias=ordering_table
                    )
                    _query_alias_map[ordering_table] = _ordering_join_info._replace(
                        join_type=None,
                        join_cols=((None, None), ),
                        join_field=None,
                        lhs_alias=None
                    )

                # Replace INNER joins with STRAIGHT joins
                # XXX: It's unsufficient, it recreates objects.
                for table in _query_tables[1:]:
                    _query_alias_map[table] = _query_alias_map[table]\
                        ._replace(join_type=self.STRAIGHT_INNER)

                # Patch query
                self.query.tables = _query_tables
                self.query.alias_map = _query_alias_map
                straight_join_patch_applied = True

        result, from_params = super(SQLCompiler, self).get_from_clause()

        # Restore patched query if patched
        if straight_join_patch_applied:
            self.query.tables = query_tables
            if ordering_table_index > 0:
                self.query.alias_map = query_alias_map
    
        return result, from_params
