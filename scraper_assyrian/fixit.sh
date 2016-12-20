#!/bin/bash
#for file in `cat badfiles.txt`
#	echo "hi" 

files="badfiles.txt"
while IFS= read file
do
        # display $file or do somthing with $line
	echo "$file"
	cp output/$file /tmp/$file.orig
	sed -n '/^.*\]\[/,$p' /tmp/$file.orig | sed 's/\]\[/\[/' > /tmp/$file
	cp /tmp/$file output/
	#rm /tmp/$file.orig
done <"$files"

#file=$1
#echo $file
#cp output/$file /tmp/$file.orig
#sed -n '/^.*\]\[/,$p' /tmp/$file.orig | sed 's/\]\[/\[/' > /tmp/$file
