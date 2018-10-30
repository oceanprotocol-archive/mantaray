# %%
import squid_py as
import requests

#%%

endpoints = {
    'keeper-contracts': 'http://a0974921fd78611e89c320e965e714bc-1426721097.us-east-1.elb.amazonaws.com:8545',
    'pleuston': 'http://a09772bc5d78611e89c320e965e714bc-920324680.us-east-1.elb.amazonaws.com:3000',
    'aquarius': 'http://aa0979d861d78611e89c320e965e714bc-1571806593.us-east-1.elb.amazonaws.com:5000',
    'aquarius_doc': 'http://a0979d861d78611e89c320e965e714bc-1571806593.us-east-1.elb.amazonaws.com:5000/api/v1/docs'
}

requests.request('GET',endpoints['aquarius_doc'])