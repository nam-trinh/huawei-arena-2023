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

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{question}`:
```sql
"""

ANSWER_GENERATION_PROMPT_TEMPLATE = """### Instructions:
Your task is to convert a returned schema into an answer to the question:

### Input:
Generate an answer to the `{question}` based on the schema.
This query will run on a database whose schema is represented in this string:
{returned_schema}

Your answer should be short, concise and straight to the point.

### Response with the following format:
Based on your question and the returned schema, here is the answer I have generated to answer the question `{question}`:
"""

def generate_sql_query_generation_prompt(question, db_schema):
    return SQL_QUERY_PROMPT_TEMPLATE.format(question=question, db_schema=db_schema)

def generate_answer_generation_prompt(question, returned_schema):
    return ANSWER_GENERATION_PROMPT_TEMPLATE.format(question=question, returned_schema=str(returned_schema))