import os
import re
import json
import time
import datetime
import hashlib
import numpy as np
import pandas as pd


TEST_SETS = [
        'data/test4242/example-data/example-covid-vaccinations',
        'data/test4242/example-data/example-data',
        'data/test4242/example-data/example-simple',
        'data/test4242/example-data/sql-murder-mystery',
        'data/test4242/example-data/tallest_buildings_global',
        'data/test4242/example2-data/example-covid-vaccinations',
        'data/test4242/example2-data/example-simple',
        'data/test4242/example2-data/sql-murder-mystery',
        'data/test4242/example2-data/tallest_buildings_global',
        'data/test4242/validation-data/danger',
        'data/test4242/validation-data/example-data',
        'data/test4242/validation-data/sql-murder-mystery',
        'data/test4242/validation-data/tallest_buildings_global',
        'data/test4242/validation2-data/danger',
        'data/test4242/validation2-data/example-data',
        'data/test4242/validation3-data/danger',
]



def mock_connect_fun(path):
    from random import random
    if random() < 0.1:
        raise Exception("mock error")
    return None

def mock_query_fun(query, table_id, db):
    from random import random
    if random() < 0.1:
        raise Exception("mock error")
    return 'abc'


class Hackaton_Validator():

    def __init__(self):
        self._data = []
        self._h1 = hashlib.sha256()
        self._h2 = hashlib.sha256()
        self._h3 = hashlib.sha256()
        self._h4 = hashlib.sha256()

    def load_json(self, path):
        try:
            return json.load(open(path, 'r'))
        except Exception as e:
            return None

    def load_test_files(self):
        F = []
        dir_path = os.path.dirname(__file__)
        for p in TEST_SETS:
            db = os.path.abspath(os.path.join(dir_path, 'db', p + '.sqlite3'))
            qq = os.path.abspath(os.path.join(dir_path, 'qq', p + '.json'))
            F.append((db,qq))
        return F

    def get_ground_truth(self, qa_data):
        return (qa_data['question'], qa_data['table_id'])

    def append_data(self, t1, t2, t3, t4):
        t1=str(t1)
        t2=str(t2)
        t3=str(t3)
        t4=str(t4)
        self._data.append( (t1, t2, t3, t4) )
        if len(self._data)>1 and (self._data[-2][0] != self._data[-1][0]):
            h0 = self._h1
            self._h1 = self._h2
            self._h2 = self._h3
            self._h3 = self._h4
            self._h4 = h0
        self._h1.update(bytearray(t1, encoding='utf-8'))
        self._h2.update(bytearray(t2, encoding='utf-8'))
        self._h3.update(bytearray(t3, encoding='utf-8'))
        self._h4.update(bytearray(t4, encoding='utf-8'))

    def append_digest(self):
        h1 = self._h1.hexdigest()
        h2 = self._h2.hexdigest()
        h3 = self._h3.hexdigest()
        h4 = self._h4.hexdigest()
        self._data.append((h1, h2, h3, h4))
        return ('-'.join(self._data[-1]))[::8]

    def score_test_case(self, query_fun, db_conn, test_case_data):
        question, table_id = test_case_data
        answer = None
        e = ''
        try:
            answer = query_fun(question, table_id, db_conn)
            return question, answer, e
        except Exception as e:
            return question, answer, e

    def score_test_cases(self, connect_fun, query_fun, time_limit=600):
        test_files = self.load_test_files()
        start_time = time.perf_counter()
        self.append_data('_start', '', str(datetime.datetime.now()), str(time.perf_counter() - start_time))
        for (db_path, test_file) in test_files:
            test_name = os.path.basename(test_file)
            test_cases = self.load_json(test_file)
            if test_cases is not None:
                self.append_data('_case', '', str(datetime.datetime.now()), str(time.perf_counter() - start_time))
                try:
                    db_conn = connect_fun(db_path)
                except Exception as e:
                    for tc in test_cases:
                        self.append_data(test_name, tc['question'], '', f"**CONNECT EXCEPTION** {e}")
                else:
                    for tc in test_cases:
                        try:
                            tc_data = self.get_ground_truth(tc)
                            if not self.check_time_limit(start_time, time_limit):
                                question, answer, e = self.score_test_case(query_fun, db_conn, tc_data)
                                self.append_data(test_name, question, answer, e)
                            else:
                                self.append_data(test_name, question, '', 'TIMEOUT')
                        except Exception as e:
                            self.append_data(test_name, tc['question'], '', f"**EXCEPTION** {e}")


        self.append_data('_end', '', str(datetime.datetime.now()), str(time.perf_counter() - start_time))
        d = self.append_digest()
        df = pd.DataFrame(data=self._data, columns=['database', 'question', 'answer', 'error'])
        df.to_csv(f'eval_results_{d}.csv', index=False)
        print(f'Please share eval_results_{d}.csv file with the Judges')
        return df


    def check_time_limit(self, start_time, time_limit):
        return (time.perf_counter() - start_time) >= time_limit



def run_all_tests(connect_fun, query_fun):
    V=Hackaton_Validator()
    V.score_test_cases(connect_fun, query_fun)


if __name__ == '__main__':

    run_all_tests(mock_connect_fun, mock_query_fun)


