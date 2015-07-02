#!/usr/bin/python

# Copyright (C) 2015 Chris Sivanich
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import random
import re
import shlex
import subprocess
import tmuxp

from subprocess import CalledProcessError
from subprocess import Popen
from subprocess import STDOUT
from subprocess import check_call
from subprocess import check_output

def random_dict_word(dictionaries):
    return random_line(get_dictionary("cracklib", dictionaries)).strip()

def get_dictionary(name, dictionary):
        return get_file(dictionary['location'])

def random_line(afile):
    line = next(iter(afile))
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line

def get_file(location):
    with open(location) as f:
        return f.readlines()

def gen_session_name():
    dictionaries=get_dictionaries()
    return random_dict_word(dictionaries[0]) + " " + random_dict_word(dictionaries[0])

def get_dictionaries():
    return [
        {
            "name" : "cracklib",
            "location" : "/usr/share/dict/cracklib-small"
        }
    ]

### BEGIN MAIN LOOP

def main():
    try:
        server=tmuxp.Server()
        unattached = subprocess.check_output("tmux list-sessions | grep -v 'attached' | awk -F ':' '{print $1}'", shell=True).decode("utf-8").splitlines()
    except tmuxp.exc.TmuxpException:
        unattached = None

    if not unattached:
        target=gen_session_name()
        server.new_session(session_name=target)
    else:
        target=unattached[0]

    server.attach_session(target)

main()
