"""
Utility script to print varius Squid API objects to console.

Useful for inspection and debugging.
"""

def print_asset(asset):
    print("Asset ID:", asset.id)
    print("\t{} services", asset.ddo.services)

def print_ddo(ddo):
    print("DDO DID:", ddo._did)
    print("Services:")
    for svc in ddo.services:
        if 'conditions' in svc._values:
            num_conditions = len(svc._values['conditions'])
        else:
            num_conditions = 0
        print("\t{} service with {} conditions".format(svc._type, num_conditions))
        if 'conditions' in svc._values:
            for condition in svc._values['conditions']:
                if hasattr(condition, 'parameters'):
                    params = [p.name for p in condition.parameters]
                    param_string = ", ".join(params)
                    print("\t\t{}.{}({})".format(condition.contract_name, condition.function_name, param_string))

def print_ocean(ocn):
    print("\n***KEEPER NODE***")
    print("Keeper node connected at {}".format(ocn.config.keeper_url))
    print("Using ABI files from {}".format(ocn.config.keeper_path))
    print("{:>40} {}".format("Token contract address:", ocn.keeper.token.address))
    print("{:>40} {}".format("Authentication contract at address:", ocn.keeper.auth.address))
    print("{:>40} {}".format("Market contract address:", ocn.keeper.market.address))
    print("{:>40} {}".format("DID Registry contract address:", ocn.keeper.didregistry.address))

    print("\n***METADATA STORE (aquarius)***")
    print("Connect at: {}".format(ocn.metadata_store._base_url))

    print("\n***SECRET STORE***")

    print("\n***SERVICE HANDLER (brizo)***")
