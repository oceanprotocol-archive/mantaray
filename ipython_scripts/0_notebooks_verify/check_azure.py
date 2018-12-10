#%%
from azure.storage.common import CloudStorageAccount
from azure.storage.blob import PublicAccess, BlockBlobService
from azure.storage.blob.models import ContentSettings
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.storage import StorageManagementClient

RESOURCE_GROUP = 'ocean-test-storage'
STORAGE_ACCOUNT_NAME = 'oceanblob'
CONTAINER_NAME = 'ocean-container'

# log in
storage_client = get_client_from_cli_profile(StorageManagementClient)

# create a public storage container to hold the file
storage_keys = storage_client.storage_accounts.list_keys(RESOURCE_GROUP, STORAGE_ACCOUNT_NAME)
storage_keys = {v.key_name: v.value for v in storage_keys.keys}

storage_client = CloudStorageAccount(STORAGE_ACCOUNT_NAME, storage_keys['key1'])
blob_service = storage_client.create_block_blob_service()
blob_service.create_container(CONTAINER_NAME, public_access=PublicAccess.Container)

#%%
FILE_NAME = 'hello-ocean.html'
blob_service.create_blob_from_bytes(
    CONTAINER_NAME,
    FILE_NAME,
    b'<center><h1> Surf the Ocean again! </h1></center>',
    content_settings=ContentSettings('text/html')
)

print(blob_service.make_blob_url(CONTAINER_NAME, FILE_NAME))

#%%

for blob in blob_service.list_blobs(CONTAINER_NAME):
    print(blob.name)


