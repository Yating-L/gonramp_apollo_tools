#!/usr/bin/env python
import os
import sys
import argparse
import json
import logging
import socket
from apollo.ApolloInstance import ApolloInstance
from apollo.ApolloUser import ApolloUser
from util.Reader import Reader
from util.Logger import Logger


def main(argv):
    parser = argparse.ArgumentParser(description='Upload a hub to display on Apollo.')
    parser.add_argument('-j', '--data_json', help='JSON file containing the metadata of the inputs')
    parser.add_argument('-o', '--output', help='HTML output')
    
    # Get the args passed in parameter
    args = parser.parse_args()
    json_inputs_data = args.data_json
    outputFile = args.output
    
    ##Parse JSON file with Reader
    reader = Reader(json_inputs_data)

    # Begin init variables
    
    apollo_port = reader.getPortNum()
    apollo_host = "http://localhost:"+ apollo_port + "/apollo"
    apollo_admin_user = reader.getAdminUser()
    toolDirectory = reader.getToolDir()
    extra_files_path = reader.getExtFilesPath()
    debug_mode = reader.getDebugMode()
    operations_dictionary = reader.getOperationList()
    

    
        
    #### Logging management ####
    # If we are in Debug mode, also print in stdout the debug dump
    log = Logger(tool_directory=toolDirectory, debug=debug_mode, extra_files_path=extra_files_path)
    log.setup_logging()

    logging.info("#### Apollo User Manager: Start on Apollo instance: %s #### ", apollo_host)
    logging.debug('JSON parameters: %s\n\n', json.dumps(reader.args))

    # Set up apollo
    apollo = ApolloInstance(apollo_host, apollo_admin_user, toolDirectory) 
    apollo.manageApolloUser(operations_dictionary)
    outHtml(outputFile, apollo_host)
    logging.info('#### Apollo User Manager: Congratulation! ####\n')

def outHtml(outputFile, host_name):
    with open(outputFile, 'w') as htmlfile:
        htmlstr = 'The Apollo User Manager has done with operations on Apollo: <br>'
        jbrowse_hub = '<li><a href = "%s" target="_blank">View JBrowse Hub on Apollo</a></li>' % host_name
        htmlstr += jbrowse_hub
        htmlfile.write(htmlstr)     
        

if __name__ == "__main__":
    main(sys.argv)