import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from config import (
    CLEANED_FILE,
    BOOTSTRAP_RESULTS_FILE,
    FIGURES_DIR,
    BOOTSTRAP_ITERATIONS,
    CONFIDENCE_LEVEL,
    RANDOM_SEED,
)


def bootstrap_conversion_difference(
    control,
    variant,
    iterations=BOOTSTRAP_ITERATIONS,
):

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    control_values = control[
        "converted"
    ].to_numpy()

    variant_values = variant[
        "converted"
    ].to_numpy()

    differences = np.empty(
        iterations
    )

    for i in range(iterations):

        control_sample = rng.choice(
            control_values,
            size=len(control_values),
            replace=True,
        )

        variant_sample = rng.choice(
            variant_values,
            size=len(variant_values),
            replace=True,
        )

        control_rate = (
            control_sample.mean()
        )

        variant_rate = (
            variant_sample.mean()
        )

        differences[i] = (
            variant_rate - control_rate
        )

    alpha = 1 - CONFIDENCE_LEVEL

    lower = np.quantile(
        differences,
        alpha / 2,
    )

    upper = np.quantile(
        differences,
        1 - alpha / 2,
    )

    return differences, lower, upper


def bootstrap_aov_difference(
    control,
    variant,
    iterations=BOOTSTRAP_ITERATIONS,
):

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    control_values = control[
        control["converted"] == 1
    ]["order_value"].to_numpy()

    variant_values = variant[
        variant["converted"] == 1
    ]["order_value"].to_numpy()

    differences = np.empty(
        iterations
    )

    for i in range(iterations):

        control_sample = rng.choice(
            control_values,
            size=len(control_values),
            replace=True,
        )

        variant_sample = rng.choice(
            variant_values,
            size=len(variant_values),
            replace=True,
        )

        differences[i] = (
            variant_sample.mean()
            - control_sample.mean()
        )

    alpha = 1 - CONFIDENCE_LEVEL

    lower = np.quantile(
        differences,
        alpha / 2,
    )

    upper = np.quantile(
        differences,
        1 - alpha / 2,
    )

    return differences, lower, upper


def create_plots(
    conversion_bootstrap,
    aov_bootstrap,
):

    sns.set_theme(
        style="whitegrid"
    )

    plt.figure(
        figsize=(10, 6)
    )

    sns.histplot(
        conversion_bootstrap,
        bins=60,
        kde=True,
    )

    plt.axvline(
        0,
        linestyle="--",
        linewidth=2,
    )

    plt.title(
        "Bootstrap Distribution - Conversion Rate Difference"
    )

    plt.xlabel(
        "Variant Conversion Rate - Control Conversion Rate"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR
        / "bootstrap_conversion_distribution.png",
        dpi=150,
    )

    plt.close()

    plt.figure(
        figsize=(10, 6)
    )

    sns.histplot(
        aov_bootstrap,
        bins=60,
        kde=True,
    )

    plt.axvline(
        0,
        linestyle="--",
        linewidth=2,
    )

    plt.title(
        "Bootstrap Distribution - AOV Difference"
    )

    plt.xlabel(
        "Variant AOV - Control AOV"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR
        / "bootstrap_aov_distribution.png",
        dpi=150,
    )

    plt.close()


def main():

    df = pd.read_csv(
        CLEANED_FILE
    )

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
    )

    (
        aov_bootstrap,
        aov_low,
        aov_high,
    ) = bootstrap_aov_difference(
        control,
        variant,
    )

    result = pd.DataFrame(
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
            "ci_excludes_zero": [
                not (
                    conversion_low <= 0
                    <= conversion_high
                ),
                not (
                    aov_low <= 0
                    <= aov_high
                ),
            ],
        }
    )

    result.to_csv(
        BOOTSTRAP_RESULTS_FILE,
        index=False,
    )

    create_plots(
        conversion_bootstrap,
        aov_bootstrap,
    )

    print("\n" + "=" * 60)
    print("BOOTSTRAP ANALYSIS")
    print("=" * 60)

    print(
        "Conversion rate difference 95% CI:"
    )

    print(
        f"[{conversion_low:.6%}, "
        f"{conversion_high:.6%}]"
    )

    print(
        "\nAOV difference 95% CI:"
    )

    print(
        f"[${aov_low:.2f}, "
        f"${aov_high:.2f}]"
    )

    print(
        f"\nBootstrap iterations: "
        f"{BOOTSTRAP_ITERATIONS:,}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()