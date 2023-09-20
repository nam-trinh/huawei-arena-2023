from infection.models.llm import SQLCoder, Llama2_7B, Llama2_13B, BaseLLM
from infection.prompt import generate_prompt
from typing import *

def get_model(name: str, **kwargs):
    if name == 'sqlcoder':
        return SQLCoder(**kwargs)
    elif name == 'llama2_7b':
        return Llama2_7B(**kwargs)
    elif name == 'llama2_13b':
        return Llama2_13B(**kwargs)
    else:
        raise NotImplementedError



def generate_llm_response(
        llm: BaseLLM, prompt_template: str,
        question: str, db_schema: str, tables_hints: List[str]=None,
    ) -> str:
    # Implement logic to generate an SQL query based on the question and table hints.
    # Replace the "pass" with a calling function to LLM
    
    # Handle the case when table hints are empty or invalid.
    if not tables_hints:
        # Default behavior: Query all tables
        pass
    
    # Handle the general case
    # Example: "SELECT COUNT(*) FROM customers"
    prompt = generate_prompt(
        prompt_template, 
        question=question, 
        db_schema=db_schema,
        # tables_hints=tables_hints
    )

    outputs = llm.generate(prompt, num_beams=1)
    
    sql_query = outputs[0].split("```sql")[-1].split("```")[0].split(";")[0].strip() + ";"
    return sql_query
