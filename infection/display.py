from IPython.display import display, Markdown

MARKDOWN_STRING_SUCCESS="""
> {answer} 
>
> ---
>
> This answer was obtained based on the following data extracted from the database:
> {table} 

---

This data was obtained by executing the following query:
```sql 
{query} 
```

{chart}

"""

MARKDOWN_STRING_ERROR="""
> {answer}
"""

CHART_STRING = """

---
The followings are some suggested charts based on the data you asked for:

"""

def print_answer(res):
    if 'response_df' in res and res['response_df'] is not None:
        if 'chart' in res['extras']: 
            chart = CHART_STRING
        else: 
            chart = ''
        formatted_markdown = MARKDOWN_STRING_SUCCESS.format(answer=res['answer'].replace('\n', '\n>'),
                                                            table=res['response_df'].to_html(),
                                                            query=res['sql_query'],
                                                            chart=chart)
    else:
        formatted_markdown = MARKDOWN_STRING_ERROR.format(answer=res['answer'].replace('\n', '\n>'))
    
    display(Markdown(formatted_markdown))
    
    if 'response_df' in res and res['response_df'] is not None:
        if 'chart' in res['extras']:
            res['extras']['chart'][0].show()
            res['extras']['chart'][1].show()
