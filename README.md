# Possible solutions:

1. Use defog/sqlcoder from huggingface
2. Use LLaMa2 from huggingface but needs finetune since performance really bad: https://medium.com/llamaindex-blog/easily-finetune-llama-2-for-your-text-to-sql-applications-ecd53640e10d
3. Use text-to-SQL LM (not LLM) like T5 and FLAN also from HuggingFace:
    - https://huggingface.co/juierror/text-to-sql-with-table-schema
    - https://huggingface.co/cssupport/t5-small-awesome-text-to-sql
4. Use CodeS: https://github.com/RUCKBReasoning/codes


# To-dos
- [x] End-to-end pipeline
- [x] Convert schema description from database to sqlcoder's db schema format
- [ ] Verify input string for potential danger (LLM?)
- [ ] Handle execution error 
- [ ] SQL injection test
- [ ] Check if the model can explain the answer generation workflow 
- [ ] Loop for following-up questions ...

# Setup
- Execute the following command:
```
cd huawei-arena-2023
pip install -e .
```

- Use the notebook: [infection-sql.ipynb](./notebooks/infection-sql.ipynb)
