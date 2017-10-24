#!/usr/bin/env python
import os
import sys
import argparse
import json
import logging
import socket
from apollo.ApolloInstance import ApolloInstance
from util.Reader import Reader
from util.Logger import Logger


def main(argv):
    parser = argparse.ArgumentParser(description='Upload a hub to display on Apollo.')
    parser.add_argument('-j', '--data_json', help='JSON file containing the metadata of the inputs')
    parser.add_argument('-o', '--output', help='HTML output')
    
    #parser.add_argument('-e', '--extra_file_path', help='Extra file path for generated jbrowse hub')
    #parser.add_argument('-d', '--jbrowsehub', help='Name of the HTML summarizing the content of the JBrowse Hub Archive')

    # Get the args passed in parameter
    args = parser.parse_args()
    json_inputs_data = args.data_json
    outputFile = args.output
    #outputFile = args.jbrowsehub
    
    
    ##Parse JSON file with Reader
    reader = Reader(json_inputs_data)

    # Begin init variables
    extra_files_path = reader.getExtFilesPath()
    #user_email = reader.getUserEmail() 
    species_name = reader.getSpeciesName() 
    #apollo_host = reader.getApolloHost()
    apollo_port = reader.getPortNum()
    apollo_host = "http://localhost:"+ apollo_port + "/apollo"
    #apollo_host = "http://localhost:8080/apollo"
    #apollo_user = reader.getApolloUser()
    apollo_admin_user = reader.getAdminUser()
    toolDirectory = reader.getToolDir()
    #jbrowse_hub = reader.getJBrowseHubDir()
    debug_mode = reader.getDebugMode()

    #### Logging management ####
    # If we are in Debug mode, also print in stdout the debug dump
    log = Logger(tool_directory=toolDirectory, debug=debug_mode, extra_files_path=extra_files_path)
    log.setup_logging()

    logging.info("#### JBrowseArchiveCreator: Start to upload JBrowse Hub to Apollo instance: %s #### ", apollo_host)
    logging.debug('JSON parameters: %s\n\n', json.dumps(reader.args))

    # Set up apollo
    apollo = ApolloInstance(apollo_host, apollo_admin_user, toolDirectory) 
    jbrowse_hub_dir = _getHubDir(extra_files_path)
    apollo.loadHubToApollo(apollo_admin_user, species_name, jbrowse_hub_dir, admin=True)
    outHtml(outputFile, apollo_host, species_name)

    logging.info('#### JBrowseArchiveCreator: Congratulation! JBrowse Hub is uploaded! ####\n')
    
def _getHubDir(extra_files_path):
    for root, dirs, files in os.walk(extra_files_path):
        for name in files:
            if name == "trackList.json":
                logging.debug("JBrowse hub directory: %s", root)
                return root
    logging.error("Cannot find jbrowsehub")
    exit(-1)

def outHtml(outputFile, host_name, species_name):
    with open(outputFile, 'w') as htmlfile:
        htmlstr = 'The new Organism "%s" is created on Apollo: <br>' % species_name
        jbrowse_hub = '<li><a href = "%s" target="_blank">View JBrowse Hub on Apollo</a></li>' % host_name
        htmlstr += jbrowse_hub
        htmlfile.write(htmlstr)     

if __name__ == "__main__":
    main(sys.argv)