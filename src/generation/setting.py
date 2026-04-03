from dataclasses import dataclass

HF_TOKEN = ""

PROMPT_TEMPLATE = "write a short biography of  {word} no longer than one paragraph. IMPORTANT: Give as output only the biography between square brackets in the following format: [biography]"

MODELS = [
    "meta-llama/Meta-Llama-3-8B-Instruct"
   # "mistralai/Mistral-7B-Instruct-v0.2",
    #"google/gemma-7b-it"
]

@dataclass
class GenerationConfig:
    max_new_tokens: int = 300
    temperature: float = 0.7
    top_p: float = 0.9
    do_sample: bool = True

GEN_CONFIG = GenerationConfig()

