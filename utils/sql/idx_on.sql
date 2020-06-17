-- blocks
ALTER TABLE blocks ADD CONSTRAINT blocks_pkey PRIMARY KEY (b_id);
CREATE INDEX idx_blocks_b_time ON blocks (b_time);
VACUUM FULL blocks;
-- trasactions
ALTER TABLE transactions ADD CONSTRAINT transactions_pkey PRIMARY KEY (t_id);
ALTER TABLE transactions ADD CONSTRAINT transactions_hash_key UNIQUE (hash);
ALTER TABLE transactions ADD CONSTRAINT transactions_b_id_fkey FOREIGN KEY (b_id) REFERENCES blocks (b_id) MATCH SIMPLE;
CREATE INDEX idx_transactions_b_id ON transactions (b_id);
VACUUM FULL transactions;
-- addresses
ALTER TABLE addresses ADD CONSTRAINT addresses_pkey PRIMARY KEY (a_id);
ALTER TABLE addresses ADD CONSTRAINT addresses_a_list_key UNIQUE (a_list);
CREATE INDEX idx_addresses_n ON addresses (n);
VACUUM FULL addresses;
-- data
ALTER TABLE data ADD CONSTRAINT data_pkey PRIMARY KEY (t_out_id,t_out_n);
ALTER TABLE data ADD CONSTRAINT data_t_out_id_fkey FOREIGN KEY (t_out_id) REFERENCES transactions (t_id) MATCH SIMPLE;
ALTER TABLE data ADD CONSTRAINT data_t_in_id_fkey FOREIGN KEY (t_in_id) REFERENCES transactions (t_id) MATCH SIMPLE;
ALTER TABLE data ADD CONSTRAINT data_a_id_fkey FOREIGN KEY (a_id) REFERENCES addresses (a_id) MATCH SIMPLE;
CREATE INDEX idx_data_t_in_id ON data (t_in_id);
CREATE INDEX idx_data_a_id ON data (a_id);
CREATE INDEX idx_data_satoshi ON data (satoshi);
VACUUM FULL data;
