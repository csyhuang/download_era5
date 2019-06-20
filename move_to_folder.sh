!#/bin/bash

# Create folders
for i in {1998..2006}; do
    mkdir $i;
done

# Move .nc files into the folders
for i in {1998..2006}; do
    mv ${i}*.nc ${i};
done