def get_schemas(cursor, table_hints=None):
    '''
    get the schema information from this database
    '''
    tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
    tableList=cursor.execute(tableQuery).fetchall()
    tables = {}
    for table in tableList:
        tableName=table[0]
        columnQuery="PRAGMA table_info('%s')" % tableName
        schema=cursor.execute(columnQuery).fetchall()
        tables[tableName] = schema
    return tables