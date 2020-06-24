#!/bin/sh
# Tool to manipulate bce interim data

declare -A table
table=([b]=blocks [t]=transactions [a]=addresses [d]=data)
# echo ${table[b]}

function help() {
  echo "Usage: $0 <cmd> <table>
  cmd:
    drop:	drop table
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
  if [[ ! "btad" =~ $1 ]]; then
    echo "Bad table '$1'"
    help
  fi
}

function drop() {
  t=${table[$]}
  echo "Drop table '$t'"
  # psql -c "DROP TABLE ...,...,...;" btcdb btcuser
}

function create() {
  t=${table[$]}
  echo "Create table '$t'"
  # psql -f " TABLE ...,...,...;" btcdb btcuser
}

function show() {
  t=${table[$]}
  echo "Show '$t'"
}

function trunc() {
  t=${table[$]}
  echo "Truncate '$t'"
  # psql -c "TRUNCATE TABLE ...,...,...;" btcdb btcuser
}

[ $# != "2" ] && help
case "$1" in
  drop)
    chk_table $2
    drop $2;;
  create)
    create $2;;
  show)
    show $2;;   # RTFM: https://www.postgresqltutorial.com/postgresql-describe-table/
  trunc)
    trunc $2;;
  idxoff)
    idxoff $2;;
  idxon)
    idxon $2;;
  vacuum)
    vacuum $2;;
  load)
    load $2;;
  *)
    echo "Bad command '$1'"
    help;;
esac
