#!/usr/bin/python

import os

class ApolloUser(object):
    def __init__(self, user_email, password, firstname=None, lastname=None):
        self.user_email = user_email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
