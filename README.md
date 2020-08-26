# Graffinity Server

This project contains server-side functions for [Graffinity](http://github.com/visdesignlab/graffinity), prototype software for visualizing connectivity relationships in large graphs. 

This project contains the necessary files to launch a virtual machine using Vagrant, install dependencies on that machine, and ultimately configure Neo4j databases for use with Graffinity.

# Setup 

These directions are for setting up the Graffinity Server for local development and testing. It requires that you use Vagrant. I developed it with Vagrant 1.8.5, though newer versions might also work. You will also need to have the git lfs extension installed before cloning this repository.

1. Clone this repository
1. Cd into the directory
1. Make sure that the git lfs files are downloaded and checked out in the _data directory using `git lfs fetch` and `git lfs checkout`
1. Run `vagrant up` to create a new virtual machine and automatically configure it for Graffinity (this will take a while)
1. Run `vagrant ssh`to connect to the machine
1. In the virtual machine, launch the script `python /vagrant/run_server.py` to start the Graffinity application
1. Back on your host machine, run files in the example_scripts directory to test the server

# Deploying with apache2

1. Install apache2 with modwsgi
1. Make symlink to connectivity_matrix_server folder in /var/www
1. Make symlink to connectivity_matrix.conf in /etc/apache2/sites-available
1. Make the site available - `sudo a2ensite connectivity_matrix.conf`
1. Edit /etc/apache2/ports.conf - add the line `Listen 8000`
1. Restart apache2 service
