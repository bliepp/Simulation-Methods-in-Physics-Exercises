#!/bin/bash

fn=outfiles/ex_3_5.out
echo "#n\tt" > $fn
for i in {3..13}; do
	echo "Calculating for $i*$i = $(($i*$i)) particles"
	python ex_3_5.py $i >> $fn
done
