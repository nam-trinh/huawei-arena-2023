from typing import List
from tabulate import tabulate
import pandas as pd
from infection.databases.sql3 import SQL3Database

def format_sql_execution(records:List[tuple], column_names: List[str], format:str='table'):
    """
    Format the SQL execution results to a table
    """
    
    if format == 'table':
        results = tabulate(records, tablefmt="github", headers=column_names)
    elif format == 'dataframe':
        try:
            results = pd.DataFrame(records)
            results.columns = column_names
        except:
            return None
    else:
        raise ValueError(f"Unknown format: {format}")
    return results
