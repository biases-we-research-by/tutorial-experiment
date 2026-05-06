import os
import json
import numpy as np
import matplotlib.pyplot as plt
import csv
from src.utils.utils import  *

# =========================
# CONFIG
# =========================
DATA_DIR = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/Generation output updated"
CSV_OUTPUT = "/Users/liadraetta/Desktop/progetti/Projects/tutorial-experiment/cleaning_tracking.csv"

# =========================
# LOAD + CLEAN
# =========================
files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

results = {}
stats = {}

global_entropy_head = []
global_entropy_tail = []

csv_rows = []

for file in files:
    category, model = parse_filename(file)

    with open(os.path.join(DATA_DIR, file), "r") as f:
        data = json.load(f)

    stats.setdefault(category, {})
    stats[category].setdefault(model, {
        "total": 0,
        "kept": 0,
        "filtered": 0,
        "no_pattern": 0,
        "head": {"total": 0, "kept": 0, "filtered": 0, "no_pattern": 0},
        "tail": {"total": 0, "kept": 0, "filtered": 0, "no_pattern": 0},
    })

    clean_data = []

    for ex in data:
        stats[category][model]["total"] += 1

        is_head = ex.get("pareto_claims") == 1
        group = "head" if is_head else "tail"
        stats[category][model][group]["total"] += 1

        cleaned_text, status = clean_generated_text(
            ex.get("generated_text", ""), model
        )

        kept = status == "ok"
        # CSV tracking
        csv_rows.append({
            "qid": ex.get("qid"),
            "model": model,
            "output": ex.get("generated_text"),
            "label": ex.get("label"),
            "occupation": category,
            "pareto_claims": ex.get("pareto_claims"),
            "kept": kept
        })

        if kept:
            ex["generated_text"] = cleaned_text
            clean_data.append(ex)

            stats[category][model]["kept"] += 1
            stats[category][model][group]["kept"] += 1
        else:
            stats[category][model][status] += 1
            stats[category][model][group][status] += 1

    pareto_1 = [ex for ex in clean_data if ex.get("pareto_claims") == 1]
    pareto_0 = [ex for ex in clean_data if ex.get("pareto_claims") == 0]

    entropy_1 = [extract_entropy_curve(ex) for ex in pareto_1]
    entropy_0 = [extract_entropy_curve(ex) for ex in pareto_0]

    global_entropy_head.extend(entropy_1)
    global_entropy_tail.extend(entropy_0)

    results.setdefault(category, {})
    results[category][model] = {
        "entropy_1": entropy_1,
        "entropy_0": entropy_0,
    }


with open(CSV_OUTPUT, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        "qid", "model", "label", "occupation", "output", "pareto_claims", "kept"
    ])
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"\nCSV saved to: {CSV_OUTPUT}")



for category, models in results.items():
    plt.figure(figsize=(10, 6))

    for model, data in models.items():
        color = get_color(model)

        mean_e1, std_e1 = mean_and_std(data["entropy_1"])
        mean_e0, std_e0 = mean_and_std(data["entropy_0"])

        if len(mean_e1) == 0 or len(mean_e0) == 0:
            continue

        x1 = range(len(mean_e1))
        x0 = range(len(mean_e0))

        name = model_mapping(model)

        plt.plot(x1, mean_e1, color=color, label=f"{name} - Head")
        plt.plot(x0, mean_e0, linestyle="--", color=color, label=f"{name} - Long-tail")

        plt.fill_between(x1, mean_e1 - std_e1, mean_e1 + std_e1, alpha=0.1, color=color)
        plt.fill_between(x0, mean_e0 - std_e0, mean_e0 + std_e0, alpha=0.1, color=color)

    plt.title(f"Entropy over time - {category}")
    plt.xlabel("Token position")
    plt.ylabel("Entropy")
    plt.legend()
    plt.grid(True)
    plt.show()


# =========================
# LENGTH vs ENTROPY (SCATTER) PER CATEGORIA
# =========================
for category, models in results.items():
    plt.figure(figsize=(10, 6))

    for model, d in models.items():
        color = get_color(model)
        name = model_mapping(model)

        # HEAD
        lengths_h = [len(c) for c in d["entropy_1"] if len(c) > 0]
        avg_entropy_h = [np.mean(c) for c in d["entropy_1"] if len(c) > 0]

        # TAIL
        lengths_t = [len(c) for c in d["entropy_0"] if len(c) > 0]
        avg_entropy_t = [np.mean(c) for c in d["entropy_0"] if len(c) > 0]

        plt.scatter(lengths_h, avg_entropy_h, color=color, alpha=0.6,
                    label=f"{name} - Head", marker="o")

        plt.scatter(lengths_t, avg_entropy_t, color=color, alpha=0.6,
                    label=f"{name} - Tail", marker="x")

    plt.title(f"Length vs Avg Entropy - {category}")
    plt.xlabel("Number of tokens")
    plt.ylabel("Average entropy")
    plt.legend()
    plt.grid(True)
    plt.show()


# =========================
# STATS PER CATEGORIA
# =========================
print("\n==== CATEGORY STATS ====")

for category, models in results.items():
    print(f"\n--- {category} ---")

    for model, d in models.items():
        avg_e1 = [np.mean(c) for c in d["entropy_1"] if len(c) > 0]
        avg_e0 = [np.mean(c) for c in d["entropy_0"] if len(c) > 0]

        print(f"\n{model}")
        print(f"  Avg entropy Head: {np.mean(avg_e1):.4f}")
        print(f"  Avg entropy Tail: {np.mean(avg_e0):.4f}")


# =========================
# GLOBAL STATS
# =========================
print("\n==== GLOBAL ENTROPY STATS ====")

avg_head = [np.mean(c) for c in global_entropy_head if len(c) > 0]
avg_tail = [np.mean(c) for c in global_entropy_tail if len(c) > 0]

print(f"\nHEAD Avg entropy: {np.mean(avg_head):.4f}")
print(f"TAIL Avg entropy: {np.mean(avg_tail):.4f}")


# =========================
# FILTERING STATS
# =========================
print("\n==== FILTERING STATS ====")

for category, models in stats.items():
    print(f"\n--- {category} ---")

    for model, s in models.items():
        print(f"\n{model}")
        print(f"  Total: {s['total']}")
        print(f"  Kept: {s['kept']}")
        print(f"  No pattern: {s['no_pattern']}")
def safe_ratio(a, b):
    return a / b if b > 0 else 0

print("\n==== FILTERING STATS (HEAD vs TAIL) ====")

for category, models in stats.items():
    print(f"\n--- {category} ---")

    for model, s in models.items():
        print(f"\n{model}")

        head_keep = safe_ratio(s['head']['kept'], s['head']['total']) * 100
        tail_keep = safe_ratio(s['tail']['kept'], s['tail']['total']) * 100

        print(f"  HEAD kept: {s['head']['kept']}/{s['head']['total']} ({head_keep:.1f}%)")
        print(f"  TAIL kept: {s['tail']['kept']}/{s['tail']['total']} ({tail_keep:.1f}%)")

        print(f"  HEAD dropped: {s['head']['filtered'] + s['head']['no_pattern']}")
        print(f"  TAIL dropped: {s['tail']['filtered'] + s['tail']['no_pattern']}")

print("\n==== GLOBAL LENGTH STATS ====")

len_h_mean, len_h_std = mean_length(global_entropy_head)
len_t_mean, len_t_std = mean_length(global_entropy_tail)

print("\nHEAD")
print(f"  Length: {len_h_mean:.2f} ± {len_h_std:.2f}")

print("\nTAIL")
print(f"  Length: {len_t_mean:.2f} ± {len_t_std:.2f}")

print("\n==== CATEGORY LENGTH STATS ====")

for category, models in results.items():
    print(f"\n--- {category} ---")

    for model, d in models.items():
        len_h_mean, len_h_std = mean_length(d["entropy_1"])
        len_t_mean, len_t_std = mean_length(d["entropy_0"])

        print(f"\n{model}")
        print(f"  Head length: {len_h_mean:.2f} ± {len_h_std:.2f}")
        print(f"  Tail length: {len_t_mean:.2f} ± {len_t_std:.2f}")
