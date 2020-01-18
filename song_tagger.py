#!/usr/bin/env python

'''
Tool for tagging my music collection for tracks of my own that
I have exported. The tool expects a directory structure as follows:

- Artist
    - Album Name
        - song_name.mp3

If there is a nested structcxscure e.g.

- Artist
    - Rough
        - Year
            - Month
                - song_name.mp3

The resulting album title will be a combination of the nested
folder names: e.g. Rough_2019_June this is primarily
to support my renders from my creations
'''

from mutagen.mp3 import EasyMP3 as MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen import File
import os
import re

YEAR_REGEX = '[12]\d{3}'

def add_meta_data(file_path, artist, album, year, song):
    # TODO: Only add missing meta data

    try:
        audio = MP3(file_path)
    except ID3NoHeaderError:
        audio = MP3()
        audio.add_tags()

    audio["title"] = song
    audio["artist"] = artist
    audio["album"] = album

    if year:
        audio["date"] = year

    audio.save(file_path)


def recurse_artist(artist, path):
    recurse_dir(artist, path, "")

def recurse_dir(artist, path, album_name):
    files = os.listdir(path)

    for f in files:
        new_path = os.path.join(path, f)
        if os.path.isdir(new_path):
            print "dir: " + new_path
            recurse_dir(artist, new_path, ''.join([album_name, '_', f]) if album_name else f)
        elif os.path.isfile(new_path):
            ext = os.path.splitext(new_path)[-1].lower()

            if ext != ".mp3":
                # TODO: Better support for other file types
                continue 

            m = re.search(YEAR_REGEX, new_path)
            year = m.group(0) if m > 0 else ""
            
            print "----------- HIT --------------"
            print new_path, artist, album_name, year, f
            print "------------------------------"

            add_meta_data(new_path, artist, album_name, year, os.path.splitext(f)[0])
        else:
            print "hmmm"

def main(args):
    root_dir = args.root_dir

    if not os.path.isdir(root_dir):
        raise TypeError("root_dir is expected to be a directory")
        return

    files = os.listdir(root_dir)
    artists = [f for f in files if os.path.isdir(os.path.join(root_dir, f))]

    for a in artists:
        recurse_artist(a, os.path.join(root_dir, a))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", "-d", help="path to root directory of songs")
    parser.add_argument("--convert", "-c", help="convert file to mp3 (only works for wav for now)")
    args = parser.parse_args()

    main(args)
