import pandas as pd

def load_row(path: str) -> pd.DataFrame:
    return pd.read_csv(path)