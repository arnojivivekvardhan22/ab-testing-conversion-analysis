import numpy as np
import pandas as pd

from scipy.stats import (
    ttest_ind,
)

from statsmodels.stats.proportion import (
    proportions_ztest,
    confint_proportions_2indep,
)

from config import (
    CLEANED_FILE,
    HYPOTHESIS_RESULTS_FILE,
    ALPHA,
)


def conversion_rate_test(df):

    control = df[
        df["experiment_group"] == "control"
    ]

    variant = df[
        df["experiment_group"] == "variant"
    ]

    control_n = len(control)
    variant_n = len(variant)

    control_conversions = (
        control["converted"].sum()
    )

    variant_conversions = (
        variant["converted"].sum()
    )

    control_rate = (
        control_conversions / control_n
    )

    variant_rate = (
        variant_conversions / variant_n
    )

    absolute_lift = (
        variant_rate - control_rate
    )

    relative_lift = (
        absolute_lift / control_rate
    )

    count = np.array(
        [
            variant_conversions,
            control_conversions,
        ]
    )

    nobs = np.array(
        [
            variant_n,
            control_n,
        ]
    )

    z_stat, p_value = proportions_ztest(
        count=count,
        nobs=nobs,
        alternative="two-sided",
    )

    ci_low, ci_high = confint_proportions_2indep(
        count1=variant_conversions,
        nobs1=variant_n,
        count2=control_conversions,
        nobs2=control_n,
        compare="diff",
        method="wald",
    )

    result = {
        "test": "Two-Sample Two-Tailed Z-Test for Proportions",
        "control_n": control_n,
        "variant_n": variant_n,
        "control_conversions": control_conversions,
        "variant_conversions": variant_conversions,
        "control_conversion_rate": control_rate,
        "variant_conversion_rate": variant_rate,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "alpha": ALPHA,
        "statistically_significant": p_value < ALPHA,
    }

    return result


def aov_test(df):

    control_aov = df.loc[
        (
            (df["experiment_group"] == "control")
            & (df["converted"] == 1)
        ),
        "order_value",
    ]

    variant_aov = df.loc[
        (
            (df["experiment_group"] == "variant")
            & (df["converted"] == 1)
        ),
        "order_value",
    ]

    control_mean = control_aov.mean()
    variant_mean = variant_aov.mean()

    absolute_difference = (
        variant_mean - control_mean
    )

    relative_difference = (
        absolute_difference / control_mean
    )

    t_stat, p_value = ttest_ind(
        variant_aov,
        control_aov,
        equal_var=False,
        alternative="two-sided",
    )

    result = {
        "test": "Welch's Two-Sample T-Test for AOV",
        "control_n_converted": len(control_aov),
        "variant_n_converted": len(variant_aov),
        "control_aov": control_mean,
        "variant_aov": variant_mean,
        "aov_absolute_difference": absolute_difference,
        "aov_relative_difference": relative_difference,
        "t_statistic": t_stat,
        "p_value": p_value,
        "alpha": ALPHA,
        "statistically_significant": p_value < ALPHA,
    }

    return result


def main():

    df = pd.read_csv(
        CLEANED_FILE
    )

    conversion_result = conversion_rate_test(
        df
    )

    aov_result = aov_test(
        df
    )

    results = pd.DataFrame(
        [
            conversion_result,
            aov_result,
        ]
    )

    results.to_csv(
        HYPOTHESIS_RESULTS_FILE,
        index=False,
    )

    print("\n" + "=" * 60)
    print("HYPOTHESIS TESTING")
    print("=" * 60)

    print("\nCONVERSION RATE")
    print("-" * 60)

    print(
        f"Control conversion: "
        f"{conversion_result['control_conversion_rate']:.4%}"
    )

    print(
        f"Variant conversion: "
        f"{conversion_result['variant_conversion_rate']:.4%}"
    )

    print(
        f"Absolute lift: "
        f"{conversion_result['absolute_lift']:.4%}"
    )

    print(
        f"Relative lift: "
        f"{conversion_result['relative_lift']:.4%}"
    )

    print(
        f"Z-statistic: "
        f"{conversion_result['z_statistic']:.6f}"
    )

    print(
        f"P-value: "
        f"{conversion_result['p_value']:.10f}"
    )

    print(
        f"95% CI: "
        f"[{conversion_result['ci_low']:.6%}, "
        f"{conversion_result['ci_high']:.6%}]"
    )

    print(
        "Significant:",
        conversion_result[
            "statistically_significant"
        ],
    )

    print("\nAOV")
    print("-" * 60)

    print(
        f"Control AOV: "
        f"${aov_result['control_aov']:.2f}"
    )

    print(
        f"Variant AOV: "
        f"${aov_result['variant_aov']:.2f}"
    )

    print(
        f"AOV difference: "
        f"${aov_result['aov_absolute_difference']:.2f}"
    )

    print(
        f"AOV relative difference: "
        f"{aov_result['aov_relative_difference']:.4%}"
    )

    print(
        f"T-statistic: "
        f"{aov_result['t_statistic']:.6f}"
    )

    print(
        f"P-value: "
        f"{aov_result['p_value']:.10f}"
    )

    print(
        "Significant:",
        aov_result[
            "statistically_significant"
        ],
    )

    print("=" * 60)


if __name__ == "__main__":
    main()