"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""
import logging
import configparser
import logging
from .config import get_config_file_path
from squid_py.ocean.ocean import Ocean
from pathlib import Path
# assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)
PATH_CONFIG = get_config_file_path()

PASSWORD_MAP = {
    '0x00bd138abd70e2f00903268f3db08f2d25677c9e' : 'node0',
    '0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0' : 'secret',
    '0xa99d43d86a0758d5632313b8fa3972b6088a21bb' : 'secret',
    # '0x64137af0104d2c96c44bb04ac06f09ec84cc5ae4' : '',
}

class User():
    def __init__(self, name, role, address, config_path=None):
        """
        A class to represent a User of Ocean Protocol.
        A User's account can be *locked*. To unlock an account, provide the password to the .unlock() method.

        :param name: Just to keep track and personalize the simulation
        :param role: Also just for personalizing
        :param address: This the account address
        :param config_path: The Ocean() library class *requires* a config file
        """
        self.name = name
        self.address = address
        self.role = role
        self.credentials = False # Does this config file have a user address and pasword?
        self.config_path = config_path

        self.ocn = None
        self.account = None

        # If the account is unlocked, instantiate Ocean and the Account classes
        if self.address.lower() in PASSWORD_MAP:
            logging.debug("Found password entry for this address")
            password = PASSWORD_MAP[self.address.lower()]

            # The ocean class REQUIRES a .ini file -> need to create this file!
            if not self.config_path:
                self.config_fname = "{}_{}_config.ini".format(self.name,self.role).replace(' ', '_')
                config_path = self.create_config(password) # Create configuration file for this user

            # Instantiate Ocean and Account for this User
            self.ocn = Ocean(config_path)
            if self.ocn.main_account: # If this attribute exists, the password is stored
                self.credentials = True
            # self.unlock(password)
            acct_dict_lower = {k.lower(): v for k, v in self.ocn.accounts.items()}
            self.account = acct_dict_lower[self.address.lower()]

        logging.info(self)

    def create_config(self,password):
        """Fow now, a new config.ini file must be created and passed into Ocean for instantiation"""
        conf = configparser.ConfigParser()
        conf.read(str(PATH_CONFIG))
        conf['keeper-contracts']['parity.address'] = self.address
        conf['keeper-contracts']['parity.password'] = password
        out_path = Path.cwd() / 'user_configurations' / self.config_fname
        logging.info("Create a new configuration file for {}.".format(self.name))
        with open(out_path, 'w') as fp:
            conf.write(fp)
        return out_path

    @property
    def locked(self):
        #TODO: This needs to be more robust, just having a password does not mean it's unlocked!
        if self.credentials:
            return False
        else:
            return True

    def __str__(self):
        if not self.credentials:
            return "{:<20} {:<20} LOCKED ACCOUNT".format(self.name, self.role)
        else:
            ocean_token = self.account.ocean_balance
            return "{:<20} {:<20} with {} Ocean token".format(self.name, self.role, ocean_token)

    def __repr__(self):
        return self.__str__()

def get_all_users(addresses):
    users = list()
    for i, acct_address in enumerate(addresses):
        user_name = "User_"+str(i)
        user = User(user_name, "Role", acct_address)
        users.append(user)
    return users

def get_user(role = 'Data Owner'):
    return User