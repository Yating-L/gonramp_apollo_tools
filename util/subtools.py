#!/usr/bin/env python

"""
This file include common used functions for converting file format to gff3
"""
from collections import OrderedDict
import json
import subprocess
import os
import sys
import tempfile
import string
import logging

class PopenError(Exception):
    def __init__(self, cmd, error, return_code):
        self.cmd = cmd
        self.error = error
        self.return_code = return_code

    def __str__(self):
        message = "The subprocess {0} has returned the error: {1}.".format(
            self.cmd, self.return_code)
        message = ','.join(
            (message, "Its error message is: {0}".format(self.error)))
        return repr(message)


def _handleExceptionAndCheckCall(array_call, **kwargs):
    """
    This class handle exceptions and call the tool.
    It maps the signature of subprocess.check_call:
    See https://docs.python.org/2/library/subprocess.html#subprocess.check_call
    """
    stdout = kwargs.get('stdout', subprocess.PIPE)
    stderr = kwargs.get('stderr', subprocess.PIPE)
    shell = kwargs.get('shell', False)
    stdin = kwargs.get('stdin', None)

    cmd = array_call[0]

    output = None
    error = None

    # TODO: Check the value of array_call and <=[0]
    logging.debug("Calling {0}:".format(cmd))
    logging.debug("%s", array_call)
    logging.debug("---------")

    # TODO: Use universal_newlines option from Popen?
    try:
        p = subprocess.Popen(array_call, stdout=stdout,
                             stderr=stderr, shell=shell, stdin=stdin)

        # TODO: Change this because of possible memory issues => https://docs.python.org/2/library/subprocess.html#subprocess.Popen.communicate

        output, error = p.communicate()

        if stdout == subprocess.PIPE:
            logging.debug("\t{0}".format(output))
        else:
            logging.debug("\tOutput in file {0}".format(stdout.name))
        # If we detect an error from the subprocess, then we raise an exception
        # TODO: Manage if we raise an exception for everything, or use CRITICAL etc... but not stop process
        # TODO: The responsability of returning a sys.exit() should not be there, but up in the app.
        if p.returncode:
            if stderr == subprocess.PIPE:
                raise PopenError(cmd, error, p.returncode)
            else:
                # TODO: To Handle properly with a design behind, if we received a option as a file for the error
                raise Exception("Error when calling {0}. Error as been logged in your file {1}. Error code: {2}"
                                .format(cmd, stderr.name, p.returncode))

    except OSError as e:
        message = "The subprocess {0} has encountered an OSError: {1}".format(
            cmd, e.strerror)
        if e.filename:
            message = '\n'.join(
                (message, ", against this file: {0}".format(e.filename)))
        logging.error(message)
        sys.exit(-1)
    except PopenError as p:
        message = "The subprocess {0} has returned the error: {1}.".format(
            p.cmd, p.return_code)
        message = '\n'.join(
            (message, "Its error message is: {0}".format(p.error)))

        logging.exception(message)

        sys.exit(p.return_code)
    except Exception as e:
        message = "The subprocess {0} has encountered an unknown error: {1}".format(
            cmd, e)
        logging.exception(message)

        sys.exit(-1)
    return p

def arrow_add_organism(organism_name, organism_dir, public=False):
    array_call = ['arrow', 'organisms', 'add_organism', organism_name, organism_dir]
    if public:
        array_call.append('--public')
    print array_call
    p = subprocess.check_output(array_call)
    return p

def arrow_create_user(user_email, firstname, lastname, password, admin=False):
    """ Create a new user of Apollo, the default user_role is "user" """
    array_call = ['arrow', 'users', 'create_user', user_email, firstname, lastname, password]
    if admin:
        array_call += ['--role', 'admin']
    logging.debug("%s", array_call)
    print array_call
    p = subprocess.check_output(array_call)
    print ("p = %s", p)
    return p

def arrow_update_organism_permissions(user_id, organism, **user_permissions):
    array_call = ['arrow', 'users', 'update_organism_permissions', str(user_id), str(organism)]
    admin = user_permissions.get("admin", False)
    write = user_permissions.get("write", False)
    read = user_permissions.get("read", False)
    export = user_permissions.get("export", False)
    if admin:
        array_call.append('--administrate')
    if write:
        array_call.append('--write')
    if read:
        array_call.append('--read')
    if export:
        array_call.append('--export')
    p = subprocess.check_output(array_call)
    return p

def arrow_get_users(user_email):
    array_call = ['arrow', 'users', 'get_users']
    logging.debug("%s", array_call)
    print array_call
    p = subprocess.check_output(array_call)
    all_users = json.loads(p)
    for d  in all_users:
        if d['username'] == user_email:
            return d['userId']
    logging.error("Cannot find user %s", user_email)

def verify_user_login(username, password):
    user_info = {'username': username, 'password': password}
    array_call = ['curl', 
                  '-b', 'cookies.txt', 
                  '-c', 'cookies.txt', 
                  '-H', 'Content-Type:application/json',
                  '-d', json.dumps(user_info),
                  'http://localhost:8080/apollo/Login?operation=login'
                  ]
    p = subprocess.check_output(array_call)
    msg = json.loads(p)
    if 'error' in msg:
        logging.error("The Authentication for user %s failed. Get error message %s", username, msg['error'])
        exit(1)
        
