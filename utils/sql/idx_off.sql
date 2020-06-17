-- data
ALTER TABLE data DROP CONSTRAINT IF EXISTS data_pkey;
ALTER TABLE data DROP CONSTRAINT IF EXISTS data_t_out_id_fkey;
ALTER TABLE data DROP CONSTRAINT IF EXISTS data_t_in_id_fkey;
ALTER TABLE data DROP CONSTRAINT IF EXISTS data_a_id_fkey;
DROP INDEX IF EXISTS idx_data_t_in_id;
DROP INDEX IF EXISTS idx_data_a_id;
DROP INDEX IF EXISTS idx_data_satoshi;
-- addresses
ALTER TABLE addresses DROP CONSTRAINT IF EXISTS addresses_pkey;
ALTER TABLE addresses DROP CONSTRAINT IF EXISTS addresses_a_list_key;
DROP INDEX IF EXISTS idx_addresses_n;
-- transactions
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS transactions_pkey;
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS transactions_hash_key;
ALTER TABLE transactions DROP CONSTRAINT IF EXISTS transactions_b_id_fkey;
DROP INDEX IF EXISTS idx_transactions_b_id;
-- blocks
ALTER TABLE blocks DROP CONSTRAINT IF EXISTS blocks_pkey;
DROP INDEX IF EXISTS idx_blocks_b_time;
