from sqlglot import parse_one, exp
from infection.database import get_schemas

def check_sql_hallucination(cursor, sql_query:str):
    """
    Check if there are non-existing column or table names in the query.
    Attempt convert CamelCase to snake_case
    Only useful for SQLCoder (https://github.com/defog-ai/sqlcoder/issues/17)
    """
    schema_all_names = []
    query_all_column_names = []
    query_all_table_names = []
    
    schemas = get_schemas(cursor)
    for table_name, columns in schemas.items():
        schema_all_names.append(table_name)
        for col in columns:
            col_id, col_name, col_type, col_notnull, col_defval, col_pk = col
            schema_all_names.append('.'.join([table_name, col_name]))

    for column in parse_one(sql_query).find_all(exp.Column):
        column_name = column.table+'.'+column.name
        query_all_column_names.append(column_name)

    for table in parse_one(sql_query).find_all(exp.Table):
        query_all_table_names.append(table.name)

    query_all_column_names = list(set(query_all_column_names))
    query_all_table_names = list(set(query_all_table_names))

    # Convert all lists to lower case
    schema_all_names = [name.lower() for name in schema_all_names]
    query_all_column_names = [name.lower() for name in query_all_column_names]
    query_all_table_names = [name.lower() for name in query_all_table_names]

    # check if there are non-existing column names
    # try to convert CamelCase to snake_case
    # if the converted name exists in the schema, then add it to the mapping dict
    # if the converted name does not exist in the schema, then add it to the not_existing_query_names list
    mapping_dict = {}
    not_existing_query_names = []
    for query_name in query_all_table_names:
        if query_name not in schema_all_names:
            if check_snake_case(query_name):
                new_query_name = snake_case2lowercase(query_name)
                if new_query_name in schema_all_names:
                    mapping_dict[query_name] = new_query_name
    
    for query_name in query_all_column_names:
        if query_name not in schema_all_names:
            table_name, column_name = query_name.split('.')
            if table_name in mapping_dict.keys():

                # if only table name is wrong
                new_query_name = mapping_dict[table_name]+'.'+column_name
                if new_query_name in schema_all_names:
                    mapping_dict[query_name] = new_query_name
                else:
                    if check_snake_case(column_name):
                        new_column_name = snake_case2lowercase(column_name)

                        # if only column name is wrong
                        new_query_name = table_name+'.'+new_column_name
                        if new_query_name in schema_all_names:
                            mapping_dict[query_name] = new_query_name
                        else:
                            # if both table name and column name are wrong
                            new_query_name = mapping_dict[table_name]+'.'+new_column_name
                            if new_query_name in schema_all_names:
                                mapping_dict[query_name] = new_query_name
                            else:
                                not_existing_query_names.append(query_name)

    return mapping_dict, not_existing_query_names

def fix_sql_hallucination(mapping_dict:dict, sql_query:str):
    """
    Fix hallucination in SQL query using a mapping dictionary
    """
    
    # Sort the mapping dict by key length
    # This is to prevent the case where a longer key is replaced by a shorter key
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

def snake_case2lowercase(text: str):
    """
    Convert snake_case to lowercase
    """
    return ''.join([x.lower() for x in text.split('_')])