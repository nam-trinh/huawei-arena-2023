import random
from typing import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from infection.databases import format_sql_execution

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

def suggest_plot(df, height=600):
    """
    Suggest two plots based on the data type of the columns

    Parameters:
    -----------
    df: pd.DataFrame
    height: int

    Returns:
    --------
    figs: dict of plotly figures

    """
    # Separate numerical and object columns
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    object_columns = df.select_dtypes(include=['object']).columns.tolist()

    # If there is only 1 numerical column and an object column, draw a bar chart and a line chart
    if len(numerical_columns) == 1 :
        kwargs = {
            'y': numerical_columns[0],
            'template': 'plotly_white',
            'height': height,
        }
        if len(object_columns) > 0:
            x_axis_column = random.sample(object_columns, 1)[0]
            color_column = random.sample(object_columns, 1)[0]
            kwargs.update({
              'x': x_axis_column,
              'color': color_column,
            })

        # Create a bar chart
        bar_fig = px.bar(df, **kwargs)
        kwargs.pop('color', None)
        # Create a line chart
        line_fig = px.line(df, **kwargs)

        output_figs = [bar_fig, line_fig]        


    # If there are two or more numerical columns and an object column, draw a scatter plot and a line chart
    elif len(numerical_columns) >= 2:
        kwargs = {
          'template': 'plotly_white',
          'height': height
        }

        if len(object_columns) > 0:
            # If there is at least one object column, randomly choose one.
            label_column = random.sample(object_columns, 1)[0]
            x_axis_column = random.sample(object_columns, 1)[0]
            kwargs.update({'color': label_column})

        # Randomly select two numerical columns for the scatter plot
        scatter_columns = random.sample(numerical_columns, 2)

        # Randomly select two numerical columns for the line chart
        line_columns = random.sample(numerical_columns, 2)

        # Create a scatter plot
        scatter_fig = px.scatter(df, x=scatter_columns[0], y=scatter_columns[1], **kwargs)

        # Create a line chart with two lines
        if len(object_columns) > 0:
            kwargs = {'x': df[x_axis_column]}
        else:
            kwargs = {}

        # Create the first trace for the first y-axis
        trace1 = go.Scatter(y=df[line_columns[0]], mode='lines+markers', name=line_columns[0], **kwargs)
        # Create the second trace for the second y-axis
        trace2 = go.Scatter(y=df[line_columns[1]], mode='lines+markers', yaxis='y2', name=line_columns[1], **kwargs)

        # Create the layout with two y-axes
        layout = go.Layout(
            title='Line Chart with Two Y-Axes',
            yaxis=dict(title=line_columns[0]),
            yaxis2=dict(title=line_columns[1], overlaying='y', side='right'),
            height=height,
            template='plotly_white'
        )

        line_fig = go.Figure(data=[trace1, trace2], layout=layout)

        output_figs = [scatter_fig, line_fig]        

    else:
        return None

    return output_figs

