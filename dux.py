#!/usr/bin/python2
import os
import random
import re
import shlex
import subprocess

from subprocess import CalledProcessError
from subprocess import Popen
from subprocess import STDOUT
from subprocess import check_call
from subprocess import check_output

# Returns array of currently running sessions sorted by alphanumeric order
# TODO figure out how to break this up and fail correctly
def sessions():
    out=check_output("tmux list-sessions | cut -d \":\" -f1 | sort -d", shell=True, stderr=STDOUT)
    match=re.match("failed to connect to server.*", out)
    if match:
        raise CalledProcessError("1", "tmux list-sessions", "No tmux sessions currently accessible")
    else:
        return out.splitlines()

def new_session(name):
    try:
        return check_output(["tmux new -s " + quote(name)], shell=True, stderr=STDOUT)
    except CalledProcessError:
        raise

def quote(string):
    if not re.match("^\".*\"$", string):
        return '"' + string + '"'
    else:
        return string

def timestamp():
    return check_output(["date +%s"], shell=True)

def attach(name):
    try:
        return check_output(["tmux attach -t " + quote(name)], shell=True, stderr=STDOUT)
    except CalledProcessError:
        raise

def random_line(afile):
    line = next(iter(afile))
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line

def random_dict_word(dictionaries):
    return random_line(get_dictionary("cracklib", dictionaries)).strip()

def get_dictionary(name, dictionaries):
    for d in dictionaries:
        dict_name=d["name"]
        dict_location=d["location"]

        if dict_name == name:
            return get_file(dict_location)

def get_file(location):
    with file(location) as f:
        return f.readlines()

def attach_new_session(name):
    new_session(name)

def gen_session_name():
    dictionaries=get_dictionaries()
    return random_dict_word(dictionaries) + " " + random_dict_word(dictionaries)

def get_dictionaries():
    dictionaries = [
        {
            "name" : "cracklib",
            "location" : "/usr/share/dict/cracklib-small"
        }
    ]

    return dictionaries

### BEGIN MAIN LOOP

def main():
    try:
        session=sessions()[0]
        print("Attaching to " + session)
        attach(session)
    except CalledProcessError as e:
        session_name = gen_session_name()
        print("Creating new session " + session_name)
        try:
            attach_new_session(session_name)
        except CalledProcessError as e:
            print("Failed to create new session named '" + session_name + "'")

main()
