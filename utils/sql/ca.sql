-- addresses
CREATE TABLE IF NOT EXISTS addresses (
	a_id BIGINT NOT NULL PRIMARY KEY,
	n INT NOT NULL,
	a_list JSONB NOT NULL UNIQUE
);
CREATE INDEX idx_addresses_n ON addresses (n);
