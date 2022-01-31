import r3
import os

# Set these secrets:
base_url = os.environ['base_url']
token = os.environ['token']

group_id = '...'

r3.headers.update({
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json'
})

res = r3.get(f'{base_url}/api/v1/users/me')
me = res.json
user_id = me['id']
print(me['profile']['login'], me['profile']['title'], res.headers['x-rate-limit-remaining'])

# Pagination.
url = r3.url(f'{base_url}/api/v1/users', filter='profile.lastName eq "Doe"', limit=2)
while url:
    res = r3.get(url)
    for user in res.json:
        print(user['profile']['login'])
    url = res.next_url
    # print(len(res.json), res.headers['x-rate-limit-remaining'])

res = r3.post(f'{base_url}/api/v1/users/{user_id}', {'profile': {'title': 'admin'}})
me = res.json
print(me['profile']['title'], res.headers['x-rate-limit-remaining'])

res = r3.put(f'{base_url}/api/v1/groups/{group_id}/users/{user_id}')
print(res.headers['x-rate-limit-remaining'])

res = r3.delete(f'{base_url}/api/v1/groups/{group_id}/users/{user_id}')
print(res.headers['x-rate-limit-remaining'])
