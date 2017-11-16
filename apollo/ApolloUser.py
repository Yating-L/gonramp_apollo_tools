#!/usr/bin/python


import os
import json
import logging
from util import subtools

class ApolloUser(object):
    """ 
    This class is to manage Apollo users, such as create, delete, add users to a group or delete users from a group
    
    """

    def __init__(self, users_list):
        self.users_list = users_list
        self.logger = logging.getLogger(__name__)


    def createApolloUser(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_create_user(user['useremail'], user['firstname'], user['lastname'], user['password'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['false_path'])
                for u in users:
                    subtools.arrow_create_user(u['useremail'], u['firstname'], u['lastname'], u['password'])
    
    @staticmethod
    def parseUserInfoFile(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        headers = lines[0].rstrip().split('\t')
        users = []
        lines = lines[1:]
        for l in lines:
            l = l.split('\t')
            info = dict()
            fields = len(l)
            for i in range(fields):
                info[headers[i]] = l[i]
            users.append(info)
        return users

    def deleteApolloUser(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_delete_user(user['useremail'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['false_path']) 
                for u in users:
                    subtools.arrow_delete_user(u['useremail'])

    def addApolloUserToGroup(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_add_to_group(user['group'], user['useremail'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['false_path'])
                for u in users:
                    subtools.arrow_add_to_group(u['group'], u['useremail'])
                
    def removeApolloUserFromeGroup(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_remove_from_group(user['group'], user['useremail'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['false_path'])
                for u in users:
                    subtools.arrow_add_to_group(u['group'], u['useremail'])
                
                

    def grantPermission(self, user_id, organism_id, **user_permissions):
        subtools.arrow_update_organism_permissions(user_id, organism_id, **user_permissions)
        self.logger.debug("Grant user %s permissions to organism %s, permissions = %s", str(user_id), str(organism_id), ','.join(user_permissions))
