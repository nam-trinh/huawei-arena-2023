from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

model_name = "defog/sqlcoder"
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir='/mnt/4TBSSD/huawei2023cache/')
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    # torch_dtype=torch.bfloat16,
    # load_in_8bit=True,
    load_in_4bit=True,
    device_map="auto",
    use_cache=True,
    cache_dir='/mnt/4TBSSD/huawei2023cache/'
)
