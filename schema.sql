DROP TABLE IF EXISTS site_readings CASCADE;

CREATE TABLE site_readings (
    id SERIAL PRIMARY KEY,
    site_code VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    source_tag VARCHAR(100) NOT NULL,
    solar_output_current FLOAT NOT NULL,
    total_load_current FLOAT NOT NULL,
    battery_total_current FLOAT NOT NULL,
    total_voltage FLOAT NOT NULL,
    CONSTRAINT unique_site_timestamp UNIQUE (site_code, timestamp)
);

CREATE INDEX idx_site_timestamp ON site_readings(site_code, timestamp);
CREATE INDEX idx_source_tag ON site_readings(source_tag);