from infection.models.llm import SQLCoder, Llama2_7B, Llama2_13B, BaseLLM, CodeS, CodeS_3B, CodeS_7B, FlanT5
from infection.prompt import generate_prompt
from typing import *

def get_model(name: str, **kwargs):
    if name == 'sqlcoder':
        return SQLCoder(**kwargs)
    elif name == 'llama2_7b':
        return Llama2_7B(**kwargs)
    elif name == 'llama2_13b':
        return Llama2_13B(**kwargs)
    elif name == 'codes':
        return CodeS(**kwargs)
    elif name == 'codes-3b':
        return CodeS_3B(**kwargs)
    elif name == 'codes-7b':
        return CodeS_7B(**kwargs)
    elif name == 'flant5':
        return FlanT5(**kwargs)
    elif name == 'nsql350':
        return NSQL350(**kwargs)
    else:
        raise NotImplementedError

def get_model_response(model: BaseLLM, prompt_template:str, **kwargs):
    prompt = generate_prompt(prompt_template, **kwargs)

    num_beams = kwargs.pop('num_beams', 1)
    outputs = model.generate(prompt, num_beams=num_beams)

    catchphrase = kwargs.get('catchphrase',None)
    if catchphrase is not None:
        result = outputs.split(catchphrase)[-1].strip()
    else:
        result = outputs.strip()
    return result
