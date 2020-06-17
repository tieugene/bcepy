#!/bin/sh
# switch indices off
psql -q -f idx_off.sql btcdb btcuser
