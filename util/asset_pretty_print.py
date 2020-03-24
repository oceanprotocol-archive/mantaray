"""
Utility script to print varius Squid API objects to console.

Useful for inspection and debugging.
"""
from ocean_utils.aquarius import AquariusProvider


def print_asset(asset):
    print("Asset ID:", asset.id)
    print("\t{} services", asset.ddo.services)


def print_ddo(ddo):
    print("DDO DID:", ddo.did)
    print("Services:")
    for svc in ddo.services:
        svc_values = svc.values()
        print("\t{} service with {} conditions".format(svc.type, len(svc_values.get('conditions', []))))
        for condition in svc_values.get('conditions', []):
            if hasattr(condition, 'parameters'):
                params = [p.name for p in condition.parameters]
                param_string = ", ".join(params)
                print("\t\t{}.{}({})".format(condition.contract_name, condition.function_name, param_string))


def print_ocean(ocn):
    print("\n***KEEPER NODE***")
    print("Keeper node connected at {}".format(ocn.config.keeper_url))
    print("Using ABI files from {}".format(ocn.config.keeper_path))
    print("{:>40} {}".format("Token contract address:", ocn.keeper.token.address))
    print("{:>40} {}".format("DID Registry contract address:", ocn.keeper.did_registry.address))

    print("\n***METADATA STORE (aquarius)***")
    print("Connect at: {}".format(AquariusProvider.get_aquarius().url))

    print("\n***SECRET STORE***")

    print("\n***SERVICE HANDLER (brizo)***")
