#!/usr/bin/python

PICKLE_DIR = "pickles/"

# FORMAT: year, imdb_year, title, imdb_title, imdb_url
FORMAT = '%4s | %4s | %-50s | %-50s | %20s'

import os, sys
import cPickle as pickle

movies = []
enc = sys.stdout.encoding or sys.getdefaultencoding()

# {{{ functions
def log(s):
    sys.stderr.write(unicode(s).encode(enc, 'replace'))
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
#{{{ print output
print FORMAT % ("YEAR", "YDB", "TITLE", "TITLE_DB", "URL_DB")
print "-"*128
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
        print FORMAT % (ty, tydb, t, tdb, tdburl)
#}}}
# vim: foldmethod=marker:filetype=python:expandtab:tabstop=4:shiftwidth=4:encoding=utf-8:textwidth=80
