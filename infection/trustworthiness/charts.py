from typing import *
from infection.database import format_sql_execution

def plot_sql_chart(
        records:List[tuple], 
        column_names:List[str],
        chart_type:str, 
    ):
    """
    Visualize the SQL response using the given chart type
    """

    if chart_type not in [
        'barh', 'bar', 'line',  
        'scatter', 'pie', 'hist', 
        'box'
        ]:
        return None

    try:
        sql_response_df = format_sql_execution(records, column_names, format='dataframe')
        fig = sql_response_df.plot(
            x=column_names[0], 
            y=column_names[1],
            kind=chart_type,
        ).get_figure()
    except:
        return None

    return fig
