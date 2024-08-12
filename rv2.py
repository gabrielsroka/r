import http.client
import urllib.parse
import json as _json
import os
import re
import time

host = os.environ['OKTA_CLIENT_ORGURL'].replace('https://', '')
token = os.environ['OKTA_CLIENT_TOKEN']

conn = http.client.HTTPSConnection(host)
headers = {'authorization': 'SSWS ' + token}

def main():
    res = get('/api/v1/users/me')
    me = res.json
    user_id = me['id']
    print(me['id'])

    start = time.time()

    for user in get_objects('/api/v1/users', filter='profile.lastName eq "Doe"', limit=2):
        print(user['id'])

    end = time.time()

    print(f'{end - start:5.1f} sec (http.client)')

    # res = post('/api/v1/users/' + user_id, {'profile': {'title': 'admin'}})
    # me = res.json
    # print(me['profile']['title'], res.headers['x-rate-limit-remaining'])

def rh(method, url, json=None):
    _headers = headers.copy()
    if json:
        body = _json.dumps(json, separators=(',', ':')).encode()
        _headers['Content-Type'] = 'application/json'
    else:
        body = None
    conn.request(method, url, body, _headers)
    res = conn.getresponse()
    if res.reason != 'No Content':
        res.json = _json.load(res)
    return res

def get_objects(url, **fields):
    if fields: url += '?' + urllib.parse.urlencode(fields)
    while url:
        res = get(url)
        for o in res.json:
            yield o
        links = [link for link in res.headers.get_all('link') if 'rel="next"' in link]
        url = re.search('<https://[^/]+(.+)>', links[0]).group(1) if links else None

def get(url):
    return rh('GET', url)

def post(url, json=None):
    return rh('POST', url, json)

main()
