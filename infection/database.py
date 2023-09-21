from typing import *
import pandas as pd
from tabulate import tabulate

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


def get_foreign_keys(cursor, table_hints=None):
    '''
    get the schema information from this database
    '''
    tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
    tableList=cursor.execute(tableQuery).fetchall()
    tables = []
    for table in tableList:
        tableName=table[0]
        columnQuery="PRAGMA foreign_key_list('%s')" % tableName
        fks=cursor.execute(columnQuery).fetchall()
        for fk in fks:
            fk_id, _, fk_table, fk_from, fk_to, _, _, _ = fk
            tables.append(
                ('.'.join([tableName,fk_from]), '.'.join([fk_table, fk_to]))
            )
    return tables

def get_examples(cursor, num_examples:int=5, table_hints=None):
    '''
    get the schema information from this database
    '''
    tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
    tableList=cursor.execute(tableQuery).fetchall()
    tables = {}
    for table in tableList:
        tableName=table[0]
        columnQuery=f"SELECT * FROM {tableName} LIMIT {num_examples}"
        examples=cursor.execute(columnQuery).fetchall()
        tables[tableName] = tabulate(examples, tablefmt="github", headers=[i[0] for i in cursor.description])
    return tables

def _format_schemas_string(schemas:Dict, foreign_keys:List, examples:Dict = None, num_examples:int=1):
    new_schemas = []

    # Format schema strings
    for table_name, columns in schemas.items():
        schema_str = f"CREATE TABLE {table_name} (\n "
        for col in columns:
            col_id, col_name, col_type, col_notnull, col_defval, col_pk = col
            if col_pk:
                col_str = " ".join([col_name, col_type, 'PRIMARY KEY,'])
            elif col_notnull:
                col_str = " ".join([col_name, col_type, 'NOT NULL,'])
            else:
                col_str = " ".join([col_name, col_type])+','
            schema_str += '\t' + col_str + '\n'
        schema_str += ');\n'

        if examples is not None:
            example_str = f"SELECT * FROM {table_name} LIMIT {num_examples};\n"
            example_str += examples[table_name]
            schema_str += (example_str + '\n')

        schema_str += '\n'
        new_schemas.append(schema_str)
    new_schemas = '\n'.join(new_schemas)

    # Format foreign keys strings
    for fk in foreign_keys:
        new_schemas += (fk[0] + ' can be joined with ' + fk[1] + '\n')
        
    return new_schemas

def format_schemas(cursor, table_hints=None, add_examples:int = 0):
    """
    Format the SQL schemas and foreign keys to a string
    """
    schemas = get_schemas(cursor, table_hints)
    foreign_keys = get_foreign_keys(cursor, table_hints)

    examples = None
    if add_examples:
        if add_examples > 0:
            examples = get_examples(cursor, num_examples=add_examples, table_hints=table_hints)

    return _format_schemas_string(schemas, foreign_keys, examples=examples, num_examples=add_examples)

def format_sql_execution(records:List[tuple], column_names: List[str], format:str='table'):
    """
    Format the SQL execution results to a table
    """
    
    if format == 'table':
        results = tabulate(records, tablefmt="github", headers=column_names)
    elif format == 'dataframe':
        results = pd.DataFrame(records)
        results.columns = column_names
    else:
        raise ValueError(f"Unknown format: {format}")
    return results