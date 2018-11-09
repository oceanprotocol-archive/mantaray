import requests
import json
from squid_py.ocean.ocean import Ocean
from squid_py.ocean.asset import Asset
from pathlib import Path
from requests.compat import urljoin
import hashlib
import logging
import urllib

class LoggerCritical:
    def __enter__(self):
        my_logger = logging.getLogger()
        my_logger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")

# print(squid)
# %% Instantiate Ocean
config_path = Path.cwd() / 'config_k8s.ini'
assert config_path.exists()
ocn = Ocean(config_path)
# %%
# Get the metadata
meta_data_links = [
    "https://s3.eu-central-1.amazonaws.com/trilobite/British_birdsong/metadata.json",
    "https://s3.eu-central-1.amazonaws.com/trilobite/Humpback_identification/metadata.json",
    "https://s3.eu-central-1.amazonaws.com/trilobite/Monkey_Species/metadata.json",
    "https://s3.eu-central-1.amazonaws.com/trilobite/World_Population/metadata.json",
]

# Download or load the metadata
resp = requests.get(meta_data_links[0])
assert resp.status_code == 200
metadata = resp.json()

# Generate the DID
did = hashlib.sha256(json.dumps(metadata['base']).encode('utf-8')).hexdigest()

# Generate the Service Endpoint (Aquarius)
service_endpoint = urljoin(ocn.metadata._base_url,f"metadata/{did}")

# Instantiate the Asset object
asset = Asset.create_from_metadata(metadata, service_endpoint)

# %%
# Publish the DDO to Aquarius
print(asset)

# if asset.asset_id in ocn.metadata.list_assets():
#     raise OceanDIDAlreadyExist
logging.info("Publishing {} in aquarius".format(asset.did))

# The base_url is not correct! Update
aqua_url = urllib.parse.urlparse(ocn.metadata._base_url)
 # + '/ddo'
# urllib.parse.urljoin(aqua_url.scheme + ':', aqua_url.netloc,'ddo')
headers = {'content-type': 'application/json'}
# ocn.metadata._base_url = 'http://' + aqua_url.netloc
requests.post(ocn.metadata._base_url + '/api/v1/assets/ddo', data=asset.ddo.as_text(), headers=headers)


ocn.metadata.publish_asset_metadata(asset.did, asset.ddo)
