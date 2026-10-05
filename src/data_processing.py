import pandas as pd


def load_tourism_data(file_path):
    """
    Load and prepare tourism trace data.
    """

    df = pd.read_csv(file_path)

    # Convert travel date to datetime
    df["travel_date"] = pd.to_datetime(df["travel_date"])

    # Remove duplicate visitor records
    df = df.drop_duplicates()

    # Standardize text columns
    text_columns = [
        "origin",
        "destination",
        "visitor_type",
        "activity_type",
        "season"
    ]

    for column in text_columns:
        df[column] = df[column].astype(str).str.strip()

    return df
