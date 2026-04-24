#RESULTS ANALYSIS
MAX_LEN = None

MODEL_COLORS = {
    "Llama-3.1-8B-Instruct": "#1f77b4",
    "Mistral-7B-Instruct-v0.3": "#ff7f0e",
    "Qwen3.5-9B": "#2ca02c",
}

MODEL_FAMILY = {
    "Llama-3.1-8B-Instruct": "llama",
    "Mistral-7B-Instruct-v0.3": "mistral",
    "Qwen3.5-9B": "qwen",
}

def parse_filename(filename):
    parts = filename.replace(".json", "").split("_")
    category = parts[0]
    model = "_".join(parts[4:])
    return category, model


def model_mapping(model):
    if model == "Llama-3.1-8B-Instruct":
        return "Llama"
    elif model == "Mistral-7B-Instruct-v0.3":
        return "Mistral"
    else:
        return "Qwen"


def get_color(model):
    return MODEL_COLORS.get(model, "black")
