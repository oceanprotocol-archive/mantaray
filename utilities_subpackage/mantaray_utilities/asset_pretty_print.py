"""

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

