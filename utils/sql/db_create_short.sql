-- blocks
CREATE TABLE IF NOT EXISTS blocks (
	b_id INT NOT NULL PRIMARY KEY,
	b_time TIMESTAMP NOT NULL
);
CREATE INDEX idx_blocks_b_time ON blocks (b_time);
-- transactions
CREATE TABLE IF NOT EXISTS transactions (
	t_id INT NOT NULL PRIMARY KEY,
	hash CHAR(64) NOT NULL UNIQUE,
	b_id INT NOT NULL REFERENCES blocks(b_id)
);
CREATE INDEX idx_transactions_b_id ON transactions (b_id);
-- addresses
CREATE TABLE IF NOT EXISTS addresses (
	a_id BIGINT NOT NULL PRIMARY KEY,
	n INT NOT NULL,
	a_list JSONB NOT NULL UNIQUE
);
CREATE INDEX idx_addresses_n ON addresses (n);
-- data
CREATE TABLE IF NOT EXISTS data (
	t_out_id INT NOT NULL REFERENCES transactions(t_id),
	t_out_n INT NOT NULL,
	t_in_id INT REFERENCES transactions(t_id) DEFAULT NULL,
	a_id BIGINT REFERENCES addresses(a_id) DEFAULT NULL,
	satoshi BIGINT NOT NULL,
	PRIMARY KEY (t_out_id, t_out_n)
);
CREATE INDEX idx_data_t_in_id ON data (t_in_id);
CREATE INDEX idx_data_a_id ON data (a_id);
CREATE INDEX idx_data_satoshi ON data (satoshi);
