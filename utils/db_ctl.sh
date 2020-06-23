#!/bin/sh
# Tool to manipulate bce interim data

declare -a table
table=([b]=blocks [t]=transactions [a]=addresses [d]=data)
echo "${table[b]}"

function help() {
  echo "Usage: $0 <cmd> <table>\n\
  cmd:\n\
    drop:\tdrop table\n\
    create:\tcreate table from scratch\n\
    show:\tshow table structure\n\
    trunc:\tdelete all records\n\
    idxoff:\tdelete all indices and constraints\n\
    idxon:\tcreate all indices and constraints\n\
    vacuum:\tvacuum table\n\
    load:\tload table from txt data\n\
  table:\n\
    b\tblocks\n\
    t\ttransactions\n\
    a\taddresses\n\
    d\tdata\n\
    z\tall\
"
  exit
}

function chk_table() {
  if [[ ! "abdt" =~ $1 ]]; then
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
    show $2;;
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
