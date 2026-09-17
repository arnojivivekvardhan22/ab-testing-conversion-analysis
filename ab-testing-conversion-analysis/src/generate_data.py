import numpy as np
import pandas as pd

from config import (
    RAW_FILE,
    RANDOM_SEED,
    TOTAL_SESSIONS,
    CONTROL_CONVERSION_RATE,
    VARIANT_CONVERSION_RATE,
    CONTROL_AOV_MEAN,
    VARIANT_AOV_MEAN,
    AOV_SIGMA,
)


def generate_dataset():
    rng = np.random.default_rng(RANDOM_SEED)

    n_control = TOTAL_SESSIONS // 2
    n_variant = TOTAL_SESSIONS - n_control

    session_ids = np.arange(1, TOTAL_SESSIONS + 1)

    user_ids = [
        f"U{number:07d}"
        for number in range(1, TOTAL_SESSIONS + 1)
    ]

    dates = pd.date_range(
        start="2026-01-01",
        end="2026-03-31",
        periods=TOTAL_SESSIONS,
    )

    control_group = np.array(
        ["control"] * n_control
        + ["variant"] * n_variant
    )

    rng.shuffle(control_group)

    device_types = rng.choice(
        ["mobile", "desktop", "tablet"],
        size=TOTAL_SESSIONS,
        p=[0.58, 0.35, 0.07],
    )

    traffic_sources = rng.choice(
        ["organic", "paid_search", "social", "email", "direct"],
        size=TOTAL_SESSIONS,
        p=[0.32, 0.24, 0.15, 0.11, 0.18],
    )

    countries = rng.choice(
        ["India", "USA", "UK", "Canada", "Australia"],
        size=TOTAL_SESSIONS,
        p=[0.52, 0.20, 0.10, 0.08, 0.10],
    )

    pages_viewed = rng.poisson(
        lam=5,
        size=TOTAL_SESSIONS,
    ) + 1

    session_duration_seconds = np.maximum(
        rng.normal(
            loc=240,
            scale=100,
            size=TOTAL_SESSIONS,
        ),
        10,
    ).round(0).astype(int)

    cart_items = rng.poisson(
        lam=2.2,
        size=TOTAL_SESSIONS,
    )

    cart_items = np.maximum(cart_items, 0)

    conversion_probability = np.where(
        control_group == "control",
        CONTROL_CONVERSION_RATE,
        VARIANT_CONVERSION_RATE,
    )

    converted = rng.binomial(
        n=1,
        p=conversion_probability,
        size=TOTAL_SESSIONS,
    )

    order_value = np.zeros(TOTAL_SESSIONS)

    control_mask = (
        (control_group == "control")
        & (converted == 1)
    )

    variant_mask = (
        (control_group == "variant")
        & (converted == 1)
    )

    control_converted_count = control_mask.sum()
    variant_converted_count = variant_mask.sum()

    control_values = rng.lognormal(
        mean=np.log(CONTROL_AOV_MEAN) - (AOV_SIGMA ** 2) / 2,
        sigma=AOV_SIGMA,
        size=control_converted_count,
    )

    variant_values = rng.lognormal(
        mean=np.log(VARIANT_AOV_MEAN) - (AOV_SIGMA ** 2) / 2,
        sigma=AOV_SIGMA,
        size=variant_converted_count,
    )

    order_value[control_mask] = control_values.round(2)
    order_value[variant_mask] = variant_values.round(2)

    cart_abandoned = (
        (cart_items > 0)
        & (converted == 0)
    ).astype(int)

    data = pd.DataFrame(
        {
            "session_id": session_ids,
            "user_id": user_ids,
            "session_date": dates,
            "experiment_group": control_group,
            "device_type": device_types,
            "traffic_source": traffic_sources,
            "country": countries,
            "pages_viewed": pages_viewed,
            "session_duration_seconds": session_duration_seconds,
            "cart_items": cart_items,
            "cart_abandoned": cart_abandoned,
            "converted": converted,
            "order_value": order_value,
        }
    )

    # Introduce a tiny number of data-quality issues
    # so the cleaning pipeline has something realistic to handle.
    duplicate_rows = data.sample(
        n=50,
        random_state=RANDOM_SEED,
    )

    data = pd.concat(
        [data, duplicate_rows],
        ignore_index=True,
    )

    missing_indices = data.sample(
        n=25,
        random_state=RANDOM_SEED + 1,
    ).index

    data.loc[
        missing_indices,
        "traffic_source"
    ] = np.nan

    data.to_csv(
        RAW_FILE,
        index=False,
    )

    print("=" * 60)
    print("DATA GENERATION COMPLETE")
    print("=" * 60)
    print(f"Raw dataset: {RAW_FILE}")
    print(f"Rows generated: {len(data):,}")
    print(f"Control rows: {(data['experiment_group'] == 'control').sum():,}")
    print(f"Variant rows: {(data['experiment_group'] == 'variant').sum():,}")
    print("=" * 60)


if __name__ == "__main__":
    generate_dataset()