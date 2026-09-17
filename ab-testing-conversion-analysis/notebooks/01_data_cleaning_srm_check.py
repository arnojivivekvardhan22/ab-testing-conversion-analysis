import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()

SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from generate_data import generate_dataset
from data_cleaning import (
    load_raw_data,
    clean_data,
)
from srm_check import run_srm_test


# ============================================================
# CELL 1 - GENERATE DATA
# ============================================================

generate_dataset()


# ============================================================
# CELL 2 - LOAD RAW DATA
# ============================================================

raw_df = load_raw_data()

print(raw_df.head())
print(raw_df.shape)


# ============================================================
# CELL 3 - DATA INFORMATION
# ============================================================

print(raw_df.info())


# ============================================================
# CELL 4 - MISSING VALUES
# ============================================================

print(
    raw_df.isnull().sum()
)


# ============================================================
# CELL 5 - DUPLICATES
# ============================================================

print(
    "Duplicate sessions:",
    raw_df["session_id"].duplicated().sum(),
)


# ============================================================
# CELL 6 - CLEAN DATA
# ============================================================

cleaned_df = clean_data(
    raw_df
)


# ============================================================
# CELL 7 - CLEAN DATA CHECK
# ============================================================

print(cleaned_df.head())

print(
    cleaned_df.shape
)

print(
    cleaned_df.isnull().sum()
)


# ============================================================
# CELL 8 - GROUP DISTRIBUTION
# ============================================================

print(
    cleaned_df[
        "experiment_group"
    ].value_counts()
)


# ============================================================
# CELL 9 - SRM TEST
# ============================================================

srm_result = run_srm_test(
    cleaned_df
)

print(srm_result)