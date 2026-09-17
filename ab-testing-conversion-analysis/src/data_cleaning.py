import pandas as pd
import numpy as np

from config import RAW_FILE, CLEANED_FILE


REQUIRED_COLUMNS = [
    "session_id",
    "user_id",
    "session_date",
    "experiment_group",
    "device_type",
    "traffic_source",
    "country",
    "pages_viewed",
    "session_duration_seconds",
    "cart_items",
    "cart_abandoned",
    "converted",
    "order_value",
]


def load_raw_data():
    return pd.read_csv(RAW_FILE)


def clean_data(df):
    df = df.copy()

    print("\nInitial shape:")
    print(df.shape)

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------------
    # Remove duplicate session IDs
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates(
        subset=["session_id"],
        keep="first",
    )

    after_duplicates = len(df)

    print(
        f"Duplicates removed: "
        f"{before_duplicates - after_duplicates:,}"
    )

    # --------------------------------------------------------
    # Convert date column
    # --------------------------------------------------------

    df["session_date"] = pd.to_datetime(
        df["session_date"],
        errors="coerce",
    )

    # --------------------------------------------------------
    # Numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "pages_viewed",
        "session_duration_seconds",
        "cart_items",
        "cart_abandoned",
        "converted",
        "order_value",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # --------------------------------------------------------
    # Handle missing categorical values
    # --------------------------------------------------------

    categorical_columns = [
        "experiment_group",
        "device_type",
        "traffic_source",
        "country",
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna("unknown")

    # --------------------------------------------------------
    # Handle numeric missing values
    # --------------------------------------------------------

    for column in numeric_columns:
        df[column] = df[column].fillna(
            df[column].median()
        )

    # --------------------------------------------------------
    # Ensure binary fields are valid
    # --------------------------------------------------------

    df["converted"] = (
        df["converted"]
        .clip(0, 1)
        .round()
        .astype(int)
    )

    df["cart_abandoned"] = (
        df["cart_abandoned"]
        .clip(0, 1)
        .round()
        .astype(int)
    )

    # --------------------------------------------------------
    # Business-rule corrections
    # --------------------------------------------------------

    # Non-converted sessions should have zero order value.
    df.loc[
        df["converted"] == 0,
        "order_value"
    ] = 0

    # Converted sessions cannot have negative order value.
    df["order_value"] = df["order_value"].clip(
        lower=0
    )

    # --------------------------------------------------------
    # Create useful derived columns
    # --------------------------------------------------------

    df["revenue_per_session"] = df["order_value"]

    df["experiment_group"] = (
        df["experiment_group"]
        .str.lower()
        .str.strip()
    )

    # --------------------------------------------------------
    # Validate groups
    # --------------------------------------------------------

    valid_groups = ["control", "variant"]

    df = df[
        df["experiment_group"].isin(valid_groups)
    ].copy()

    # --------------------------------------------------------
    # Final sorting
    # --------------------------------------------------------

    df = df.sort_values(
        by="session_id"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Save cleaned dataset
    # --------------------------------------------------------

    df.to_csv(
        CLEANED_FILE,
        index=False,
    )

    print("\nFinal shape:")
    print(df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nGroup counts:")
    print(df["experiment_group"].value_counts())

    print("\nCleaned dataset saved:")
    print(CLEANED_FILE)

    return df


def main():
    df = load_raw_data()
    clean_data(df)


if __name__ == "__main__":
    main()