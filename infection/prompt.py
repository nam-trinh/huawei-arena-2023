SQL_QUERY_PROMPT_TEMPLATE = """### Instructions:
Your task is to convert a question into a SQL query, given a SQLlite database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float
- Use correct table names and column names, case sensitive
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
You were given a query '{question}' and given a data cue in tabular format:
'{returned_schema}'

where each row represents a data point, and the columns are separated by "|"

Now, you should formulate a response to answer the question '{question}' based on the data in the table.
If you could not find any relevant information in the data cue, you should say that you don't know the answer.
Do not make up any data
Do not make up any data
Do not make up any data
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
If no chart is suitable, you can answer with "none".
Do not explain your answer. Your response should be only a single word from the available options.
    
### Response:

"""

LLAMA2_ANSWER_GENERATION_PROMPT_TEMPLATE = """
<s>[INST] <<SYS>>
Act as a data analyst, give a normal text answer to a query using the extracted tabular data.
<</SYS>>

You are given a query '{question}' and a data cue in tabular format:
'{returned_schema}'

where each row represents a data point, and the columns are separated by "|"

Now, you should formulate a response to answer the question '{question}' based on the data in the table.
If you could not find any relevant information in the data cue, or the data cue is empty, you should say that you don't know the answer.
Only base your answer on the data. Do not make up or assume any data
Your response should be short, concise and straight to the point.

[/INST]
"""

LLAMA2_CHART_GENERATION_PROMPT_TEMPLATE = """
<s>[INST] <<SYS>>
Act as a data analyst, give a suggestion about a type of chart that can be used to create a visualization 
based on the query and the extracted tabular data.
<</SYS>>

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
If no chart is suitable, you can answer with "none".
Do not explain your answer or extend your answer. Your response should only be a single word from the available options.

[/INST]
"""


SQL_SAFETY_PROMPT_TEMPLATE = """### Instructions:
 You will be given a SQL query to validate its safety.
Your task is to check if the query is safe to run on the database or not.
You should not allow any query that can cause a security breach or a data modification.
Your response should be either [YES] or [NO]. Provide explaination if possible.

### SQL query:
{sql_query}
    
### Response:

"""    

LLAMA2_SAFETY_PROMPT_TEMPLATE = """
<s>[INST] <<SYS>>
Act as a database analyst and security expert. You have detected a malicious pattern that could cause a security breach or a data modification in the input SQL query of the user.
You should explain why it is dangerous to proceed with the SQL query and suggest users to modify their question.
Your response should be short, concise and straight to the point, limit within 3 sentences.
<</SYS>>

You are given this database schema related to the user's query:
"{db_schema}"

Explain why user should not run this SQL query and suggest alternative SQL queries that are safe to run, limit within 3 sentences.
"{sql_query}"

[/INST]
"""

LLAMA2_ERROR_PROMPT_TEMPLATE = """
<s>[INST] <<SYS>>
Act as a database analyst and security expert. You have detected an error when trying to execute the query of the user.
You should explain why that error occurs and suggest users to modify their query.
Your response should be short, concise and straight to the point, limit within 3 sentences.
<</SYS>>

You are given this database schema related to the user's query:
"{db_schema}"

The input query from user is:
"{question}"

The error message you have detected is:
"{error_message}"

Explain why user should not run the query and suggest alternative query that are safe to run, limit within 3 sentences.

[/INST]
"""   



def generate_prompt(prompt_template, **kwargs):
    return prompt_template.format(**kwargs)


def list_all_templates():
    global_vars = globals()
    var_names = [var for var in global_vars if not callable(global_vars[var]) and not var.startswith("__")]
    print("Available prompt templates:")
    print("---------------------------")
    for var_name in var_names:
        print(var_name)

def show_template(template_name):
    global_vars = globals()
    if template_name in global_vars:
        print(global_vars[template_name])
    else:
        print("Template not found")
    
