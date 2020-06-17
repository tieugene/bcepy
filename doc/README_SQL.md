# Using PostgrSQL

F30: pgsql 11.7

## 1. Prepare PostgreSQL
postgres:pgpassword

* [RTFM #1](https://linux-notes.org/ustanovka-postgresql-centos-red-hat-fedora/)
* [RTFM #2](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04-ru)
* [RTFM #3](http://r00ssyp.blogspot.com/2017/03/postgresql-9.html)

### 1.1. install postgres

```
sudo dnf install postgresql-server [pgadmin3]
sudo mkdir -m0700 /mnt/shares/pgsql
sudo chown postgres:postgres /mnt/shares/pgsql
sudo mv /var/lib/pgsql/{data,backups} /mnt/shares/pgsql/
sudo ln -s /mnt/shares/pgsql/data /var/lib/pgsql/data
sudo ln -s /mnt/shares/pgsql/backups /var/lib/pgsql/backups
sudo postgresql-setup --initdb
```

### 1.2. tuning
/var/lib/data/pg_hba.conf (B4 all):

```
-local   all             all                                     peer
+local   all             all                                     trust
-host    all             all             127.0.0.1/32            ident
+host    all             all             127.0.0.1/32            md5
-host    all             all             ::1/128                 ident
```

### 1.3. go

```
sudo systemctl start postgresql
sudo -i -u postgres psql -c "\password [postgres]"
...
# check
psql -U postgres [-W]
SELECT * FROM pg_user;
SELECT * FROM pg_database;
```

## 2. Create DB

btcuser:btcpassword@btcdb

### 2.1. db

```
psql -U postgres
CREATE USER btcuser;
ALTER USER btcuser WITH ENCRYPTED PASSWORD 'btcpassword';
CREATE DATABASE btcdb;
GRANT ALL PRIVILEGES ON DATABASE btcdb TO btcuser;
ALTER DATABASE btcdb OWNER TO btcuser;
\q
```
check:
```
psql btcdb btcuser
\q
```

or (not tested)

```
sudo createuser -U postgres -w btcuser
sudo -u postgres createdb -O "btcuser" btcdb
```

### 2.2. data

```
psql -f db_create.sql btcdb btcuser
```

### 2.x. service

~/.pgpass:

```
localhost:5433:*:btcuser:btcpassword
```

## 3. Insert data

### 3.1. simply

by file:

```
(echo "BEGIN;"; bzcat _sql/000.sql.bz2; echo "COMMIT;") | psql -q btcdb btcuser
```

or bulk:

```
START=0
END=99
for i in `seq $START $END`
do
    fn=`printf "%03d" $i`
    echo $fn
    (echo "BEGIN;"; bzcat _sql/$fn.sql.bz2; echo "COMMIT;") | psql -q btcdb btcuser
done
```

### 3.2. bulk

#### switch indeces off

psql -d idx_off.sql btcdb btcuser:

```
ALTER TABLE transactions DROP CONSTRAINT transactions_b_id_fkey;
ALTER TABLE data DROP CONSTRAINT data_a_id_fkey;
ALTER TABLE data DROP CONSTRAINT data_t_in_id_fkey;
ALTER TABLE data DROP CONSTRAINT data_t_out_id_fkey;
ALTER TABLE blocks DROP CONSTRAINT blocks_pkey;
ALTER TABLE transactions DROP CONSTRAINT transactions_pkey;
ALTER TABLE addresses DROP CONSTRAINT addresses_pkey;
ALTER TABLE data DROP CONSTRAINT data_pkey;
DROP INDEX data_t_out_n_idx;
```

#### load data

```
unpigz -c 0xx.bk.gz | psql -c "COPY blocks (b_id, b_time) FROM STDIN;" btcdb btcuser
unpigz -c 0xx.tx.gz | psql -c "COPY transactions (t_id, b_id, hash) FROM STDIN;" btcdb btcuser
unpigz -c 0xx.addr.gz | psql -c "COPY addresses (a_id, n, a_list) FROM STDIN;" btcdb btcuser
unpigz -c 0xx.vout.gz | psql -c "COPY data (t_out_id, t_out_n, satoshi, a_id) FROM STDIN;" btcdb btcuser
```

#### switch indeces on

```
ALTER TABLE blocks ADD CONSTRAINT blocks_pkey PRIMARY KEY (b_id);
ALTER TABLE transactions ADD CONSTRAINT transactions_pkey PRIMARY KEY (t_id);
ALTER TABLE addresses ADD CONSTRAINT addresses_pkey PRIMARY KEY (a_id);
ALTER TABLE data ADD CONSTRAINT data_pkey PRIMARY KEY (id);
ALTER TABLE transactions ADD CONSTRAINT transactions_b_id_fkey FOREIGN KEY (b_id) REFERENCES blocks (b_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE data ADD CONSTRAINT data_a_id_fkey FOREIGN KEY (a_id) REFERENCES addresses (a_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE data ADD CONSTRAINT data_t_in_id_fkey FOREIGN KEY (t_in_id) REFERENCES transactions (t_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE data ADD CONSTRAINT data_t_out_id_fkey FOREIGN KEY (t_out_id) REFERENCES transactions (t_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION;
CREATE INDEX data_t_out_n_idx ON data (t_out_n);
```

#### reindex PKs etc

```
for t in blocks transactions addresses data; do psql -q -c "REINDEX TABLE $t;" btcdb btcuser; done
```

#### updates

```
(echo "BEGIN;"; unpigz -c 0xx.vin.gz; echo "COMMIT;") | psql -q btcdb btcuser
```

## 4. Clean

### 4.1. data

```
psql -c "TRUNCATE TABLE data, addresses, transactions, blocks;" btcdb btcuser
```

### 4.2. db

```
sudo -i -u postgres psql
dropdn btcdb
dropuser btcuser
```

### 4.3. PostgreSQL

## 5. remake

```
ALTER TABLE data DROP CONSTRAINT data_pkey;
ALTER TABLE data ADD CONSTRAINT data_pkey PRIMARY KEY (t_out_id, t_out_n);

```