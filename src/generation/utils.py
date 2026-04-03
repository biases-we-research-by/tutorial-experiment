import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def get_top_and_bottom_entities(df: pd.DataFrame, k: int = 2) -> pd.DataFrame:
    df_clean = df[
        df["label"].notna() &
        (df["label"].str.strip() != "")
    ].copy()

    df_sorted = df_clean.sort_values(by="total_claims", ascending=False)

    top_k = df_sorted.head(k)
    bottom_k = df_sorted.tail(k)

    combined = pd.concat([top_k, bottom_k]).drop_duplicates(subset="qid")

    return combined


def build_prompt(template: str, word: str) -> str:
    return template.format(word=word)