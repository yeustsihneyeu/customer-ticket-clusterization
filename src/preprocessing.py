import re
import pandas as pd

def substitute_template_vars(df):
    df = df.copy()
    df["Ticket Description"] = df.apply(
        lambda row: row["Ticket Description"].replace(
            "{product_purchased}", row["Product Purchased"]
        ),
        axis=1,
    )
    return df


def clean_description(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def drop_noise_columns(df):
    return df.drop(columns=["Resolution", "Customer Name", "Customer Email"])


def parse_dates(df):
    df = df.copy()
    df["Date of Purchase"] = pd.to_datetime(df["Date of Purchase"])
    df["First Response Time"] = pd.to_datetime(df["First Response Time"])
    df["Time to Resolution"] = pd.to_datetime(df["Time to Resolution"])

    # Negative values occur because Time to Resolution / First Response Time
    # are synthetic timestamps with no causal ordering (see EDA conclusions).
    df["response_time_hours"] = (
        df["Time to Resolution"] - df["First Response Time"]
    ).dt.total_seconds() / 3600

    return df