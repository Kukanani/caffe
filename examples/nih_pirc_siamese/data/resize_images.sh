EXAMPLE=examples/nih_pirc_siamese/data

for file in $EXAMPLE/dr/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 227x227! $file;
	fi
done
for file in $EXAMPLE/dc/*
do
	if [ ! -d "$file" ]
		then
		echo $file
		convert $file -resize 227x227! $file;
	fi
done