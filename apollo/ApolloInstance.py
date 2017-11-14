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


class ApolloInstance(object):
    def __init__(self, apollo_host, apollo_admin, tool_directory):
        self.apollo_host = apollo_host
        self.tool_directory = tool_directory
        self.logger = logging.getLogger(__name__)
        self.apollo_admin =  apollo_admin
        self.apolloTemplate = self._getApolloTemplate()
        self._arrow_init()
    
    
    def _arrow_init(self):
        subtools.verify_user_login(self.apollo_admin.user_email, self.apollo_admin.password, self.apollo_host)
        arrow_config = tempfile.NamedTemporaryFile(bufsize=0)
        with open(arrow_config.name, 'w') as conf:
            htmlMakoRendered = self.apolloTemplate.render(
            apollo_host = self.apollo_host,
            admin_user = self.apollo_admin.user_email,
            admin_pw = self.apollo_admin.password
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

    def createApolloUser(self, apollo_user, admin=None):
        p = subtools.arrow_create_user(apollo_user.user_email, apollo_user.firstname, apollo_user.lastname, apollo_user.password, admin) 
        user_info = json.loads(p)
        user_id = user_info.get('userId')
        if not user_id:
            self.logger.debug("Cannot create new user: %s; The user may already exist", apollo_user.user_email)
            subtools.verify_user_login(apollo_user.user_email, apollo_user.password, self.apollo_host)
            user_id = subtools.arrow_get_users(apollo_user.user_email)
            self.logger.debug("Got user_id for new or existing user: user_id = %s", str(user_id))
        return user_id   

    def grantPermission(self, user_id, organism_id, **user_permissions):
        subtools.arrow_update_organism_permissions(user_id, organism_id, **user_permissions)
        self.logger.debug("Grant user %s permissions to organism %s, permissions = %s", str(user_id), str(organism_id), ','.join(user_permissions))

    def addOrganism(self, organism_name, organism_dir):
        exist = self.getOrganism(organism_name)
        if not exist:
            self.logger.debug("The organism does not exist.")
            p = subtools.arrow_add_organism(organism_name, organism_dir)
            if not p:
                self.logger.error("The user %s is not authorized to add organism", self.apollo_admin.user_email)
                exit(-1)
            organism = json.loads(p)
            organism_id = organism['id']
            self.logger.debug("A new organism %s was added to Apollo instance", p)
            return organism_id
        else:
            self.logger.error("The organism %s already exists! Rerun the tool to use a different species name or choose to overwrite the organism", organism_name)
            exit(-1)

    #TODO: the JSON dictionary return by deleteOrganism still contains the deleted organism. Improve the API.
    def deleteOrganism(self, organism_name):
        organism_id = self.getOrganism(organism_name)
        if organism_id:
            self.logger.debug("Deleting the organism %s", organism_name)
            subtools.arrow_delete_organism(organism_id)
            if not self.getOrganism(organism_name):
                self.logger.debug("Organism %s has been deleted", organism_name)
            else:
                self.logger.error("Organism %s cannot be deleted", organism_name)
                exit(-1)
        else:
            self.logger.error("Organism %s doesn't exist", organism_name)
            exit(-1)

    #TODO: filtering by commonName doesn't work. Improve the API.
    def getOrganism(self, organism_name):
        p = subtools.arrow_get_organism(organism_name)
        if p:
            return str(p)

    #TODO: API update_organism not working. Improve the API to enable updating directory.
    def overwriteOrganism(self, organism_name, organism_dir):
        self.deleteOrganism(organism_name)
        p = subtools.arrow_add_organism(organism_name, organism_dir)
        if not p:
            self.logger.error("The user is not authorized to add organism")
            exit(-1)
        organism = json.loads(p)
        organism_id = organism['id']
        self.logger.debug("A new organism %s has been added to Apollo instance", p)
        return organism_id
        
    
    def loadHubToApollo(self, organism_name, organism_dir, action):
        if action == "add":
            self.addOrganism(organism_name, organism_dir)
            self.logger.info("Successfully add a new organism (%s) to Apollo", organism_name)
        elif action == "overwrite":
            self.overwriteOrganism(organism_name, organism_dir)
            self.logger.info("Successfully overwrite the organism %s", organism_name)
        else:
            self.logger.error("Invalid operation %s", action)
            exit(-1)
        