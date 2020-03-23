import json

from ocean_utils.utils.utilities import get_timestamp


def get_metadata_example():
    metadata_path = 'assets/sample_metadata.json'
    with open(metadata_path) as f:
        metadata = json.load(f)

    metadata['main']['dateCreated'] = get_timestamp()
    return metadata

