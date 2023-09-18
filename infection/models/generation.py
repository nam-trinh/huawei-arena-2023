


def generate_sql_query(question: str, db_schema: str, tables_hints: List[str]) -> str:
    # Implement logic to generate an SQL query based on the question and table hints.
    # Replace the "pass" with a calling function to LLM
    
    # Handle the case when table hints are empty or invalid.
    if not tables_hints:
        # Default behavior: Query all tables
        pass
    
    # Handle the general case
    # Example: "SELECT COUNT(*) FROM customers"
    prompt = generate_sql_query_generation_prompt(question, db_schema)
    eos_token_id = tokenizer.convert_tokens_to_ids(["```"])[0]
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda") # or to("cpu")
    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=eos_token_id,
        pad_token_id=eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=5
    )
    
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    sql_query = outputs[0].split("```sql")[-1].split("```")[0].split(";")[0].strip() + ";"
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    
    return sql_query


def generate_answer_with_context(question: str, schema: List[str]) -> str:
    answer_generation_prompt = generate_answer_generation_prompt(question, schema)
    
    ### Use the same procedure
    eos_token_id = tokenizer.convert_tokens_to_ids(["```"])[0]
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda") # or to("cpu")
    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=eos_token_id,
        pad_token_id=eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=5
    )
    
    asnwer = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    
    return answer
    
    