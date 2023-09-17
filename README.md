# Possible solutions:

1. Use defog/sqlcoder from huggingface
2. Use LLaMa2 from huggingface but needs finetune since performance really bad: https://medium.com/llamaindex-blog/easily-finetune-llama-2-for-your-text-to-sql-applications-ecd53640e10d
3. Use text-to-SQL LM (not LLM) like T5 and FLAN also from HuggingFace:
    - https://huggingface.co/juierror/text-to-sql-with-table-schema
    - https://huggingface.co/cssupport/t5-small-awesome-text-to-sql
4. Use CodeS: https://github.com/RUCKBReasoning/codes