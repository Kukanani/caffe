EXAMPLE=.

for file in $EXAMPLE/dr_256/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 256x256! $file;
	fi
done
for file in $EXAMPLE/dc_256/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 256x256! $file;
	fi
done
