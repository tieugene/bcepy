#!/bin/sh
# Tool to manipulate bce interim data

declare -A table
table=([b]=blocks [t]=transactions [a]=addresses [d]=data [z]="blocks,transactions,addresses,data")
# echo ${table[b]}

dbname=""
dbuser=""
dn=`dirname $0`
cfgname=$dn/.db_ctl.cfg

function help() {
  echo "Usage: $0 <cmd> <table>
  cmd:
    drop:   drop table
    create: create table from scratch
    show:   show table structure
    trunc:  delete all records
    idxoff: delete all indices and constraints
    idxon:  create all indices and constraints
    vacuum: vacuum table
    load:   load table from txt data
  table:
    b:  blocks
    t:  transactions
    a:  addresses
    d:  data
    z:  all"
  exit
}

function chk_table() {
  # check given table name
  if [[ ! "btadz" =~ $1 ]]; then
    echo "Bad <table> option '$1'"
    help
  fi
}

# can be altogether
function drop() {
  t=${table[$1]}
  echo "Drop table[s] '$t'."
  # psql -c "DROP TABLE $t;" $dbname $dbuser
}

function trunc() {
  t=${table[$1]}
  echo "Truncate table[s] '$t'."
  # psql -c "TRUNCATE TABLE $t;" $dbname $dbuser
}

function vacuum() {
  t=${table[$1]}
  echo "Vacuum table[s] '$t'."
  # psql -c "VACUUM FULL TABLE $t;" $dbname $dbuser
}

# separate
function create() {
  if [ ! $1 = "z" ]; then
    t=$dn/sql/c$1.sql
    echo "Create table '${table[$1]}' from '$t'."
    # psql -f $t $dbname $dbuser
  else
    echo "Create all tables."
    # cat $dn/sql/{cb.sql,ct.sql,ca.sql,cd.sql} | psql $dbname $dbuser
  fi
}

function idxoff() {
  if [ ! $1 = "z" ]; then
    t=$dn/sql/u$1.sql
    echo "Drop indices of '${table[$1]}' from '$t'."
    # psql -f $t $dbname $dbuser
  else
    echo "Drop all indices."
    # cat $dn/sql/{ud.sql,ut.sql,ua.sql,ub.sql} | psql $dbname $dbuser
  fi
}

function idxon() {
  if [ ! $1 = "z" ]; then
    t=$dn/sql/i$1.sql
    echo "Create indices of '${table[$1]}' from '$t'."
    # psql -f $t $dbname $dbuser
  else
    echo "Create all indices."
    # cat $dn/sql/{ib.sql,it.sql,ia.sql,id.sql} | psql $dbname $dbuser
  fi
}

function show() {
  # RTFM: https://www.postgresqltutorial.com/postgresql-describe-table/
  # TODO: z == ?
  t=${table[$1]}
  echo "Show '$t'"
  # pg_dump $dbname -t $t --schema-only -U $dbuser
  # \d, \dt \d+
}

function load() {
  # TODO: separate for each
  t=${table[$]}
  echo "Load table '$t'"
}

# 1. chk options
[ $# != "2" ] && help
# 2. chk cfg
if [ ! -f "$cfgname" ]; then
  echo "Please fill '$cfgname' (dbname=..., dbuser=...)"
  exit 1
fi
source $cfgname
# 3. go
chk_table $2
case "$1" in
  drop)
    drop    $2;;
  trunc)
    trunc   $2;;
  vacuum)
    vacuum  $2;;
  create)
    create  $2;;
  show)
    show    $2;;
  idxoff)
    idxoff  $2;;
  idxon)
    idxon   $2;;
  load)
    load    $2;;
  *)
    echo "Bad <cmd> '$1'"
    help;;
esac
