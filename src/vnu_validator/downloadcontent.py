#!/usr/bin/python -u
#-*- coding: utf-8 -*-
#-u for autoflush

import logging
import urllib.request, urllib.error, urllib.parse
import http.client
import re
import sys
#to print stack information
import traceback
import time
from sys import argv


def downloadcontent(url, extras = {}, log = None):

    if log is None:
        logkeys = list(logging.Logger.manager.loggerDict.keys())
        if len (logkeys) > 0 :
            #vai buscar o primeiro logger
            log = logging.getLogger(logkeys[0])
        else :
            logging.basicConfig(level=logging.INFO)
            log = logging.getLogger('downloadcontent')

    url2 = url
    # Set headers.
    headers = {'Accept': '*/*'}
    post = None
    log.debug("extras %s" % extras)
    if extras.get("method", "").upper() == "POST":
        laux = url.split('?', 1)
        url2 = laux[0]
        if len(laux) == 2 :
            post = laux[1]
        else:
            post = ""
        log.info("POST %s, post %s" % (url2, post))
    add_header = extras.get("add_header", [])
    if type(add_header) is dict:
        add_header = [add_header]
    for aux in add_header:
        headers.update(aux)
    log.info("downloadcontent headers %s" % headers)

    typemesg = "info"
    dbmesg = ""
    img = ""
    try:
        # if we dont want gzip , simple don't accept
        # req = urllib2.Request(url, None, {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'} )
        req = urllib.request.Request(url2, post, headers)
        log.info("getting url (%s)" % url)
        filedescriptor = urllib.request.urlopen(req)
        final_url = filedescriptor.url.encode("utf-8")

        img = filedescriptor.read()
        if filedescriptor.headers.get("Content-Encoding") == 'gzip':
            #oh no! this is gzip
            import io
            import gzip
            img = gzip.GzipFile(fileobj=io.StringIO(img)).read()

    except urllib.error.URLError as e:
        typemesg = "errorr"
        # messagens em HTML convem não ter < e >.
        dbmesg = "(%s) %s" % (url, str(e).replace('<','').replace('>',''))
        return url, typemesg, dbmesg
    except http.client.BadStatusLine as e:
        typemesg = "error"
        dbmesg = "server responds with a HTTP status code that we don’t understand. (%s) %s" % (url, e)
        return url, typemesg, dbmesg
    except Exception as e:
        log.debug(traceback.format_exc())
        typemesg = "error"
        dbmesg = "Error in process img/pdf (%s): %s" % (url, e)
        return url, typemesg, dbmesg

    if img.strip() == "":
        typemesg = "error"
        dbmesg = "Error img/pdf is empty ! (%s)" % (url)
        return final_url, typemesg, dbmesg

    #print final_url, img
    return final_url, img, ""

if __name__ == '__main__':
    log = logging.getLogger('downloadcontent')

    if len(argv) < 1 or len(argv) > 2 :
        print("Usage : %s infile [extras]" % sys.argv[0])
        exit(1)
    extras = {}
    if len(argv) > 1:
        try:
            extras = eval (argv[2])
        except:
            pass
        if type (extras) is not dict:
            log.info ("extras is not dict ignoring")
            extras = {}

    uri = argv[1]
    url, content, text_aux = downloadcontent(argv[1], extras)
    print(content)
