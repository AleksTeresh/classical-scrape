#!/usr/bin/env python

from subprocess import call

args = ["cron", "-f", "-L 15"]
call(args)