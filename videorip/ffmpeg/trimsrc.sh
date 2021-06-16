#!/bin/sh
rm mylist.txt

for i in $( seq 0 7 );
do ffmpeg -probesize 4096M -i $1  -ss 00:`expr $i \* 8`:00 -t 00:00:15 -map 0 -c copy split$i$2;
    echo "file './split$i$2'" >> mylist.txt
done

for i in $( seq 0 3 );
do ffmpeg -probesize 4096M -i $1  -ss 01:`expr $i \* 8`:00 -t 00:00:15 -map 0 -c copy splith1$i$2;
    echo "file './splith1$i$2'" >> mylist.txt
done
