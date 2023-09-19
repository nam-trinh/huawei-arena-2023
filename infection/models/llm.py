from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class BaseLLM:
    def __init__(
            self, 
            cache_dir:str, 
            load_in_4bit:bool=False,
            load_in_8bit:bool=False,
            torch_dtype=None,
        ) -> None:
        self.cache_dir = cache_dir
        self.load_in_4bit = load_in_4bit
        self.load_in_8bit = load_in_8bit
        self.torch_dtype = torch_dtype

    def generate(self, **kwargs):
        pass

class SQLCoder(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "defog/sqlcoder"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=self.torch_dtype,
            load_in_8bit=self.load_in_8bit,
            load_in_4bit=self.load_in_4bit,
            device_map="auto",
            use_cache=True,
            cache_dir=self.cache_dir
        )

    def generate(self, prompt, **kwargs):
        eos_token_id = self.tokenizer.convert_tokens_to_ids(["```"])[0]
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda") # or to("cpu")
        generated_ids = self.model.generate(
            **inputs,
            num_return_sequences=1,
            eos_token_id=eos_token_id,
            pad_token_id=eos_token_id,
            max_new_tokens=kwargs.get("max_new_tokens", 400),
            do_sample=False,
            num_beams=kwargs.get("num_beams", 1)
        )
        
        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        return outputs