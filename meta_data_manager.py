#!/usr/bin/python
import os
import audiotools
import taglib


def print_meta_data(audio_file):
    tags = audio_file.tags

    if len(tags) > 0:
        max_key_len = max(len(key) for key in tags.keys())
        for key, values in tags.items():
            for value in values:
                print(('{0:' + str(max_key_len) + '} = {1}').format(key, value))


def add_meta_data(file, print_data=True):
    audio_file = taglib.File(file)

    if "ARTIST" not in audio_file.tags:
        audio_file.tags["ARTIST"] = ["Recording"]
        audio_file.save()

    if print_data:
        print "TAGS OF '{0}'".format(os.path.basename(file))
        print_meta_data(audio_file)


def main(args):
    path = args.path

    if os.path.isdir(path):
        files = os.listdir(path)

        for f in files:
            if not os.path.isfile(f):
                continue

            ext = os.path.splitext(f)[-1].lower()

            if ext == ".wav":
                continue

            add_meta_data(f, args.verbose)

    elif os.path.isfile(path):
        add_meta_data(path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", help="path to file or directory")
    parser.add_argument("--verbose", "-v", type=bool)
    args = parser.parse_args()

    main(args)
