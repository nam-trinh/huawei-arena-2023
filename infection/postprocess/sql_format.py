from tabulate import tabulate
def format_sql_execution(sql_response, sql_schema):
    results = tabulate(sql_response, tablefmt="jira", headers=sql_schema)
    return results