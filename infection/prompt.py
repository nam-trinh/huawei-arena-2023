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

ANSWER_GENERATION_PROMPT_TEMPLATE = """
Generate a suitable answer to a prompt based on the extracted tabular information.
The information extracted from the database is as follows:
{returned_schema}
Each row represents a data point, and the columns are separated by "|".
Your answer should be short, concise and straight to the point.
The prompt is as followed: `{question}`

### Response:
Based on your instructions, here is the answer I have generated to give an appropriate response:
```sql
"""

def generate_prompt(prompt_template, **kwargs):
    return prompt_template.format(**kwargs)