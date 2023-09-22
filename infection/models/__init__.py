from typing import *
from infection.prompt import generate_prompt
from infection.models.llm import SQLCoder, Llama2, BaseLLM, CodeS, FlanT5

def get_model(name: str, **kwargs):
    if name == 'sqlcoder':
        return SQLCoder(**kwargs)
    elif name == 'llama2':
        return Llama2(**kwargs)
    elif name == 'codes':
        return CodeS(**kwargs)
    elif name == 'flant5':
        return FlanT5(**kwargs)
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