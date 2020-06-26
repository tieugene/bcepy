-- blocks
ALTER TABLE blocks ADD CONSTRAINT blocks_pkey PRIMARY KEY (b_id);
CREATE INDEX idx_blocks_b_time ON blocks (b_time);
VACUUM FULL blocks;
