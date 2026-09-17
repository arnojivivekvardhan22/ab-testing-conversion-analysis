-- ============================================================
-- A/B TESTING EXPERIMENT METRICS
-- ============================================================


-- ============================================================
-- 1. TOTAL SESSIONS BY GROUP
-- ============================================================

SELECT
    experiment_group,
    COUNT(*) AS sessions
FROM experiment_sessions
GROUP BY experiment_group
ORDER BY experiment_group;


-- ============================================================
-- 2. CONVERSIONS BY GROUP
-- ============================================================

SELECT
    experiment_group,
    COUNT(*) AS sessions,
    SUM(converted) AS conversions,
    ROUND(
        100.0 * SUM(converted) / COUNT(*),
        4
    ) AS conversion_rate_percent
FROM experiment_sessions
GROUP BY experiment_group
ORDER BY experiment_group;


-- ============================================================
-- 3. REVENUE BY GROUP
-- ============================================================

SELECT
    experiment_group,
    SUM(order_value) AS total_revenue,
    AVG(order_value) AS revenue_per_session
FROM experiment_sessions
GROUP BY experiment_group
ORDER BY experiment_group;


-- ============================================================
-- 4. AOV BY GROUP
-- ============================================================

SELECT
    experiment_group,
    COUNT(*) FILTER (
        WHERE converted = 1
    ) AS converted_orders,

    ROUND(
        AVG(order_value)
        FILTER (
            WHERE converted = 1
        ),
        2
    ) AS average_order_value

FROM experiment_sessions

GROUP BY experiment_group

ORDER BY experiment_group;


-- ============================================================
-- 5. DEVICE PERFORMANCE
-- ============================================================

SELECT
    experiment_group,
    device_type,
    COUNT(*) AS sessions,
    SUM(converted) AS conversions,

    ROUND(
        100.0 * SUM(converted) / COUNT(*),
        4
    ) AS conversion_rate_percent

FROM experiment_sessions

GROUP BY
    experiment_group,
    device_type

ORDER BY
    experiment_group,
    conversion_rate_percent DESC;


-- ============================================================
-- 6. TRAFFIC SOURCE PERFORMANCE
-- ============================================================

SELECT
    experiment_group,
    traffic_source,
    COUNT(*) AS sessions,
    SUM(converted) AS conversions,

    ROUND(
        100.0 * SUM(converted) / COUNT(*),
        4
    ) AS conversion_rate_percent

FROM experiment_sessions

GROUP BY
    experiment_group,
    traffic_source

ORDER BY
    experiment_group,
    conversion_rate_percent DESC;


-- ============================================================
-- 7. COUNTRY PERFORMANCE
-- ============================================================

SELECT
    experiment_group,
    country,
    COUNT(*) AS sessions,
    SUM(converted) AS conversions,

    ROUND(
        100.0 * SUM(converted) / COUNT(*),
        4
    ) AS conversion_rate_percent

FROM experiment_sessions

GROUP BY
    experiment_group,
    country

ORDER BY
    experiment_group,
    conversion_rate_percent DESC;


-- ============================================================
-- 8. DAILY CONVERSION TREND
-- ============================================================

SELECT
    DATE(session_date) AS experiment_date,
    experiment_group,
    COUNT(*) AS sessions,
    SUM(converted) AS conversions,

    ROUND(
        100.0 * SUM(converted) / COUNT(*),
        4
    ) AS conversion_rate_percent

FROM experiment_sessions

GROUP BY
    DATE(session_date),
    experiment_group

ORDER BY
    experiment_date,
    experiment_group;


-- ============================================================
-- 9. CART ABANDONMENT
-- ============================================================

SELECT
    experiment_group,

    COUNT(*) AS sessions,

    SUM(cart_abandoned) AS abandoned_sessions,

    ROUND(
        100.0 * SUM(cart_abandoned) / COUNT(*),
        4
    ) AS abandonment_rate_percent

FROM experiment_sessions

GROUP BY experiment_group

ORDER BY experiment_group;


-- ============================================================
-- 10. EXECUTIVE SUMMARY QUERY
-- ============================================================

WITH experiment_metrics AS (

    SELECT
        experiment_group,

        COUNT(*) AS sessions,

        SUM(converted) AS conversions,

        SUM(order_value) AS revenue,

        AVG(
            order_value
        ) FILTER (
            WHERE converted = 1
        ) AS aov

    FROM experiment_sessions

    GROUP BY experiment_group

)

SELECT
    experiment_group,
    sessions,
    conversions,

    ROUND(
        100.0 * conversions / sessions,
        4
    ) AS conversion_rate_percent,

    ROUND(
        revenue,
        2
    ) AS total_revenue,

    ROUND(
        aov,
        2
    ) AS average_order_value

FROM experiment_metrics

ORDER BY experiment_group;