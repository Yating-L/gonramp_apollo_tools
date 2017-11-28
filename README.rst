G-OnRamp Apollo Tools
=====================

A suite of Galaxy tools for managing a local Apollo server. It includes following tools:

JBrowseHub to Apollo
--------------------

This Galaxy tool is used to create or overwrite an organism on an Apollo server with a jbrowse hub created by JBrowse Archive Creator. 

Apollo User Manager
-------------------

This Galaxy tool is used to manage Apollo users. The currently supported operation including:

  - Create a new user 
  - Delete a user
  - Add a user to a group (If the group doesn't exist, create the group)
  - Remove a user to a group

The tool can do these operations on one student at a time. It can also do the operations on multiple students at a time by uploading a text file, which including students information.

The text file can be either CSV (comma-delimited) or Tabular (tab-delimited). It should have a header line, including names for each column. Example text files: 

Text file for creating multiple users:

.. csv-table:: 
   :header: "useremail", "firstname", "lastname", "password"
   :widths: 20, 10, 10, 10

   "test1@demo.com", "test1", "demo", "1234"
   "test2@demo.com", "test2", "demo", "1234"
   "test3@demo.com", "test3", "demo", "1234"


Text file for deleting multiple users:

.. csv-table:: 
    :header: "useremail"
    :widths: 20

    "test1@demo.com"
    "test2@demo.com"
    "test3@demo.com"

Text file for adding multiple users to a group:

.. csv-table:: 
    :header: "useremail", "group"
    :widths: 20, 20

    "test1@demo.com", "Test group"
    "test2@demo.com", "Test group"
    "test3@demo.com", "Test group"

Text file for removing multiple users to a group:

.. csv-table:: 
    :header: "useremail", "group"
    :widths: 20, 20

    "test1@demo.com", "Test group"
    "test2@demo.com", "Test group"
    "test3@demo.com", "Test group"
