from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"

RAW_FILE = RAW_DATA_DIR / "raw_sessions.csv"
CLEANED_FILE = PROCESSED_DATA_DIR / "cleaned_experiment_data.csv"

EXPERIMENT_SUMMARY_FILE = OUTPUT_DIR / "experiment_summary.csv"
SRM_RESULTS_FILE = OUTPUT_DIR / "srm_results.csv"
HYPOTHESIS_RESULTS_FILE = OUTPUT_DIR / "hypothesis_results.csv"
BOOTSTRAP_RESULTS_FILE = OUTPUT_DIR / "bootstrap_results.csv"
BUSINESS_IMPACT_FILE = OUTPUT_DIR / "business_impact.csv"


# ============================================================
# EXPERIMENT SETTINGS
# ============================================================

RANDOM_SEED = 42

TOTAL_SESSIONS = 150_000

CONTROL_RATIO = 0.50
VARIANT_RATIO = 0.50

ALPHA = 0.05

BETA = 0.20
POWER = 1 - BETA

# MDE is specified as a relative effect.
MDE_RELATIVE = 0.02

BOOTSTRAP_ITERATIONS = 10_000
CONFIDENCE_LEVEL = 0.95


# ============================================================
# DATA GENERATION SETTINGS
# ============================================================

CONTROL_CONVERSION_RATE = 0.0420
VARIANT_CONVERSION_RATE = 0.0434

CONTROL_AOV_MEAN = 105.0
VARIANT_AOV_MEAN = 107.0

AOV_SIGMA = 0.85


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

for directory in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OUTPUT_DIR,
    FIGURES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)