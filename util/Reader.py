import json
import re
import logging
import codecs
import socket
from apollo.ApolloUser import ApolloUser
from util import santitizer 

class Reader(object):

    def __init__(self, input_json_file):
        self.inputFile = input_json_file
        self.args = self.loadJson()
        
    
    def loadJson(self):
        try:
            data_file = codecs.open(self.inputFile, 'r', 'utf-8')   
            return json.load(data_file) 
        except IOError:
            print "Cannot find JSON file\n"
            exit(1)

    def getJBrowseHubDir(self):
        try:
            return self.args["jbrowse_hub"]
        except KeyError:
            print ("jbrowse_hub is not defined in the input file!")
            exit(1)

    def getToolDir(self):
        try:
            return self.args["tool_directory"]
        except KeyError:
            print ("tool_directory is not defined in the input file!")
            exit(1)

    def getExtFilesPath(self):
        try:
            return self.args["extra_files_path"]
        except KeyError:
            print ("extra_files_path is not defined in the input file!")
            exit(1)

    def getUserEmail(self):
        try:
            return self.args["user_email"]
        except KeyError:
            print ("user_email is not defined in the input file!")
            exit(1)
    
    def getDebugMode(self):
        try:
            return self.args["debug_mode"]
        except KeyError:
            print ("debug_mode is not defined in the input file!")
            exit(1)
            
    def getPortNum(self):
        try:
            return self.args["port"]
        except KeyError:
            print ("port is not defined in the input file!")
            exit(1)
    
    def getApolloHost(self):
        #apollo_host = self.args.get("apollo_host")
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        protocol = socket.getprotobyname(hostname)
        apollo_host = str(protocol) + str(ip)
        return apollo_host
        
        
    def getSpeciesName(self):
        species_name = santitizer.sanitize_name_input(self.args["species_name"])
        return species_name 

    def getAction(self):
        action = self.args.get("action")
        return action

    def getAdminUser(self):
        apollo_admin = self.args.get("apollo_admin")
        return apollo_admin    


    def getOperationList(self):
        l = self.args.get("operations")
        return l

    