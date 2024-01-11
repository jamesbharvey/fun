#!/bin/bash

for file in *; do
    if [ -d "$file" ]; then
	pushd "$file"
        for zipfile in *.zip; do
	    unzip "$zipfile"
	done
	popd
    fi
done

