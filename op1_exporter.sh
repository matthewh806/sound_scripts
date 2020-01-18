#!/bin/bash

# A simple utility for exporting OP-1 files
# It will place them in a structure like:
# track_name/
#	track_name.aif
#       tape/
#		track_1_xx.xbpm.aif
#		...
#		track_4_xx.xbpm.aif

OP1_PATH=/Volumes/OP-1

# TODO:
# Use Getopts for CL arg parsing
# Append BPM to filename
# Choose whether or not to export tape
# Choose which side of the album too export
# Convert to BPM?

if [[ "$#" -ne 3 ]]; then
	echo "Error. Illegal number of parameters. USAGE $0 track_name Directory BPM"
	exit 2
fi

if [[ ! -d ${OP1_PATH} ]]; then
	echo "Error: Path not found ${OP1_PATH}"
	exit 1
fi

TRACK_NAME=$1
DIR=$2
TRACK_DIR=$DIR/$TRACK_NAME
TAPE_DIR=$TRACK_DIR/tape

BPM=$3

# Create required directories first
mkdir -p $DIR
mkdir -p $TRACK_DIR
mkdir -p $TAPE_DIR

cp $OP1_PATH/album/side_a.aif $TRACK_DIR/${TRACK_NAME}_a.aif
cp $OP1_PATH/album/side_b.aif $TRACK_DIR/${TRACK_NAME}_b.aif

cp $OP1_PATH/tape/*.aif $TAPE_DIR/
for f in $TAPE_DIR/*.aif; do
	mv "$f" "${f%.aif}_${BPM}bpm.aif";
done

