import pandas as pd
from scipy.stats import chisquare

from config import (
    CLEANED_FILE,
    SRM_RESULTS_FILE,
    ALPHA,
    CONTROL_RATIO,
    VARIANT_RATIO,
)


def run_srm_test(df):
    observed_control = (
        df["experiment_group"]
        .eq("control")
        .sum()
    )

    observed_variant = (
        df["experiment_group"]
        .eq("variant")
        .sum()
    )

    total = observed_control + observed_variant

    expected_control = total * CONTROL_RATIO
    expected_variant = total * VARIANT_RATIO

    observed = [
        observed_control,
        observed_variant,
    ]

    expected = [
        expected_control,
        expected_variant,
    ]

    chi_square_stat, p_value = chisquare(
        f_obs=observed,
        f_exp=expected,
    )

    actual_control_ratio = (
        observed_control / total
    )

    actual_variant_ratio = (
        observed_variant / total
    )

    result = pd.DataFrame(
        {
            "metric": [
                "Observed Control",
                "Observed Variant",
                "Expected Control",
                "Expected Variant",
                "Control Ratio",
                "Variant Ratio",
                "Chi-Square Statistic",
                "P-Value",
                "Alpha",
                "SRM Status",
            ],
            "value": [
                observed_control,
                observed_variant,
                expected_control,
                expected_variant,
                actual_control_ratio,
                actual_variant_ratio,
                chi_square_stat,
                p_value,
                ALPHA,
                (
                    "PASS"
                    if p_value >= ALPHA
                    else "FAIL"
                ),
            ],
        }
    )

    result.to_csv(
        SRM_RESULTS_FILE,
        index=False,
    )

    print("\n" + "=" * 60)
    print("SAMPLE RATIO MISMATCH TEST")
    print("=" * 60)

    print(f"Control observed: {observed_control:,}")
    print(f"Variant observed: {observed_variant:,}")

    print(
        f"Control ratio: "
        f"{actual_control_ratio:.4%}"
    )

    print(
        f"Variant ratio: "
        f"{actual_variant_ratio:.4%}"
    )

    print(
        f"Chi-square statistic: "
        f"{chi_square_stat:.6f}"
    )

    print(
        f"P-value: "
        f"{p_value:.6f}"
    )

    if p_value >= ALPHA:
        print("SRM RESULT: PASS")
    else:
        print("SRM RESULT: FAIL")

    print("=" * 60)

    return result


def main():
    df = pd.read_csv(CLEANED_FILE)
    run_srm_test(df)


if __name__ == "__main__":
    main()