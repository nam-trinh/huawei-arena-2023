import os
import re
import json
import time
import numpy as np
import pandas as pd
import sqlite3
from io import StringIO 


class TestObject:
    def __init__(self, path):
        self._db = sqlite3.connect(path) 

    def sql(self, sql_query):
        return pd.read_sql_query(sql_query, self._db)

    def text_to_sql(self, question, tables):
        return question   # magic

    def result_to_text(self, question, query, result):
        return "Here is what I think:\n" + result.to_string()

    def question(self, question, tables):
        query = self.text_to_sql(question, tables)
        answer = self.sql(query)
        return self.result_to_text(question, query, answer)


def test_connect_fun(path):
    db = TestObject(path)
    return db

def test_query_fun(query, table_id, db):
    return db.question(query, table_id)


def run_test(test_name, connect_fun, query_fun):
    with open(test_name + ".json", "r") as test_file:
        test_cases = json.load(test_file)

    db = connect_fun(test_name + ".sqlite3")
    for test_case in test_cases:
        (f"Question: {test_case['question']}")
        if 'sql' in test_case and len(test_case['sql']):
            sql = test_case['sql'][0]
            print(f"Example query: {test_case['sql'][0]}")
        else:
            sql = None
        expected = pd.read_json(StringIO(test_case['sql_result']))
        print(f"Example result:")
        print(expected.to_string())
        
        try:
            model_result = query_fun(test_case['question'], test_case['table_id'], db)
        except Exception as E:
            model_result = f"ERROR Running SQL: {E}"
        print(f"Model result:")
        print(model_result)
        print()

        
def run_many_tests(tests, connect_fun, query_fun):
    for test in tests:
        try:
            run_test(test, connect_fun, query_fun)
        except Exception as E:
            print(f"** EXCEPTION: {E}")



def run_all_tests(connect_fun, query_fun, path=''):
    TEST_SETS = [
        'example-data/example-covid-vaccinations',
        'example-data/example-data',
        'example-data/example-simple',
        'example-data/sql-murder-mystery',
        'example-data/tallest_buildings_global',
        'example2-data/example-covid-vaccinations',
        'example2-data/example-simple',
        'example2-data/sql-murder-mystery',
        'example2-data/tallest_buildings_global'
    ]
    TEST_SETS = [path + x for x in TEST_SETS]
    run_many_tests(TEST_SETS, connect_fun, query_fun)


if __name__ == '__main__':
    run_all_tests(test_connect_fun, test_query_fun)

