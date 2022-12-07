import urllib.request
import urllib.parse
from json import dumps as json_dumps, load as json_load
import gzip
import re
from http import HTTPStatus

headers = {'Accept-Encoding': 'gzip'}

def url(url, **kwargs):
    return url + '?' + urllib.parse.urlencode(kwargs)

def r(method, url, json=None):
    """Returns HTTPResponse object (including res.reason, .status, .headers) and also .json."""
    _headers = headers.copy()
    if json:
        data = json_dumps(json, separators=(',', ':')).encode()
        _headers['Content-Type'] = 'application/json'
    else:
        data = None
    req = urllib.request.Request(url, data, _headers, method=method)
    with urllib.request.urlopen(req) as res:
        if res.status != HTTPStatus.NO_CONTENT: # TODO: add more reasons/statuses?
            fp = gzip.open(res) if res.headers['Content-Encoding'] == 'gzip' else res
            res.json = json_load(fp)
    return res

def get_objects(url):
    while url:
        res = get(url)
        for o in res.json:
            yield o
        url = res.next_url

def get(url):
    """Returns HTTPResponse object (including res.reason, .status, .headers) and also .json, .next_url."""
    res = r('GET', url)
    links = [link for link in res.headers.get_all('link', []) if 'rel="next"' in link]
    res.next_url = re.search('<(.*)>', links[0]).group(1) if links else None
    return res 

def post(url, json=None):
    return r('POST', url, json)

def put(url, json=None):
    return r('PUT', url, json)

def patch(url, json=None):
    return r('PATCH', url, json)

def delete(url):
    return r('DELETE', url)
