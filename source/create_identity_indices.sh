#!/bin/bash
for TYPEI in 0 1 2
do
for TYPEJ in 0 1 2 3 4 5 6 7
do
echo python identity_index.py $TYPEI $TYPEJ
python identity_index.py $TYPEI $TYPEJ
done
done
