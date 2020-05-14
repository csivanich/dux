#!/usr/bin/env python

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
import urllib.request

from subprocess import CalledProcessError
from subprocess import Popen
from subprocess import STDOUT
from subprocess import check_call
from subprocess import check_output

def random_dict_word(dictionaries):
    return random_line(dictionaries[0]).strip()

def random_line(afile):
    print("Random line from " + afile)
    afile=open(os.path.expanduser(afile))
    line = next(iter(afile))
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line

def gen_session_name():
    return random_dict_word(dictionaries()) + " " + random_dict_word(dictionaries())

def new_session(name):
    print("Starting new session " + name)
    subprocess.check_output("tmux new -s '" + name + "'", shell=True).decode("utf-8")

def attach_session(name):
    print("Attaching to session " + name)
    subprocess.check_output("tmux attach-session -t '" + name + "'", shell=True).decode("utf-8")

def download_dict(adest):
    adest = os.path.expanduser(adest)
    print("Downloading dictionary from github to " + adest)

    dest_dir = os.path.dirname(adest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    u = urllib.request.URLopener()
    u.retrieve("https://raw.githubusercontent.com/atebits/Words/master/Words/en.txt", adest)

def dictionaries():
    afile="~/.dux/dict"
    if not os.path.exists(os.path.expanduser(afile)):
        download_dict(afile)
    return [afile]

def get_unattached_sessions():
    return subprocess.check_output("tmux list-sessions | grep -v 'attached' | grep -v \"^*\" | awk -F ':' '{print $1}'", shell=True).decode("utf-8").splitlines()

### BEGIN MAIN
if os.environ.get('TMUX'):
    print("Dux will not run inside existing tmux session! ($TMUX is set)")
    exit(127)

sessions = get_unattached_sessions()

if sessions:
    attach_session(sessions.pop())
else:
    print("No unattached sessions found")
    new_session(gen_session_name())

print("done")
