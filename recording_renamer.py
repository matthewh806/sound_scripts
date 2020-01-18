#!/usr/bin/python
import os
import datetime


def rename_mod_time(source_dir, target_dir):
    if not os.path.exists(target_dir):
        raise ValueError("Target directory {} does not exist!".format(target_dir))

    if not os.path.exists(source_dir):
        raise ValueError("Source directory {} does not exist!".format(source_dir))

    os.chdir(target_dir)
    files = os.listdir(target_dir)

    for f in files:
        if not os.path.isfile(f):
            continue

        ext = os.path.splitext(f)[-1].lower()

        if ext != ".wav":
            continue

        t = os.path.getmtime(f)
        formatted_date = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')
        formatted_time = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%H-%M-%S')


        # check if dir. with this formatted time exists, if not create it
        if not os.path.exists(formatted_date):
            print "Creating dir: %s" % formatted_date
            os.makedirs(formatted_date)

        # check if file with this name exists, if so skip
        file_name = formatted_time + ".wav"
        if os.path.exists(formatted_date + "/" + file_name):
            print "File with name: %s already exists; skipping" % file_name
            continue

        print "Adding new file: %s mod-time: %s" % (f, formatted_time)
        os.rename(f, formatted_date + "/" + file_name)


def rename_create_time():
    pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", '-s', default="/Users/matthew/Documents/Music/Recordings")
    parser.add_argument("--target", '-t', default="/Users/matthew/Documents/Music/Recordings")
    args = parser.parse_args()

    rename_mod_time(args.source, args.target)
