"""ICWS: I cnanot write shell.
A set of simple functions that are typically written in shell script
for Android testing automation but here written in Python due to the
inertia.
"""
import os
import subprocess
from datetime import datetime

def shell(cmd: str):
    os.system(cmd)


def adb(cmd: str):
    shell('adb ' + cmd)


def ashell(cmd: str):
    adb('shell "' + cmd + '"')


def acall(cmd: str) -> str:
    return subprocess.run('adb ' + cmd, shell=True, check=True, stdout=subprocess.PIPE).stdout.decode('utf-8')


def ascall(cmd: str) -> str:
    return acall('shell "' + cmd + '"')


def launch_fresh(app: str):
    ashell('echo 3 > /proc/sys/vm/drop_caches')
    ashell('am start-activity -S -W -c android.intent.category.LAUNCHER -a android.intent.action.MAIN %s' % app)


def fingerprint():
    return ascall('getprop ro.build.fingerprint')

def short_fingerprint():
    comp = fingerprint().split('/')
    return (comp[1] + '_' + comp[3].replace('.', ''))

def timestamp_fingerprint():
    return short_fingerprint() + '_' + datetime.now().strftime('%Y%m%d%H%M%S')