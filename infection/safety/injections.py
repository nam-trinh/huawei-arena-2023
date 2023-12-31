from transformers import pipeline
import torch

class InjectionDetector:
    """
    Class for detecting SQL injection and prompt injection
    """
    def __init__(self):

        self.prompt_injection_pipe = pipeline(
            "text-classification", 
            model="deepset/deberta-v3-base-injection",
            device='cuda'
        )

        self.sql_injection_pipe = pipeline(
            "text-classification", 
            model="cssupport/mobilebert-sql-injection-detect",
            device='cuda'
        )

        self.mutation_commands = [
            'INSERT', 'UPDATE', 
            'DELETE', 'DROP', 'TRUNCATE', 
            'ALTER', 'CREATE'
        ]

    def prompt_injection_classify(self, prompt:str, **kwargs):
        # return True if prompt injection is detected
        with torch.no_grad():
            res = self.prompt_injection_pipe(prompt)[0]['label'] == 'INJECTION'
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        return res

    def sql_injection_classify(self, prompt:str, **kwargs):
        # return True if SQL injection is detected
        with torch.no_grad():
            res = self.sql_injection_pipe(prompt)[0]['label'] == 'LABEL_1'
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        return res

    
    def mutation_classify(self, prompt:str, **kwargs):
        # return True if SQL databse mutation is detected
        for command in self.mutation_commands:
            if command in prompt:
                return True

        return False