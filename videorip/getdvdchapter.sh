#!/bin/bash
if [ $# -lt 1 ]; then
    echo "Usage: $0 filename title_no"
    exit 
fi

i=1
j2=01
filename=$1
echo "Using lsdvd to load chapter info:"
lsdvd -c ./
if [ -z "$2" ]; then
    echo -ne "What title number do you want to create chapter info for: "
    read title
else
    title=$2
fi
IFS=',' read -r -a CHAPTERS <<< `mplayer -identify -frames 0 "./VTS_0"$title"_0.IFO" 2>/dev/null | grep CHAPTERS: | sed 's/CHAPTERS: //'`

for chapter in "${CHAPTERS[@]}"
do
    echo "Chapter $i: $chapter"
    let i++
done

echo -ne "Creating chapter data file...."
sleep 3
for chapter in "${CHAPTERS[@]}"
do
    echo "CHAPTER$j2=$chapter" >> $filename.txt
    echo "CHAPTER"$j2"NAME=Chapter $j2" >> $filename.txt
    j2=$(printf %02d $((10#$j2 + 1 )))

done
echo "DONE."
echo "Chapter data file: $filename.txt"
