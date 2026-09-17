import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from generate_data import generate_dataset
from data_cleaning import load_raw_data, clean_data
from srm_check import run_srm_test
from hypothesis_testing import (
    conversion_rate_test,
    aov_test,
)
from bootstrap import (
    bootstrap_conversion_difference,
    bootstrap_aov_difference,
    create_plots,
)

import pandas as pd

from config import (
    OUTPUT_DIR,
    EXPERIMENT_SUMMARY_FILE,
    HYPOTHESIS_RESULTS_FILE,
    BOOTSTRAP_RESULTS_FILE,
    BUSINESS_IMPACT_FILE,
    BOOTSTRAP_ITERATIONS,
    CONFIDENCE_LEVEL,
)


def create_experiment_summary(df):

    control = df[
        df["experiment_group"] == "control"
    ]

    variant = df[
        df["experiment_group"] == "variant"
    ]

    summary = []

    for name, group in [
        ("control", control),
        ("variant", variant),
    ]:

        sessions = len(group)
        conversions = group["converted"].sum()

        conversion_rate = (
            conversions / sessions
        )

        revenue = group["order_value"].sum()

        converted_orders = group[
            group["converted"] == 1
        ]

        aov = (
            converted_orders["order_value"].mean()
            if len(converted_orders) > 0
            else 0
        )

        summary.append(
            {
                "experiment_group": name,
                "sessions": sessions,
                "conversions": conversions,
                "conversion_rate": conversion_rate,
                "total_revenue": revenue,
                "aov": aov,
                "revenue_per_session": (
                    revenue / sessions
                ),
            }
        )

    result = pd.DataFrame(summary)

    result.to_csv(
        EXPERIMENT_SUMMARY_FILE,
        index=False,
    )

    return result


def calculate_business_impact(df):

    control = df[
        df["experiment_group"] == "control"
    ]

    variant = df[
        df["experiment_group"] == "variant"
    ]

    control_rate = (
        control["converted"].mean()
    )

    variant_rate = (
        variant["converted"].mean()
    )

    control_aov = control.loc[
        control["converted"] == 1,
        "order_value",
    ].mean()

    variant_aov = variant.loc[
        variant["converted"] == 1,
        "order_value",
    ].mean()

    traffic = len(df)

    incremental_conversions = (
        traffic
        * (variant_rate - control_rate)
    )

    estimated_incremental_revenue = (
        incremental_conversions
        * variant_aov
    )

    impact = pd.DataFrame(
        {
            "metric": [
                "Total Experiment Traffic",
                "Control Conversion Rate",
                "Variant Conversion Rate",
                "Absolute Conversion Lift",
                "Incremental Conversions",
                "Variant AOV",
                "Estimated Incremental Revenue",
            ],
            "value": [
                traffic,
                control_rate,
                variant_rate,
                variant_rate - control_rate,
                incremental_conversions,
                variant_aov,
                estimated_incremental_revenue,
            ],
        }
    )

    impact.to_csv(
        BUSINESS_IMPACT_FILE,
        index=False,
    )

    return impact


def main():

    print("\n")
    print("#" * 70)
    print("# A/B TESTING END-TO-END PIPELINE")
    print("#" * 70)

    # ========================================================
    # STEP 1 - GENERATE DATA
    # ========================================================

    print("\n[1/7] Generating dataset...")
    generate_dataset()

    # ========================================================
    # STEP 2 - CLEAN DATA
    # ========================================================

    print("\n[2/7] Cleaning dataset...")
    raw_df = load_raw_data()
    df = clean_data(raw_df)

    # ========================================================
    # STEP 3 - SRM
    # ========================================================

    print("\n[3/7] Running SRM test...")
    run_srm_test(df)

    # ========================================================
    # STEP 4 - SUMMARY
    # ========================================================

    print("\n[4/7] Creating experiment summary...")
    summary = create_experiment_summary(
        df
    )

    print(summary)

    # ========================================================
    # STEP 5 - HYPOTHESIS TESTING
    # ========================================================

    print("\n[5/7] Running hypothesis tests...")

    conversion_result = conversion_rate_test(
        df
    )

    aov_result = aov_test(
        df
    )

    hypothesis_results = pd.DataFrame(
        [
            conversion_result,
            aov_result,
        ]
    )

    hypothesis_results.to_csv(
        HYPOTHESIS_RESULTS_FILE,
        index=False,
    )

    # ========================================================
    # STEP 6 - BOOTSTRAP
    # ========================================================

    print("\n[6/7] Running bootstrap analysis...")

    control = df[
        df["experiment_group"] == "control"
    ]

    variant = df[
        df["experiment_group"] == "variant"
    ]

    (
        conversion_bootstrap,
        conversion_low,
        conversion_high,
    ) = bootstrap_conversion_difference(
        control,
        variant,
        iterations=BOOTSTRAP_ITERATIONS,
    )

    (
        aov_bootstrap,
        aov_low,
        aov_high,
    ) = bootstrap_aov_difference(
        control,
        variant,
        iterations=BOOTSTRAP_ITERATIONS,
    )

    bootstrap_results = pd.DataFrame(
        {
            "metric": [
                "Conversion Rate Difference",
                "AOV Difference",
            ],
            "bootstrap_iterations": [
                BOOTSTRAP_ITERATIONS,
                BOOTSTRAP_ITERATIONS,
            ],
            "confidence_level": [
                CONFIDENCE_LEVEL,
                CONFIDENCE_LEVEL,
            ],
            "ci_low": [
                conversion_low,
                aov_low,
            ],
            "ci_high": [
                conversion_high,
                aov_high,
            ],
        }
    )

    bootstrap_results.to_csv(
        BOOTSTRAP_RESULTS_FILE,
        index=False,
    )

    create_plots(
        conversion_bootstrap,
        aov_bootstrap,
    )

    # ========================================================
    # STEP 7 - BUSINESS IMPACT
    # ========================================================

    print("\n[7/7] Calculating business impact...")

    impact = calculate_business_impact(
        df
    )

    print("\n")
    print("#" * 70)
    print("# PIPELINE COMPLETE")
    print("#" * 70)

    print("\nExperiment Summary:")
    print(summary)

    print("\nHypothesis Results:")
    print(hypothesis_results)

    print("\nBootstrap Results:")
    print(bootstrap_results)

    print("\nBusiness Impact:")
    print(impact)

    print("\nAll outputs saved to:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()