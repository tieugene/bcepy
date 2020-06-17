# 1. 100k (time, psql)
## 1.0. > dev/null:	6"
## 1.1. INSERT
1.1.1. w/ constraints:	3'33"	65
1.1.2. w/o constraints:	2'32"	48
## 1.2. COPY
1.2.1. w/ constraints:	0'47"	65
1.2.2. w/o constraints:	0'7"	54
## 1.3. UPDATE
1.3.1. w/ constraints:	1'33"	81
1.3.2. w/o constraints:	90'+ (75 items)	x
# 2. 200k
## 2.0. > dev/null:	3'51"
## 2.1. INSERT
2.1.1. w/ constraints:	191'58"	238>3508
2.1.2. w/o constraints:	120'41"	431>2623	+7" idx
## 1.2. COPY
2.2.1. w/ constraints:	51"3'	991>
2.2.2. w/o constraints:	7"7'	865>3391	+8" idx
## 1.3. UPDATE
2.3.1. w/ constraints:	238"38'	4416>4544
2.3.2. w/o constraints:	~~not tested~~
