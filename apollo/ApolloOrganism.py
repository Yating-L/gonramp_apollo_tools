#!/usr/bin/env python

import json
import logging
from util import subtools

class ApolloOrganism(object):

    def __init__(self, organism_name, organism_dir):
        self.organism_name = organism_name
        self.organism_dir = organism_dir
        self.logger = logging.getLogger(__name__)

    def addOrganism(self):
        exist = self.getOrganism(self.organism_name)
        if not exist:
            self.logger.debug("The organism does not exist.")
            p = subtools.arrow_add_organism(self.organism_name, self.organism_dir)
            if not p:
                self.logger.error("The user is not authorized to add organism")
                exit(-1)
            organism = json.loads(p)
            organism_id = organism['id']
            self.logger.debug("A new organism %s was added to Apollo instance", p)
            return organism_id
        else:
            self.logger.error("The organism %s is already on Apollo instance! Rerun the tool to use a different species name or choose to overwrite the organism", self.organism_name)
            exit(-1)

    #TODO: the JSON dictionary return by deleteOrganism still contains the deleted organism. Improve the API.
    def deleteOrganism(self):
        organism_id = self.getOrganism(self.organism_name)
        if organism_id:
            self.logger.debug("Deleting the organism %s", self.organism_name)
            subtools.arrow_delete_organism(organism_id)
            if not self.getOrganism(self.organism_name):
                self.logger.debug("Organism %s has been deleted", self.organism_name)
            else:
                self.logger.error("Organism %s cannot be deleted", self.organism_name)
                exit(-1)
        else:
            self.logger.error("Organism %s doesn't exist", self.organism_name)
            exit(-1)

    #TODO: filtering by commonName doesn't work. Improve the API.
    @staticmethod
    def getOrganism(organism_name):
        p = subtools.arrow_get_organism(organism_name)
        if p:
            return str(p)

    #TODO: API update_organism not working. Improve the API to enable updating directory.
    def overwriteOrganism(self):
        self.deleteOrganism()
        p = subtools.arrow_add_organism(self.organism_name, self.organism_dir)
        if not p:
            self.logger.error("The user is not authorized to add organism")
            exit(-1)
        organism = json.loads(p)
        organism_id = organism['id']
        self.logger.debug("A new organism %s has been added to Apollo instance", p)
        return organism_id
        
    
    