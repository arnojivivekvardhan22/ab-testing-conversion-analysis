import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()

SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

import pandas as pd

from hypothesis_testing import (
    conversion_rate_test,
    aov_test,
)

from bootstrap import (
    bootstrap_conversion_difference,
    bootstrap_aov_difference,
    create_plots,
)

from config import (
    CLEANED_FILE,
    BOOTSTRAP_ITERATIONS,
)


# ============================================================
# CELL 1 - LOAD CLEANED DATA
# ============================================================

df = pd.read_csv(
    CLEANED_FILE
)

print(
    df.head()
)

print(
    df.shape
)


# ============================================================
# CELL 2 - CREATE GROUPS
# ============================================================

control = df[
    df["experiment_group"] == "control"
]

variant = df[
    df["experiment_group"] == "variant"
]


# ============================================================
# CELL 3 - CONVERSION RATE
# ============================================================

control_conversion = (
    control["converted"].mean()
)

variant_conversion = (
    variant["converted"].mean()
)

print(
    "Control:",
    control_conversion
)

print(
    "Variant:",
    variant_conversion
)


# ============================================================
# CELL 4 - CONVERSION Z-TEST
# ============================================================

conversion_result = conversion_rate_test(
    df
)

print(
    conversion_result
)


# ============================================================
# CELL 5 - AOV
# ============================================================

control_aov = control.loc[
    control["converted"] == 1,
    "order_value",
].mean()

variant_aov = variant.loc[
    variant["converted"] == 1,
    "order_value",
].mean()

print(
    "Control AOV:",
    control_aov
)

print(
    "Variant AOV:",
    variant_aov
)


# ============================================================
# CELL 6 - WELCH'S T-TEST
# ============================================================

aov_result = aov_test(
    df
)

print(
    aov_result
)


# ============================================================
# CELL 7 - BOOTSTRAP CONVERSION
# ============================================================

(
    conversion_bootstrap,
    conversion_low,
    conversion_high,
) = bootstrap_conversion_difference(
    control,
    variant,
    iterations=BOOTSTRAP_ITERATIONS,
)

print(
    "Conversion Bootstrap CI:",
    conversion_low,
    conversion_high,
)


# ============================================================
# CELL 8 - BOOTSTRAP AOV
# ============================================================

(
    aov_bootstrap,
    aov_low,
    aov_high,
) = bootstrap_aov_difference(
    control,
    variant,
    iterations=BOOTSTRAP_ITERATIONS,
)

print(
    "AOV Bootstrap CI:",
    aov_low,
    aov_high,
)


# ============================================================
# CELL 9 - CREATE VISUALIZATIONS
# ============================================================

create_plots(
    conversion_bootstrap,
    aov_bootstrap,
)


# ============================================================
# CELL 10 - FINAL RESULT
# ============================================================

print("=" * 60)

print(
    "Control Conversion:",
    f"{conversion_result['control_conversion_rate']:.4%}",
)

print(
    "Variant Conversion:",
    f"{conversion_result['variant_conversion_rate']:.4%}",
)

print(
    "Relative Lift:",
    f"{conversion_result['relative_lift']:.4%}",
)

print(
    "P-value:",
    conversion_result["p_value"],
)

print(
    "Statistically Significant:",
    conversion_result[
        "statistically_significant"
    ],
)

print("=" * 60)