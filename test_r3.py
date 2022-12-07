import r3
import os

# Set these:
org_url = os.environ['OKTA_CLIENT_ORGURL']
token = os.environ['OKTA_CLIENT_TOKEN']
group_id = '...'

r3.headers.update({
    'Authorization': 'SSWS ' + token,
    'Accept': 'application/json'
})

res = r3.get(f'{org_url}/api/v1/users/me')
me = res.json
user_id = me['id']
print(me['profile']['login'], me['profile']['title'], res.headers['x-rate-limit-remaining'])

# Pagination.
url = r3.url(f'{org_url}/api/v1/users', filter='profile.lastName eq "Doe"', limit=2)
for user in r3.get_objects(url):
    print(user['profile']['login'])

# res = r3.post(f'{org_url}/api/v1/users/{user_id}', {'profile': {'title': 'admin'}})
# me = res.json
# print(me['profile']['title'], res.headers['x-rate-limit-remaining'])

# res = r3.put(f'{org_url}/api/v1/groups/{group_id}/users/{user_id}')
# print(res.headers['x-rate-limit-remaining'])

# res = r3.delete(f'{org_url}/api/v1/groups/{group_id}/users/{user_id}')
# print(res.headers['x-rate-limit-remaining'])
