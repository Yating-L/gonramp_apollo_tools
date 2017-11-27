#!/usr/bin/python


import os
import sys
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
                users = self.parseUserInfoFile(user['format'], user['false_path'])
                for u in users:
                    if not 'useremail' in u:
                        self.logger.error("Cannot find useremail in the text file, make sure you use the correct header, see README file for examples.")
                    if not 'firstname' in u:
                        self.logger.error("Cannot find firstname in the text file, make sure you use the correct header, see README file for examples.")
                    if not 'lastname' in u:
                        self.logger.error("Cannot find lastname in the text file, make sure you use the correct header, see README file for examples.")
                    if not 'password' in u:
                        self.logger.error("Cannot find password in the text file, make sure you use the correct header, see README file for examples.")
                    subtools.arrow_create_user(u['useremail'], u['firstname'], u['lastname'], u['password'])
    
    
    def parseUserInfoFile(self, file_format, filename):
        if file_format == "tab":
            delimiter = '\t'
        elif file_format == "csv":
            delimiter = ','
        else:
            self.logger.error("The %s format is not supported!", file_format)
        with open(filename, 'r') as f:
            lines = f.readlines()
        headers = lines[0].rstrip().split(delimiter)
        users = []
        lines = lines[1:]
        for l in lines:
            print l
            l = l.split(delimiter)
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
                users = self.parseUserInfoFile(user['format'], user['false_path']) 
                for u in users:
                    if not 'useremail' in u:
                        self.logger.error("Cannot find useremail in the text file, make sure you use the correct header, see README file for examples.")
                    subtools.arrow_delete_user(u['useremail'])

    def addApolloUserToGroup(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_add_to_group(user['group'], user['useremail'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['format'], user['false_path'])
                for u in users:
                    if not 'useremail' in u:
                        self.logger.error("Cannot find useremail in the text file, make sure you use the correct header, see README file for examples.")
                    if not 'group' in u:
                        self.logger.error("Cannot find group in the text file, make sure you use the correct header, see README file for examples.")
                    subtools.arrow_add_to_group(u['group'], u['useremail'])
                
    def removeApolloUserFromeGroup(self):
        for user in self.users_list:
            if user['batch'] == "false":
                subtools.arrow_remove_from_group(user['group'], user['useremail'])
            elif user['batch'] == "true":
                users = self.parseUserInfoFile(user['format'], user['false_path'])
                for u in users:
                    if not 'useremail' in u:
                        self.logger.error("Cannot find useremail in the text file, make sure you use the correct header, see README file for examples.")
                    if not 'group' in u:
                        self.logger.error("Cannot find group in the text file, make sure you use the correct header, see README file for examples.")
                    subtools.arrow_add_to_group(u['group'], u['useremail'])
                

