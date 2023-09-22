import sqlite3
from typing import *
from tabulate import tabulate
from infection.databases.base import Database

class SQL3Database(Database):
    def __init__(self, database_name: str, **kwargs):
        try:
            self.connection = sqlite3.connect(database_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            self.connection = None
            self.cursor = None

    def execute_sql(self, sql_query: str):
        """
        Execute the given SQL query
        """
        try:
            self.cursor.execute(sql_query)
            records = self.cursor.fetchall()
            column_names = [i[0] for i in self.cursor.description]
            return records, column_names
        except sqlite3.Error as e:
            print(f"Error executing the SQL query: {e}")
            return None, None

    def get_schemas(self, table_hints=None):
        '''
        get the schema information from this database
        '''
        tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
        tableList=self.cursor.execute(tableQuery).fetchall()
        tables = {}
        for table in tableList:
            tableName=table[0]
            columnQuery="PRAGMA table_info('%s')" % tableName
            schema=self.cursor.execute(columnQuery).fetchall()
            tables[tableName] = schema
        return tables

    def get_foreign_keys(self, table_hints=None):
        '''
        get the schema information from this database
        '''
        tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
        tableList=self.cursor.execute(tableQuery).fetchall()
        tables = []
        for table in tableList:
            tableName=table[0]
            columnQuery="PRAGMA foreign_key_list('%s')" % tableName
            fks=self.cursor.execute(columnQuery).fetchall()
            for fk in fks:
                fk_id, _, fk_table, fk_from, fk_to, _, _, _ = fk
                tables.append(
                    ('.'.join([tableName,fk_from]), '.'.join([fk_table, fk_to]))
                )
        return tables

    def get_examples(self, num_examples:int=5, table_hints=None):
        '''
        get the schema information from this database
        '''
        tableQuery="SELECT name FROM sqlite_master WHERE type='table'"
        tableList=self.cursor.execute(tableQuery).fetchall()
        tables = {}
        for table in tableList:
            tableName=table[0]
            columnQuery=f"SELECT * FROM {tableName} LIMIT {num_examples}"
            examples=self.cursor.execute(columnQuery).fetchall()
            tables[tableName] = tabulate(examples, tablefmt="github", headers=[i[0] for i in self.cursor.description])
        return tables

    def _format_schemas_string(self, schemas:Dict, foreign_keys:List, examples:Dict = None, num_examples:int=1):
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

    def format_schemas(self, table_hints=None, add_examples:int = 0):
        """
        Format the SQL schemas and foreign keys to a string
        """
        schemas = self.get_schemas(table_hints)
        foreign_keys = self.get_foreign_keys(table_hints)

        examples = None
        if add_examples:
            if add_examples > 0:
                examples = self.get_examples(num_examples=add_examples, table_hints=table_hints)

        return self._format_schemas_string(schemas, foreign_keys, examples=examples, num_examples=add_examples)