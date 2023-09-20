SQL_QUERY_PROMPT_TEMPLATE = """### Instructions:
Your task is to convert a question into a SQL query, given a SQLlite database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float
### Input:
Generate a SQL query that answers the question `{question}`.
This query will run on a database whose schema is represented in this string:
{db_schema}

These are some hints to help you in this task. 
Some of these hints can be wrong, so only use relevant ones:
{tables_hints}

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
```sql
"""


ANSWER_GENERATION_PROMPT_TEMPLATE = """### Instructions:
Act as a data analyst, give a normal text answer to query by using the extracted tabular data.

### Input:
You were given a query '{question}' and already found the answer as in a tabular format:
'{returned_schema}'

where each row represents a data point, and the columns are separated by "|"

Now, you should formulate a verbally comprehensive answer to answer the question '{question}' based on the data in the table.
**Do not make up any data**
Your response should be short, concise and straight to the point.

### Response:

"""
# Based on your instructions, here is the answer I have generated:
# ```sql
#a comprehensive way to create a verbally normal response
CHART_GENERATION_PROMPT_TEMPLATE = """### Instructions:
Act as a data analyst, give a suggestion about a type of chart that can be used to create a visualization 
based on the query and the extracted tabular data.

### Input:
You are given a query '{question}' and an extracted tabular data:
'{returned_schema}'

where each row represents a data point, and the columns are separated by "|"

Now, you should choose only one type of chart from the available charts below to answer:
    - barh 
    - bar 
    - line 
    - scatter 
    - pie 
    - hist 
    - box 
    - none
Your response should be only one word from the above options.
If no chart is suitable, you can answer with "none".
    
### Response:

"""

SQL_SAFETY_PROMPT_TEMPLATE = """### Instructions:
Act as a database analyst and security expert. You will be given a SQL query to validate its safety.
Your task is to check if the query is safe to run on the database or not.
You should not allow any query that can cause a security breach or a data modification.
Your response should be either [YES] or [NO]. Provide explaination if possible.

### SQL query:
{sql_query}
    
### Response:

"""    



def generate_prompt(prompt_template, **kwargs):
    return prompt_template.format(**kwargs)