#!/usr/bin/env python
import os
import json
import shutil
import tempfile
import logging
import random
import string
from util import subtools
from mako.lookup import TemplateLookup

from ApolloOrganism import ApolloOrganism
from ApolloUser import ApolloUser

class ApolloInstance(object):
    def __init__(self, apollo_host, apollo_admin, tool_directory):
        self.apollo_host = apollo_host
        self.tool_directory = tool_directory
        self.logger = logging.getLogger(__name__)
        self.apollo_admin =  apollo_admin
        self.apolloTemplate = self._getApolloTemplate()
        self._arrow_init()
    
    
    def _arrow_init(self):
        subtools.verify_user_login(self.apollo_admin['user_email'], self.apollo_admin['password'], self.apollo_host)
        arrow_config = tempfile.NamedTemporaryFile(bufsize=0)
        with open(arrow_config.name, 'w') as conf:
            htmlMakoRendered = self.apolloTemplate.render(
            apollo_host = self.apollo_host,
            admin_user = self.apollo_admin['user_email'],
            admin_pw = self.apollo_admin['password']
        )
            conf.write(htmlMakoRendered)

        home_dir = os.path.expanduser('~')
        arrow_config_dir = os.path.join(home_dir, '.apollo-arrow.yml')
        shutil.copyfile(arrow_config.name, arrow_config_dir)
        self.logger.debug("Initated arrow: apollo-arrow.yml= %s", arrow_config_dir)
    
    #TODO: Encode admin password
    '''
    def _generatePassword(self, length=8):
        chars = string.digits + string.letters
        pw = ''.join([random.choice(chars) for _ in range(length)])
        return pw
    '''

    def _getApolloTemplate(self):
        mylookup = TemplateLookup(directories=[os.path.join(self.tool_directory, 'templates')],
                                  output_encoding='utf-8', encoding_errors='replace')
        apolloTemplate = mylookup.get_template("apollo-arrow.yml")
        return apolloTemplate

   
    def manageApolloOrganism(self, organism_name, organism_dir, action):
        organism = ApolloOrganism(organism_name, organism_dir) 
        if action == "add":
            organism.addOrganism()
            self.logger.info("Successfully add a new organism (%s) to Apollo", organism_name)
        elif action == "overwrite":
            organism.overwriteOrganism()
            self.logger.info("Successfully overwrite the organism %s", organism_name)
        else:
            self.logger.error("Invalid operation %s", action)
            exit(-1)

    def manageApolloUser(self, operations_dictionary = dict()):
        for operation, users_list in operations_dictionary.items(): 
            apollo_user = ApolloUser(users_list)
            if operation == "create":
                apollo_user.createApolloUser()
            elif operation == "delete":
                apollo_user.deleteApolloUser()
            elif operation == "add":
                apollo_user.addApolloUserToGroup()
            elif operation == "remove":
                apollo_user.removeApolloUserFromeGroup()

    
