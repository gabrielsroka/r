import urllib3
import urllib.parse
from json import dumps as json_dumps, loads as json_loads
import re

headers = {'Accept-Encoding': 'gzip'}
http = urllib3.PoolManager()

def url(url, **kwargs):
    return url + '?' + urllib.parse.urlencode(kwargs)

def r(method, url, json=None):
    """Returns HTTPResponse object (including res.reason, .status, .headers) and also .json."""
    _headers = headers.copy()
    if json:
        body = json_dumps(json, separators=(',', ':')).encode()
        _headers['Content-Type'] = 'application/json'
    else:
        body = None
    res = http.request(method, url, headers=_headers, body=body)
    res.json = json_loads(data) if (data := res.data.decode()) else None
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
