# %%
import requests
import json

# %%
# ## Constants
organization_name = 'oceanprotocol'

UNAME=""
UPASS=""

# %%
# ## Get the access token

url = r'https://hub.docker.com/v2/users/login/'
headers = None
data = {'username': UNAME, 'password' : UPASS}
params = None
r = requests.get(url, headers=headers, data=data, params=params)

token = r.content.decode("utf-8")
token_dict = json.loads(token)

# %%
# ## Get the repos
url = 'https://hub.docker.com/v2/repositories/{}/?page_size=100'.format(organization_name)
headers = {'Authorization': token_dict['token']}
data = None
params = None
r = requests.get(url, headers=headers, data=data, params=params)


repo_def = json.loads(r.content.decode("utf-8"))

for repo in repo_def['results']:
    if repo['pull_count']:
        pull_count = repo['pull_count']
    else:
        pull_count = None
    print("{:25} updated {:20} with {} pulls".format(repo['name'],repo['last_updated'],)

