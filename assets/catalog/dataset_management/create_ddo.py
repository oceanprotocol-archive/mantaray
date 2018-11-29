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

TEMP_DDO2 = {
  "@context": "https://w3id.org/future-method/v1",
  "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
  "publicKey": [
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a#keys-1",
      "type": "RsaVerificationKey2018",
      "owner": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a#keys-2",
      "type": "Ed25519VerificationKey2018",
      "owner": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "publicKeyBase58": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a#keys-3",
      "type": "RsaPublicKeyExchangeKey2018",
      "owner": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
    }
  ],
  "authentication": [
    {
      "type": "RsaSignatureAuthentication2018",
      "publicKey": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a#keys-1"
    },
    {
      "type": "ieee2410Authentication2018",
      "publicKey": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a#keys-2"
    }
  ],
  "service": [
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "OpenIdConnectVersion1.0Service",
      "serviceEndpoint": "https://openid.example.com/"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "CredentialRepositoryService",
      "serviceEndpoint": "https://repository.example.com/service/8377464"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "XdiService",
      "serviceEndpoint": "https://xdi.example.com/8377464"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "HubService",
      "serviceEndpoint": "https://hub.example.com/.identity/did:op:0123456789abcdef/"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "MessagingService",
      "serviceEndpoint": "https://example.com/messages/8377464"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "SocialWebInboxService",
      "serviceEndpoint": "https://social.example.com/83hfh37dj",
      "description": "My public social inbox",
      "spamCost": {
        "amount": "0.50",
        "currency": "USD"
      }
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a;bops",
      "type": "BopsService",
      "serviceEndpoint": "https://bops.example.com/enterprise/"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "Consume",
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/consume?pubKey=${pubKey}&serviceId={serviceId}&url={url}"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "Compute",
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/compute?pubKey=${pubKey}&serviceId={serviceId}&algo={algo}&container={container}"
    },
    {
      "id": "did:op:3597a39818d598e5d60b83eabe29e337d37d9ed5af218b4af5e94df9f7d9783a",
      "type": "Metadata",
      "serviceEndpoint": "http://myaquarius.org/api/v1/provider/assets/metadata/{did}",
      "metadata": {
        "base": {
          "name": "UK Weather information 2011",
          "type": "dataset",
          "description": "Weather information of UK including temperature and humidity",
          "size": "3.1gb",
          "dateCreated": "2012-10-10T17:00:000Z",
          "author": "Met Office",
          "license": "CC-BY",
          "copyrightHolder": "Met Office",
          "encoding": "UTF-8",
          "compression": "zip",
          "contentType": "text/csv",
          "workExample": "423432fsd,51.509865,-0.118092,2011-01-01T10:55:11+00:00,7.2,68",
          "contentUrls": [
            "https://testocnfiles.blob.core.windows.net/testfiles/testzkp.zip"
          ],
          "links": [
            { "name": "Sample of Asset Data", "type": "sample", "url": "https://foo.com/sample.csv" },
            { "name": "Data Format Definition", "type": "format", "AssetID": "4d517500da0acb0d65a716f61330969334630363ce4a6a9d39691026ac7908ea" }
          ],
          "inLanguage": "en",
          "tags": "weather, uk, 2011, temperature, humidity",
          "price": 10
        },
        "curation": {
          "rating": 0.93,
          "numVotes": 123,
          "schema": "Binary Voting"
        },
        "additionalInformation": {
          "updateFrequency": "yearly",
          "structuredMarkup": [
            {
              "uri": "http://skos.um.es/unescothes/C01194/jsonld",
              "mediaType": "application/ld+json"
            },
            {
              "uri": "http://skos.um.es/unescothes/C01194/turtle",
              "mediaType": "text/turtle"
            }
          ]
        }
      }
    }
  ]
}



TEMP_DDO = {
  "@context": "https://w3id.org/future-method/v1",
  "authentication": [
    {
      "type": "RsaSignatureAuthentication2018"
    },
    {
      "publicKey": "did:op:123456789abcdefghi#keys-1"
    }
  ],
  "id": "did:op:123456789abcdefghi",
  "publicKey": [
    {
      "id": "did:op:123456789abcdefghi#keys-1"
    },
    {
      "type": "Ed25519VerificationKey2018"
    },
    {
      "owner": "did:op:123456789abcdefghi"
    },
    {
      "publicKeyBase58": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    }
  ],
  "service": [
    {
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/consume?pubKey=${pubKey}&serviceId={serviceId}&url={url}",
      "type": "Consume"
    },
    {
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/compute?pubKey=${pubKey}&serviceId={serviceId}&algo={algo}&container={container}",
      "type": "Compute"
    },
    {
      "metadata": {
        "additionalInformation": {
          "structuredMarkup": [
            {
              "mediaType": "application/ld+json",
              "uri": "http://skos.um.es/unescothes/C01194/jsonld"
            },
            {
              "mediaType": "text/turtle",
              "uri": "http://skos.um.es/unescothes/C01194/turtle"
            }
          ],
          "updateFrecuency": "yearly"
        },
        "base": {
          "author": "Met Office",
          "compression": "zip",
          "contentType": "text/csv",
          "contentUrls": [
            "https://testocnfiles.blob.core.windows.net/testfiles/testzkp.zip"
          ],
          "copyrightHolder": "Met Office",
          "dateCreated": "2012-10-10T17:00:000Z",
          "description": "Weather information of UK including temperature and humidity",
          "encoding": "UTF-8",
          "inLanguage": "en",
          "license": "CC-BY",
          "links": [
            {
              "sample1": "http://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-daily/"
            },
            {
              "sample2": "http://data.ceda.ac.uk/badc/ukcp09/data/gridded-land-obs/gridded-land-obs-averages-25km/"
            },
            {
              "fieldsDescription": "http://data.ceda.ac.uk/badc/ukcp09/"
            }
          ],
          "name": "UK Weather information 2011",
          "price": 10,
          "size": "3.1gb",
          "tags": "weather, uk, 2011, temperature, humidity",
          "type": "dataset",
          "workExample": "423432fsd,51.509865,-0.118092,2011-01-01T10:55:11+00:00,7.2,68"
        },
        "curation": {
          "numVotes": 123,
          "rating": 0.93,
          "schema": "Binary Votting"
        }
      },
      "serviceEndpoint": "http://myaquarius.org/api/v1/provider/assets/metadata/{did}",
      "type": "Metadata"
    }
  ]
}
# print(squid)
# %% Instantiate Ocean
config_path = Path.cwd() / 'config_k8s_deployed.ini'
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
#%%
ocn.metadata.publish_asset_metadata(asset.did, asset.ddo)
# %%
# Publish the DDO to Aquarius
print(asset)

# if asset.asset_id in ocn.metadata.list_assets():
#     raise OceanDIDAlreadyExist
logging.info("Publishing {} in aquarius".format(asset.did))
ocn.metadata.publish_asset_metadata(asset.did, asset.ddo)
# The base_url is not correct! Update
aqua_url = urllib.parse.urlparse(ocn.metadata._base_url)
headers = {'content-type': 'application/json'}

this_url = "http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/aquarius/assets/ddo"
resp = requests.post(this_url, data=asset.ddo.as_text(), headers=headers)
resp.status_code
resp.content
resp = requests.post(this_url, data=TEMP_DDO2, headers=headers)
resp = requests.post("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/aquarius/assets/ddo", data=TEMP_DDO, headers=headers)
resp.status_code
resp.content

resp = requests.get("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/aquarius/assets")
resp.content
requests.get("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/").content
resp = requests.post("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/aquarius/assets/ddo", data=asset.ddo.as_text(), headers=headers)
resp.content
resp.status_code
# requests.get(this_url)
# requests.get("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000")
# requests.post("http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/aquarius/assets/ddo")

# ocn.metadata.publish_asset_metadata(asset.did, asset.ddo)
