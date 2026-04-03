import torch
import math
import os
import pandas as pd
import json
from transformers import AutoTokenizer, AutoModelForCausalLM

from utils.setting import MODELS, PROMPT_TEMPLATE, GEN_CONFIG, HF_TOKEN
from utils.utils import load_data, get_top_and_bottom_entities, build_prompt

def load_model(model_name):
    print(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=HF_TOKEN,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

def generate_with_metrics(model, tokenizer, prompt, k_top_save=10):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    

    stop_token_id = tokenizer.encode("]", add_special_tokens=False)[-1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=GEN_CONFIG.max_new_tokens,
            temperature=GEN_CONFIG.temperature,
            top_p=GEN_CONFIG.top_p,
            do_sample=GEN_CONFIG.do_sample,
            eos_token_id=[tokenizer.eos_token_id, stop_token_id], # Si ferma al "]"
            output_scores=True,           
            return_dict_in_generate=True  
        )

    generated_ids = outputs.sequences[0][inputs.input_ids.shape[-1]:]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    logits_list = torch.stack(outputs.scores) 
    per_step_metrics = []
    total_entropy = 0

    for t in range(logits_list.shape[0]):
        step_logits = logits_list[t, 0] 
        
        probs = torch.softmax(step_logits, dim=-1)
        
        entropy = -torch.sum(probs * torch.log(probs + 1e-10)).item()
        
        # 3. Salviamo solo i TOP K logit per evitare -Infinity e file giganti
        topk_logits, topk_indices = torch.topk(step_logits, k_top_save)
        
        safe_logits = [l if l != float('-inf') else -999.0 for l in topk_logits.tolist()]
        
        token_id = generated_ids[t].item()
        token_text = tokenizer.decode([token_id])

        per_step_metrics.append({
            "token": token_text,
            "entropy": entropy,
            "top_logits": safe_logits,
            "top_tokens": [tokenizer.decode([idx]) for idx in topk_indices.tolist()]
        })
        total_entropy += entropy

    avg_entropy = total_entropy / len(per_step_metrics) if per_step_metrics else 0
    
    return generated_text, avg_entropy, per_step_metrics

def process_category(file_path, output_dir):
    category_name = os.path.splitext(os.path.basename(file_path))[0]
    df = load_data(file_path)
    selected_entities = get_top_and_bottom_entities(df)

    results = []

    for model_name in MODELS:
        tokenizer, model = load_model(model_name)

        for _, row in selected_entities.iterrows():
            word = row["label"] 
            prompt = build_prompt(PROMPT_TEMPLATE, word)

            try:
                gen_text, avg_ent, step_details = generate_with_metrics(model, tokenizer, prompt)

                results.append({
                    "model": model_name,
                    "qid": row["qid"],
                    "label": word,
                    "generated_text": gen_text,
                    "avg_entropy": avg_ent,
                    "token_details": step_details 
                })

            except Exception as e:
                print(f"Error with {model_name} on {word}: {e}")

        del model
        torch.cuda.empty_cache()

    output_path = os.path.join(output_dir, f"{category_name}_metrics.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Saved: {output_path}")

def main():
    input_dir = "/beegfs/home/ldraetta/BiasWeResearchBy/data"
    output_dir = "/beegfs/home/ldraetta/BiasWeResearchBy/outputs"

    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    print(f"Found {len(files)} category files")

    for file in files:
        file_path = os.path.join(input_dir, file)
        print(f"\nProcessing category: {file}")
        process_category(file_path, output_dir)

    print("\nAll categories processed!")

if __name__ == "__main__":
    main()