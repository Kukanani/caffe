EXAMPLE=.

for file in $EXAMPLE/dr_ss/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 227x227! $file;
	fi
done
for file in $EXAMPLE/dc_ss/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 227x227! $file;
	fi
done