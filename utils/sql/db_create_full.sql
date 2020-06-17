-- blocks
CREATE TABLE IF NOT EXISTS blocks (
	b_id BIGINT NOT NULL,
	b_time TIMESTAMP NOT NULL,
	CONSTRAINT blocks_pkey PRIMARY KEY (b_id)
);
CREATE INDEX idx_blocks_b_time ON blocks (b_time);
-- transactions
CREATE TABLE IF NOT EXISTS transactions (
	t_id BIGINT NOT NULL,
	hash CHAR(64) NOT NULL,
	b_id BIGINT NOT NULL,
	CONSTRAINT transactions_pkey PRIMARY KEY (t_id),
	CONSTRAINT transactions_hash_key UNIQUE (hash),
	CONSTRAINT transactions_b_id_fkey FOREIGN KEY (b_id)
	    REFERENCES blocks (b_id) MATCH SIMPLE
);
CREATE INDEX idx_transactions_b_id ON transactions (b_id);
-- addresses
CREATE TABLE IF NOT EXISTS addresses (
	a_id BIGINT NOT NULL,
	n INT NOT NULL,
	a_list JSONB NOT NULL,
	CONSTRAINT addresses_pkey PRIMARY KEY (a_id),
	CONSTRAINT addresses_a_list_key UNIQUE (a_list)
);
CREATE INDEX idx_addresses_n ON addresses (n);
-- data
CREATE TABLE IF NOT EXISTS data (
	t_out_id INT NOT NULL,
	t_out_n INT NOT NULL,
	t_in_id INT DEFAULT NULL,
	a_id BIGINT DEFAULT NULL,
	satoshi BIGINT NOT NULL,
	CONSTRAINT data_pkey PRIMARY KEY (t_out_id, t_out_n),
	CONSTRAINT data_t_out_id_fkey FOREIGN KEY (t_out_id)
	    REFERENCES transactions (t_id) MATCH SIMPLE,
	CONSTRAINT data_t_in_id_fkey FOREIGN KEY (t_in_id)
	    REFERENCES transactions (t_id) MATCH SIMPLE,
	CONSTRAINT data_a_id_fkey FOREIGN KEY (a_id)
	    REFERENCES addresses (a_id) MATCH SIMPLE
);
CREATE INDEX idx_data_t_in_id ON data (t_in_id);
CREATE INDEX idx_data_a_id ON data (a_id);
CREATE INDEX idx_data_satoshi ON data (satoshi);
