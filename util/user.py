"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""
import logging
import csv
import os
import random

from ocean_keeper.account import Account
from ocean_keeper.web3_provider import Web3Provider


def password_map(address, password_dict):
    """Simple utility to match lowercase addresses to the password dictionary

    :param address:
    :param password_dict:
    :return:
    """
    lower_case_pw_dict = {k.lower(): v for k, v in password_dict.items()}
    if str.lower(address) in lower_case_pw_dict:
        password = lower_case_pw_dict[str.lower(address)]
        return password
    else:
        return False


def load_passwords_environ():
    assert 'PASSWORD_PATH' in os.environ
    return load_passwords(os.environ['PASSWORD_PATH'])


def load_passwords(path_passwords):
    """Load password file into an address:password dictionary

    :param path_passwords:
    :return: dict
    """

    assert os.path.exists(path_passwords), "Password file not found: {}".format(path_passwords)
    passwords = dict()
    with open(path_passwords) as f:
        for row in csv.reader(f):
            if row:
                passwords[row[0]] = row[1]

    passwords = {k.lower(): v for k, v in passwords.items()}
    logging.info("{} account-password pairs loaded".format(len(passwords)))
    return passwords


def get_account(ocn):
    """Utility to get a random account
    Account exists in the environment variable for the passwords filej
    Account must have a password
    Account must have positive ETH balance

    :param ocn:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        # Only select accounts with positive ETH balance
        if ocn.accounts.balance(acct).eth/10**18 < 1:
            continue
        possible_accounts.append(acct)

    this_account = random.choice(possible_accounts)
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account


def get_account_by_index(ocn, acct_number):
    """Utility to get one of the available accounts by index (as listed in the password file)
    Account exists in the environment variable for the passwords file
    Account must have password

    :param ocn:
    :param acct_number:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        possible_accounts.append(acct)

    this_account = possible_accounts[acct_number]
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account
