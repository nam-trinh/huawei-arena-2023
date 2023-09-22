from typing import *

class Database:
    def __init__(self):
        pass

    def execute_sql(self, sql_query:str):
        raise NotImplementedError

    def get_schemas(self, table_hints=None):
        raise NotImplementedError
    
    def get_foreign_keys(self, table_hints=None):
        raise NotImplementedError
    
    def get_examples(self, num_examples:int=5, table_hints=None):
        raise NotImplementedError
    
    def _format_schemas_string(self, schemas:Dict, foreign_keys:List, examples:Dict = None, num_examples:int=1):
        raise NotImplementedError
    
    def format_schemas(self, table_hints=None, num_examples:int=1):
        schemas = self.get_schemas(table_hints=table_hints)
        foreign_keys = self.get_foreign_keys(table_hints=table_hints)
        examples = self.get_examples(num_examples=num_examples, table_hints=table_hints)
        return self._format_schemas_string(schemas, foreign_keys, examples, num_examples=num_examples)