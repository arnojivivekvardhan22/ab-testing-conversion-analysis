CREATE TABLE IF NOT EXISTS experiment_sessions (
    session_id BIGINT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    session_date TIMESTAMP,
    experiment_group VARCHAR(20) NOT NULL,
    device_type VARCHAR(30),
    traffic_source VARCHAR(50),
    country VARCHAR(50),
    pages_viewed INTEGER,
    session_duration_seconds INTEGER,
    cart_items INTEGER,
    cart_abandoned INTEGER,
    converted INTEGER,
    order_value NUMERIC(12, 2),
    revenue_per_session NUMERIC(12, 2)
);