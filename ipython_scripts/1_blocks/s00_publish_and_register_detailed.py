# %% [markdown]
# ## Building Blocks: Publishing assets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 1: Import modules, and setup logging
#%%
import pathlib
import sys
import logging

import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.service_agreement.service_factory import ServiceDescriptor

# Add the local utilities package
utilities_path = Path('.') / 'script_fixtures'
if not utilities_path.exists():
    utilities_path = Path('.') / '..' / '..' / 'script_fixtures'
assert utilities_path.exists()

#Get the project root path
PATH_PROJECT_ROOT = utilities_path / '..'
PATH_PROJECT_ROOT.absolute()

utilities_path_str = str(utilities_path.absolute())
if utilities_path_str not in sys.path:
    sys.path.append(utilities_path_str)

import script_fixtures.logging as util_logging
util_logging.logger.setLevel('INFO')

logging.info("Squid API version: {}".format(squid_py.__version__))

#%%
# get_registered_ddo -> register_service_agreement_template -> get_conditions_data_from_keeper_contracts
# The data:
# contract_addresses
# fingerprints
# fulfillment_indices
# conditions_keys

# %% [markdown]
# ### Section 2: Instantiate Ocean()
#%%
# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
ocn._http_client
ocn._secret_store_client

# %% [markdown]
# ### Section 3.1: Get a Service Execution Agreement for *access*
#%%
# Get the asset type
SEA_type=squid_py.service_agreement.service_types.ServiceTypes.ASSET_ACCESS
SEA_type_name='access_sla_template.json'
# There are 2 other types currently available: 'compute_sla_template.json', and 'fitchain_sla_template.json'
#TODO: The templates are copied here in mantaray - will need to use the templates direct from pip-installed squid!

# Get the path of the .json template
SEA_template_json_path = pathlib.Path('.') / 'assets' / 'SEA_templates' / SEA_type_name
assert SEA_template_json_path.exists()
SEA_template_json_path = SEA_template_json_path.absolute()
# Instantiate the template
SEA_template = squid_py.service_agreement.service_agreement_template.ServiceAgreementTemplate.from_json_file(SEA_template_json_path.absolute())

print("Service template created: {}".format(SEA_template.name))
print(SEA_template.description)

# %% [markdown]
# ### Section 3.3: Get conditions data
#%%
_network_name = squid_py.utils.get_network_name(ocn._web3)
logging.info("Network name: {}".format(_network_name))

names = {cond.contract_name for cond in SEA_template.conditions}
name_to_contract_abi_n_address = {
  name: squid_py.keeper.utils.get_contract_abi_and_address(ocn._web3, SEA_template_json_path, name, _network_name)
  for name in names
}
contract_addresses = [
  web3.toChecksumAddress(name_to_contract_abi_n_address[cond.contract_name][1])
  for cond in conditions
]
fingerprints = [
  hexstr_to_bytes(web3, get_fingerprint_by_name(
    name_to_contract_abi_n_address[cond.contract_name][0],
    cond.function_name
  ))
  for i, cond in enumerate(conditions)
]
fulfillment_indices = [i for i, cond in enumerate(conditions) if cond.is_terminal]
conditions_keys = build_conditions_keys(web3, contract_addresses, fingerprints, sla_template_id)
return contract_addresses, fingerprints, fulfillment_indices, conditions_keys



template_id = register_service_agreement_template(
  ocn.keeper.service_agreement, ocn.keeper.contract_path,
  ocn.main_account, ServiceAgreementTemplate.from_json_file(get_sla_template_path())
)

#%%

TEST_DDO = {
  "@context": "https://w3id.org/future-method/v1",
  "id": "did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
  "publicKey": [
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-1",
      "type": "RsaVerificationKey2018",
      "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
      "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
    },
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-2",
      "type": "Ed25519VerificationKey2018",
      "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
      "publicKeyBase58": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
    },
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-3",
      "type": "RsaPublicKeyExchangeKey2018",
      "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
      "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
    }
  ],
  "authentication": [
    {
      "type": "RsaSignatureAuthentication2018",
      "publicKey": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-1"
    },
    {
      "type": "ieee2410Authentication2018",
      "publicKey": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-2"
    }
  ],
  "service": [
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
      "type": "Consume",
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/consume?pubKey=${pubKey}&serviceId={serviceId}&url={url}"
    },
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
      "type": "Compute",
      "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/compute?pubKey=${pubKey}&serviceId={serviceId}&algo={algo}&container={container}"
    },
    {
      "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
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

asset = Asset.from_ddo_dict(TEST_DDO)
asset_price = 10
service_descriptors = [ServiceDescriptor.access_service_descriptor(asset_price, '/purchaseEndpoint', '/serviceEndpoint', 600)]
ocn.register_asset(asset.metadata, unlocked_account_name, service_descriptors)