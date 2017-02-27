#!/bin/bash

dhome=$HOME/Documents/data/toAnnotate/toAnnotate
i=0
mkdir Annotations
mkdir Images
mkdir ImageSets
while [ $i -lt 16 ]
do
    echo "processing folder $dhome/$i"
    cp $dhome/$i/*.png Images
    cp $dhome/$i/*.xml Annotations
    let "i=i+1"
done
ls Annotations/ -m | sed s/\\s/\\n/g | sed s/.xml//g | sed s/,//g > ImageSets/train.txt
