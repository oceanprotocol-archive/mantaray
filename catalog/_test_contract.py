import web3
print(web3.__version__)

from squid_py.keeper.token import Token
from squid_py.keeper.market import Market
from squid_py.keeper.auth import Auth
from squid_py.keeper.didregistry import DIDRegistry
from squid_py.ocean.account import Account

keeper_url = 'http://ac9959fcade8d11e89c320e965e714bc-777187363.us-east-1.elb.amazonaws.com:8545'

this_web3 = web3.Web3(web3.HTTPProvider(keeper_url))
token_contract_path = r"/home/batman/anaconda3/envs/mantaray_latest/artifacts/OceanToken.development.json/OceanToken.development.json/"
token_contract_path = r"/home/batman/anaconda3/envs/mantaray_latest/artifacts"
token_address = r"0xCfEB869F69431e42cdB54A4F4f105C19C080A601"

token = Token(this_web3, token_contract_path, token_address)
print(token)
print(type(token))
token_concise = token.contract_concise
accts = this_web3.eth.accounts

# Account(self.keeper, account_address)

token.get_ether_balance(accts[0])
token.get_token_balance(accts[0])
token.contract_concise.balanceOf(accts[0])

this_web3.eth.getBalance(accts[0], 'latest')

token.contract_concise.name()

