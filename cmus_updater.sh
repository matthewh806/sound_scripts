#!/bin/bash

cmus-remote -C clear
cmus-remote -C "add ~/Documents/Music/Projects/renders/"
cmus-remote -C "add ~/Documents/Music/others_songs"
cmus-remote -C "add ~/Documents/Music/books/Music Theory"

for p in ~/Documents/Music/Projects/OP-1/*/*/*; do
	echo $p
	filename=`basename $p`
	if [[ ! -e "$p/$filename.mp3" ]]; then
		ffmpeg -i "$p/$filename.aif" "$p/$filename.mp3"
	fi

	python -c "from song_tagger import add_meta_data; add_meta_data('$p/$filename.mp3', 'mdh', 'op1', '', '$filename')"

	cmus-remote -C "add $p/$filename.mp3"
done

cmus-remote -C "update-cache -f"
