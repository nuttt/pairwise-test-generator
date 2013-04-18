pairwise-test-generator
=======================
Python script use for generate pairwise-test with multiple parameters, values

How to Use
----------
### By Terminal
create testdata in text file in this format:
```
param1: a b
param2: c d e f
param3: g h i
param4: j k
```

then run python script in terminal
```
python pairwise.py input-file.txt
```

it will generate test and print result in terminal
```
param1  param2	param3	param4
a j	g	c
a	k	d	h
b	j	d	i
b	k	c	g
a	i	e	j
b	h	j	f
a	e	j	h
b	c	h	k
c	i	j	a
d	g	a	j
e	i	a	j
f	g	j	a

```
