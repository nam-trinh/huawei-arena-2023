from transformers import (
    AutoTokenizer, AutoModelForCausalLM,
    LlamaTokenizer, LlamaForCausalLM,
    BitsAndBytesConfig,
    T5Tokenizer, T5ForConditionalGeneration,
    AutoModelForSeq2SeqLM
)
import torch
try:
    import optimum
    USE_OPTIMUM = True
except ImportError:
    USE_OPTIMUM = False


class BaseLLM:
    def __init__(
            self, 
            cache_dir:str, 
            load_in_4bit:bool=False,
            load_in_8bit:bool=False,
            torch_dtype=None,
            quantization_type:str="bnb",
            device:str="cuda"
        ) -> None:
        self.cache_dir = cache_dir


        # Quantization config
        """
        https://huggingface.co/docs/transformers/perf_infer_gpu_many
        """
        self.device = device
        if load_in_4bit:
            if quantization_type == "bnb":
                self.quantization_config = BitsAndBytesConfig(
                    load_in_4bit=load_in_4bit,
                    bnb_4bit_compute_dtype=torch.float16
                )
        else:
            self.quantization_config = None

        self.load_in_4bit = load_in_4bit
        self.load_in_8bit = load_in_8bit
        self.torch_dtype = torch_dtype

    def generate(self, prompt:str, **kwargs):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_new_tokens", 400),
                num_beams=kwargs.get("num_beams", 1),
                num_return_sequences=1,
            )
        
        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        return outputs[0]

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
            cache_dir=self.cache_dir,
            quantization_config=self.quantization_config,
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

    def generate(self, prompt:str, **kwargs):
        eos_token_id = self.tokenizer.convert_tokens_to_ids(["```"])[0]
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device) # or to("cpu")
        
        with torch.no_grad():
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
        
        # Solely based on SQLCoder's output format, the prompt template should follow this format:
        outputs = outputs[0].split("```sql")[-1].split("```")[0].split(";")[0].strip() + ";"
        
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        return outputs


class Llama2_7B(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "meta-llama/Llama-2-7b-chat-hf"
        # "meta-llama/Llama-2-7b-chat-hf"
        # "openlm-research/open_llama_3b_v2"
        #
        # 
        # "openlm-research/open_llama_7b_v2"
        # "openlm-research/open_llama_13b_v2"

        self.token = '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'
        self.tokenizer = LlamaTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir,
            token=self.token
        )
        self.model = LlamaForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            load_in_4bit=self.load_in_4bit,
            load_in_8bit=self.load_in_8bit,
            device_map="auto" if self.device == "cuda" else "cpu",
            use_cache=True,
            cache_dir=self.cache_dir,
            token=self.token,
            quantization_config=self.quantization_config,
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

    def generate(self, prompt:str, **kwargs):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_new_tokens", 400),
                num_beams=kwargs.get("num_beams", 1),
                num_return_sequences=1,
            )
        
        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        return outputs[0]


class Llama2_13B(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "meta-llama/Llama-2-13b-chat-hf"
        #"openlm-research/open_llama_3b_v2"
        #
        # 
        # "openlm-research/open_llama_7b_v2"
        # "openlm-research/open_llama_13b_v2"

        self.token = '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'
        self.tokenizer = LlamaTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir,
            token=self.token
        )
        self.model = LlamaForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            load_in_4bit=self.load_in_4bit,
            device_map="auto",
            use_cache=True,
            cache_dir=self.cache_dir,
            token=self.token,
            quantization_config=self.quantization_config,
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

class CodeS(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "seeklhy/codes-1b" #"microsoft/CodeGPT-small-py-adaptedGPT2"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            load_in_4bit=self.load_in_4bit,
            device_map="auto" if self.device == "cuda" else "cpu",
            use_cache=True,
            quantization_config=self.quantization_config,
            cache_dir  = self.cache_dir
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

class CodeS_3B(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "seeklhy/codes-3b" #"microsoft/CodeGPT-small-py-adaptedGPT2"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            load_in_4bit=self.load_in_4bit,
            device_map="auto" if self.device == 'cuda' else 'cpu',
            use_cache=True,
            quantization_config=self.quantization_config,
            cache_dir  = self.cache_dir
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()
        
class CodeS_7B(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "seeklhy/codes-7b" #"microsoft/CodeGPT-small-py-adaptedGPT2"
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, cache_dir=self.cache_dir
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            load_in_4bit=self.load_in_4bit,
            device_map="auto" if self.device == 'cuda' else 'cpu',
            use_cache=True,
            quantization_config=self.quantization_config,
            cache_dir  = self.cache_dir
        )

        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

class FlanT5(BaseLLM):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "juierror/text-to-sql-with-table-schema"
        #'cssupport/t5-small-awesome-text-to-sql'
        if self.model_name == "juierror/text-to-sql-with-table-schema":
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name , cache_dir=self.cache_dir)
        else:
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            self.tokenizer = T5Tokenizer.from_pretrained('t5-small', cache_dir=self.cache_dir)

        self.model = self.model.to(self.device)
        if USE_OPTIMUM:
            self.model.to_bettertransformer()
        self.model.eval()

class NSQL350(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "NumbersStation/nsql-350M"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        self.model.eval()

    def generate(self, prompt:str, **kwargs):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_new_tokens", 400),
                num_beams=kwargs.get("num_beams", 1),
                num_return_sequences=1,
            )
        
        outputs = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        if self.device == "cuda":
            torch.cuda.synchronize()
        return outputs[0]
