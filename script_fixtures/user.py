"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""

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
            acct_dict_lower = {k.lower(): v for k, v in ocn.accounts.items()}
            self.account = acct_dict_lower[self.address.lower()]

        logging.info(self)

    def create_config(self,password):
        """Fow now, a new config.ini file must be created and passed into Ocean for instantiation"""
        conf = configparser.ConfigParser()
        conf.read(PATH_CONFIG)
        conf['keeper-contracts']['parity.address'] = self.address
        conf['keeper-contracts']['parity.password'] = password
        out_path = Path.cwd() / 'user_configurations' / self.config_fname
        logging.info("Create a new configuration file for {}.".format(self.name))
        with open(out_path, 'w') as fp:
            conf.write(fp)
        return out_path

    def __str__(self):
        if not self.credentials:
            return "{:<20} {:<20} LOCKED ACCOUNT".format(self.name, self.role)
        else:
            ocean_token = self.account.ocean_balance
            return "{:<20} {:<20} with {} Ocean token".format(self.name, self.role, ocean_token)

    def __repr__(self):
        return self.__str__()