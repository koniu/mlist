#!/usr/bin/python
# {{{ config 
DIR = "/mnt/movies/movies"
DIR = "/tmp/mvz"
DIR = "/home/koniu/mvz.all"
DIR = "/home/koniu/mvz"
DIR = "/mnt/zombie/shares/movies"
PICKLES = "pickles"
OUTPUT = "output"

templates = {
    'a-z': {
        'grp_title': lambda m: [alfanum(m['title'])],
        'style': 'hbig'
    },
    'date added': {
        'grp_title': lambda m: [date.fromtimestamp(m['mtime']).isoformat()],
    },
    'year': {
        'grp_title': lambda m: [m['year']], 
        'style': 'hbig'
    },
    'language': {
        'grp_title': lambda m: getkey([m,'imdb','languages']),
    },
    'director': {
        'grp_title': lambda m: getkey([m,'imdb','director']),
        'sort': lambda m: getkey([m, 'year']),
        'link': lambda g: 'http://www.imdb.com/name/nm' + g.personID,
        'style': 'tiny'
    },
    'genre': {
        'grp_title': lambda m: getkey([m,'imdb','genres']),
        'link': lambda g: 'http://www.imdb.com/genre/' + g,
    },
    'writer': {
        'grp_title': lambda m: getkey([m,'imdb','writer']),
        'sort': lambda m: getkey([m, 'year']),
        'link': lambda g: 'http://www.imdb.com/name/nm' + g.personID,
        'style': 'tiny'
    },
    'country': {
        'grp_title': lambda m: getkey([m,'imdb','countries']),
        'style': 'tiny'
    },
    'color': {
       'grp_title': lambda m: getkey([m,'imdb','color']),
    },
    'company': {
        'grp_title': lambda m: getkey([m,'imdb','production company']),
        'style': 'tiny'
    },
    'actors': {
        'grp_title': lambda m: getkey([m,'imdb','actors']),
        'sort': lambda m: getkey([m, 'year']),
        'link': lambda g: 'http://www.imdb.com/name/nm' + g.personID,
        'style': 'tiny'
    },
    'music': {
        'grp_title': lambda m: getkey([m,'imdb','music']),
        'style': 'tiny'
    },
   'producer': {
       'grp_title': lambda m: getkey([m,'imdb','producer']),
        'link': lambda g: 'http://www.imdb.com/name/nm' + g.personID,
        'style': 'tiny'
    },
    'rating': {
        'grp_title': lambda m: [getkey([m,'imdb','rating'])],
    },
    'camera': {
        'grp_title': lambda m: getkey([m,'imdb','cinematographer']),
        'link': lambda g: 'http://www.imdb.com/name/nm' + g.personID,
        'style': 'tiny'
    },
    'tags': {
        'grp_title': lambda m: getkey([m,'imdb','keywords']),
        'link': lambda g: 'http://www.imdb.com/keyword/' + g,
        'style': 'tiny'
    },
    'runtime': {
        'grp_title': lambda m: [runtime(m)],
        'style': 'hbig'
    },
    'locations': {
        'grp_title': lambda m: getkey([m,'imdb','locations']),
        'style': 'tiny'
    },
}
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
# {{{ functions
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
# {{{ alfanum
def alfanum(s):
    if s[0] in 'abcdefghijklmnopqrstuvwxyz':
        return s[0]
    else:
        return '_'
# }}}
# {{{ group
def group(key):
    grouped = {}
    for m in movies:
        for g in key['grp_title'](m):
            if not(g in grouped):
                grouped[g] = {}
                grouped[g]['mvz'] = [m]
                if g != "~":
                    grouped[g]['link'] = key.get('link', lambda g: "")(g)
                #grouped[g] = { 'link': key.get('link', lambda g: "")(g), 'mvz': [m] }
            else:
                if not (m in grouped[g].get('mvz',[])):
                    grouped[g]['mvz'].append(m)
    return grouped
# }}}
# {{{ linkify_list
def linkify_list(l,f, delimiter=", "):
    txt = ""
    for w in l:
        w = unicode(w)
        txt = txt + '<a href="%s#%s">%s<a>%s' % (f, w, w, delimiter)
    return txt[0:len(txt)-len(delimiter)]
# }}}
# {{{ movie_info
def movie_info(m):
    db = m.get('imdb',{})
    if len(db) == 0:
        return
    fn = OUTPUT + '/info/' + db.movieID
    dr = unicode(getkey([db, 'director'])[0])
    txt = \
          '<table width="100%"><tr valign="top">' +\
          '<td><span id="minfo_title">' + getkey([db, 'title']) + '</span><br>' +\
          unicode(getkey([db, 'year'])) + ' by ' +\
          linkify_list(getkey([db, 'director']), 'director.html') +\
          '<br><br><table>' +\
          '<tr valign="top"><td class="hh">writer</td><td>&nbsp;</td><td>' +\
          linkify_list(getkey([db, 'writer']), 'writer.html') + '</td></tr>\n' +\
          '<tr valign="top"><td class="hh">language</td><td>&nbsp;</td><td>' +\
          linkify_list(getkey([db, 'language']), 'language.html') + '</td></tr>\n' +\
          '<tr valign="top"><td class="hh">country</td><td>&nbsp;</td><td>' +\
          linkify_list(getkey([db, 'countries']), 'country.html') + '</td></tr>\n' +\
          '<tr valign="top"><td class="hh">runtime</td><td>&nbsp;</td><td>' +\
          unicode(string.join(getkey([db, 'runtimes']),', ')) + '</td></tr>\n' +\
          '<tr valign="top"><td class="hh">genres</td><td>&nbsp;</td><td>' +\
          linkify_list(getkey([db, 'genres']), 'genre.html') + '</td></tr>\n' +\
          '<tr valign="top"><td class="hh">rating</td><td>&nbsp;</td><td> ' +\
          unicode(getkey([db, 'rating'])) + '</td></tr>\n' +\
          '</table>' +\
          '</td>' +\
          '<td align="right"><img src="%s"></td>' % getkey([db, 'cover url']) +\
          '</tr></table>' +\
          '\n<table>' +\
          '<br><tr valign="top"><td class="hh">tagline</td><td>' +\
          getkey([db, 'taglines'])[0] + '</td></tr>\n' +\
          '<br><tr valign="top"><td class="hh">plot</td><td>' +\
          getkey([db, 'plot'])[0] + '</td></tr>\n' +\
          '<br><tr valign="top"><td class="hh">tags</td><td class="tiny">' +\
          linkify_list(getkey([db, 'keywords']), 'tags.html') + '</td></tr>\n' +\
          '<br><tr valign="top"><td class="hh">cast</td><td class="tiny">' +\
          linkify_list(getkey([db, 'actors']), 'actors.html') + '</td></tr>\n' +\
          '<br><tr valign="top"><td class="hh">aka</td><td class="tiny">' +\
          unicode(string.join(getkey([db, 'akas']),"<br>")) + '</td></tr>\n' +\
          "</table>"
    write_out(txt.encode(enc,'replace'), fn)
# }}}
# {{{ movie_out
def movie_out(m):
    if 'imdb' in m:
        tt = m['imdb'].movieID
        url = 'http://imdb.com/title/tt' + tt 
    else:
        tt = ""
        url = ''
    a = '<a href="%s" onfocus="showinfo(\'%s\')" onmouseover="showinfo(\'%s\')" onmouseout="hideinfo()">%s</a>\
        <sub>%s</sub><br>\n' % (url, tt, tt, unicode(m['title'], enc,
        'replace'),  m['year'])
    return a
# }}}
# {{{ group_out 
def group_out(link, gr,mvs):
    g = unicode(gr)
    txt = "<tr valign='top'><td style='max-width: 200px'>"+ \
        "<a href='"+link+"' class='hx " + t.get('style', '') + "' name='" +g + "'>" + g + "</a> &nbsp;<sub>" + str(len(mvs)) + \
        "</sub>&nbsp;&nbsp;<br></td><td>\n"
    for m in sorted(mvs, key=t.get('sort', None)):
        txt = txt + movie_out(m)
    txt = txt + "</td></tr>\n"
    return txt
# }}}
# {{{ links_out
def links_out():
    txt = '<span id="links">Sort by: &nbsp; '
    for x in sorted(templates):
        if x==g:
            cls='cur'
        else:
            cls=''
        txt = txt + "<a id='"+cls+"' href='"+x+".html'>"+x+"</a> | "
    return txt + "</span><br><br>"
# }}}
# {{{ write_out
def write_out(s, fn):
    f = open(fn, "w")
    f.write(s)
    f.close()
# }}}
# {{{ movie_exists
def movie_exists(d):
    for m in movies:
        if d == m['dir']:
            return True
    return False
# }}}
# {{{ get_movie
def get_movie(t):
    m = {}
    # save film's directory
    m['dir'] = t
    # parse year
    m['year'] = t[len(t)-5:len(t)-1]
    m['title'] = t[0:len(t)-7]
    # get film's imdb data
    res = db.search_movie(t)
    if len(res) > 0:
        for r in res:
            if str(getkey([r,'year'])) == str(getkey([m, 'year'])):
                result = r
                break
        if not ("result" in locals()):
            result = res[0]
        m['imdb'] = db.get_movie(result.movieID, ('main', 'plot', 'keywords', 'locations', 'connections', 'taglines', 'awards', 'soundtrack'))
    # get date added
    m['mtime'] = os.stat(DIR+"/"+t)[ST_MTIME]
    return m
# }}}
# {{{ runtime
import re
def runtime(m):
    t = getkey([m,'imdb','runtimes'])[0]
    r = re.compile('(\d+)')
    try:
        o = int(r.search(t).group(1))
        if o > 20:
            o = (o / 10)*10
    except:
        o = '_'
    return o 
# }}}
# }}}
# {{{ procedure
log(now + '\n')
# {{{ load pickes
log("*** loading pickles: ")
if not os.path.exists(PICKLES):
    os.makedirs(PICKLES)
for l in sorted(os.listdir(PICKLES)):
#for l in ['_']:
    log(l)
    ms = pickle.load(file(PICKLES+"/"+l))
    for x in ms:
        movies.append(x)
log('\n')
# }}}
# {{{ update movie info
log('*** updating film info:\n')
updated = []
# remove non-existent entries
tmp = movies
removed = 0
for m in movies:
    t = m['dir']
    if not (t in dirs):
        removed = removed + 1
        tmp.remove(m)
        log('     - ' + unicode(t, enc, 'replace') + '\n')
        if not (alfanum(t) in updated):
            updated.append(alfanum(t))
movies = tmp
added = 0
# fetch new entries
for t in sorted(dirs):
    if not movie_exists(t):
        added = added + 1
        log('     + ' + unicode(t, enc, 'replace') + ' -> ')
        m = get_movie(t)
        movies.append(m)
        if not (alfanum(t) in updated):
            updated.append(alfanum(t))
        log(getkey([m,'imdb','title']) + ' (' + unicode(getkey([m,'imdb','year'])) + ')\n')
log('     = added %d, removed %d (%d)\n' % (added, removed, added - removed))
# }}}
# {{{ update pickles
if len(updated) > 0:
    log('*** updating pickles: ')
for p in updated:
    log(p)
    pkl = []
    for m in movies:
        if alfanum(m['dir']) == p:
            pkl.append(m)
    pickle.dump(pkl, file(PICKLES+"/"+p, "w"), True)
if len(updated) > 0:
    log('\n')
# }}}
# {{{ get stats
log('*** generating stats')
size = pread('du -sh '+DIR+' | cut -f1')
stats = '<span id="stats">%s &nbsp; - &nbsp; total %s &nbsp; - &nbsp; size %s</span><br>'  % (now, str(len(movies)), size)
log('\n')
# }}}
# {{{ create output dirs
if not os.path.exists(OUTPUT+'/info'):
    os.makedirs(OUTPUT+'/info')
# }}}
# {{{ copy static files
log('*** copying static files\n')
for f in os.listdir('html/static'):
    write_out(fread("html/static/" + f), OUTPUT+"/"+f)
# }}}
# {{{ write movie info 
c = 1
log('*** generating film info pages: ' + str(c))
for m in sorted(movies):
    movie_info(m)
    log('\b' * len(str(c-1)) + str(c))
    c = c + 1
log('\n')
# }}}
# {{{ write lists
log('*** generating lists: ')
for g in sorted(templates):
    log(g + ' ')
    t = templates[g]
    grouped = group(t)
    txt = fread("html/header.html") + stats + links_out() + "<table>"
    for (gr,mvs) in sorted(grouped.items()):
        txt = txt + group_out(mvs.get('link', ''), gr, mvs['mvz']).encode(enc,'replace')
    write_out(txt, OUTPUT+"/"+g+".html")
log('\n')
# }}}
# }}}
# vim: foldmethod=marker:filetype=python:expandtab:tabstop=4:shiftwidth=4:encoding=utf-8:textwidth=80
