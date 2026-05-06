import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Wong (2011) colorblind-safe palette — 8 colors + 2 extras
COLORBLIND_PALETTE = [
    "#000000",  # black
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # pink
    "#882255",  # wine
    "#44AA99",  # teal
]

def plot_brier_score_gaussians(path: str,title:str) -> None:
    df = pd.read_csv(path)
    deciles = sorted(df["decile"].unique())

    x = np.linspace(df["brier_score"].min() - 0.005,
                    df["brier_score"].max() + 0.005, 500)

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, decile in enumerate(deciles):
        scores = df.loc[df["decile"] == decile, "brier_score"].values
        mu, sigma = scores.mean(), scores.std()
        color = COLORBLIND_PALETTE[i % len(COLORBLIND_PALETTE)]
        y = norm.pdf(x, mu, sigma)

        ax.plot(x, y, color=color, linewidth=2,
                label=f"Decile {decile}  (μ={mu:.4f})")
        ax.fill_between(x, y, alpha=0.12, color=color)

    ax.set_xlabel("Brier score", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="both", color="lightgray", linewidth=0.5)
    ax.legend(title="Decile", bbox_to_anchor=(1.01, 1), loc="upper left",
              frameon=False, fontsize=9)
    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.show()

plot_brier_score_gaussians("brier_scores_llama.csv", "Brier score-based distributions for Llama generated outputs")