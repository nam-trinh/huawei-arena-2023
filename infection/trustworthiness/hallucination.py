from typing import *
from sqlglot import parse_one, exp

def check_sql_hallucination(schemas:Dict, sql_query:str):
    """
    schemas: 
    {
        'table_name': [
            ('column_id', 'column_name', 'column_type', 'is_column_not_null', 'column_default_value', 'column_is_primary_key'),
        ]
    }
    Check if there are non-existing column or table names in the query.
    Attempt convert CamelCase to snake_case
    Only useful for SQLCoder (https://github.com/defog-ai/sqlcoder/issues/17)
    """
    space_name_dict = {}
    mapping_dict = {}
    not_existing_query_names = []

    schema_all_names = []
    query_all_tablecolumn_names = []
    query_all_column_names = []
    query_all_table_names = []

    for table_name, columns in schemas.items():
        schema_all_names.append(table_name)
        for col in columns:
            col_id, col_name, col_type, col_notnull, col_defval, col_pk = col
            if ' ' in col_name:
                schema_all_names.append(f'`{col_name}`')
                space_name_dict[col_name] = col_name.replace(' ', '_')
                schema_all_names.append('.'.join([table_name, f'`{col_name}`']))
            else:
                schema_all_names.append(col_name)
                schema_all_names.append('.'.join([table_name, col_name]))

    for k, v in space_name_dict.items():
        sql_query = sql_query.replace(k, v)

    for column in parse_one(sql_query).find_all(exp.Column):
        column_name = column.table+'.'+column.name
        query_all_tablecolumn_names.append(column_name)
        query_all_column_names.append(column.name)

    for table in parse_one(sql_query).find_all(exp.Table):
        query_all_table_names.append(table.name)

    query_all_column_names = list(set(query_all_column_names))
    query_all_table_names = list(set(query_all_table_names))

    # Convert all lists to lower case
    schema_all_names = [name.lower() for name in schema_all_names]
    query_all_tablecolumn_names = [name.lower() for name in query_all_tablecolumn_names]
    query_all_table_names = [name.lower() for name in query_all_table_names]
    query_all_column_names = [name.lower() for name in query_all_column_names] 

    # check if there are non-existing column names
    # try to convert CamelCase to snake_case
    # if the converted name exists in the schema, then add it to the mapping dict
    # if the converted name does not exist in the schema, then add it to the not_existing_query_names list
    for table_name in query_all_table_names:
        if table_name not in schema_all_names:
            if check_snake_case(table_name):
                found = False
                for option in range(2):
                    new_table_name = snake_case2lowercase(table_name, option=option)
                    if new_table_name in schema_all_names:
                        mapping_dict[table_name] = new_table_name
                        found = True
                    if found: break
                if not found:
                    not_existing_query_names.append(table_name)
        else:
            mapping_dict[table_name] = table_name

    for column_name in query_all_column_names:
        if column_name not in schema_all_names:
            if check_snake_case(column_name):
                found = False
                for option in range(2):
                    new_column_name = snake_case2lowercase(column_name, option=option)
                    if new_column_name in schema_all_names:
                        mapping_dict[column_name] = new_column_name
                        found = True
                    if found: break
                if not found:
                    not_existing_query_names.append(column_name)
        else:
            mapping_dict[column_name] = column_name

    for query_name in query_all_tablecolumn_names:
        if query_name not in schema_all_names:
            table_name, column_name = query_name.split('.')
            if table_name in mapping_dict.keys():
                # Here means table_name is wrong, but since we fixed it before
                # so we will map the correct table name and fix the column
                
                new_query_name = mapping_dict[table_name]+'.'+column_name
                if new_query_name in schema_all_names:
                    mapping_dict[query_name] = new_query_name
                else:
                    if check_snake_case(column_name):
                        for option in range(2): 
                            found = False
                            new_column_name = snake_case2lowercase(column_name, option=option)
                            # if only column name is wrong
                            new_query_name = table_name+'.'+new_column_name
                            if new_query_name in schema_all_names:
                                mapping_dict[query_name] = new_query_name
                                found=True
                            else:
                                # if both table name and column name are wrong
                                new_query_name = mapping_dict[table_name]+'.'+new_column_name
                                if new_query_name in schema_all_names:
                                    mapping_dict[query_name] = new_query_name
                                    found=True
                            if found: break
                        if not found:       
                            not_existing_query_names.append(query_name)

    return mapping_dict, not_existing_query_names, sql_query


def lower_table_and_column(sql_query):
    for column in parse_one(sql_query).find_all(exp.Column):
        sql_query.replace(column.name, column.name.lower())

    for table in parse_one(sql_query).find_all(exp.Table):
        sql_query.replace(table.name, table.name.lower())

    return sql_query


def fix_sql_hallucination(mapping_dict:dict, sql_query:str):
    """
    Fix hallucination in SQL query using a mapping dictionary
    """
    
    # Sort the mapping dict by key length
    # This is to prevent the case where a longer key is replaced by a shorter key
    sql_query = lower_table_and_column(sql_query)
    if len(mapping_dict) > 0:
        mapping_dict = {k: mapping_dict[k] for k in sorted(mapping_dict, key=len, reverse=True)}
        
    for query_name, schema_name in mapping_dict.items():
        sql_query = sql_query.replace(query_name, schema_name)
    return sql_query


def check_snake_case(text:str):
    """
    Check if the text is in snake_case
    """
    import re
    return bool(re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', text))

def snake_case2lowercase(text: str, option=0):
    """
    Convert snake_case to lowercase
    """
    if option==0:
        return ''.join([x.lower() for x in text.split('_')])
    else:
        val = ' '.join([x.lower() for x in text.split('_')])
        return f'`{val}`'