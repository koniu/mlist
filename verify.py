#!/usr/bin/python
# {{{ config 
#DIR = "/mnt/movies/movies"
DIR = "/tmp/mvz"
DIR = "/home/koniu/mvz"
DIR = "/home/koniu/mvz.all"
DIR = "/mnt/zombie/shares/movies"
PICKLE_DIR = "pickles/"
# }}}
# {{{ init

# modules
from stat import *
from datetime import date#,time
import os, time, sys, string
import imdb
import cPickle as pickle
from pprint import pprint

# list of film directories
dirs = os.listdir(DIR)

# imdb object
db = imdb.IMDb()

# data structures
movies = []
stats = []

now = time.ctime()
enc = sys.stdout.encoding or sys.getdefaultencoding()
# }}}
# {{{ common functions
def fread(path):
    f = open(path)
    r = f.read()
    f.close()
    return r

def pread(cmd):
    f = os.popen(cmd)
    r = f.read()
    f.close()
    return r

def log(s):
    sys.stderr.write(unicode(s).encode(enc, 'replace'))
# }}}
# {{{ getkey
def getkey(path):
    na = '~'
    d = path[0]
    for key in path[1:len(path)]:
        if d.has_key(key):
            d = d[key]
        else:
            return na
    return d
# }}}
# {{{ load pickes
log("*** loading pickles: ")
for l in sorted(os.listdir(PICKLE_DIR)):
#for l in ['a', 'b']:
    log(l)
    ms = pickle.load(file(PICKLE_DIR+l))
    for x in ms:
        movies.append(x)
log('\n')
# }}}
print "%4s | %4s | %-50s | %-50s | %20s" % ("YEAR", "YDB", "TITLE", "TITLE_DB", "URL_DB")
print "-"*200
for m in movies:
    t = unicode(m['title'].lower(), enc, 'replace')
    ty = str(m['year'])
    tdb = getkey([m,'imdb','title']).lower()
    tydb = str(getkey([m,'imdb','year']))
    if 'imdb' in m:
        tdburl = 'http://imdb.com/title/tt' + str(m['imdb'].movieID)
    else:
        tdburl = ''
    if (t != tdb) or (ty != tydb):
        print "%-4s | %-4s | %-50s | %-60s | %20s" % (ty, tydb, t, tdb, tdburl)
# vim: foldmethod=marker:filetype=python:expandtab:tabstop=4:shiftwidth=4:encoding=utf-8:textwidth=80
