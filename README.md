# connectivity_matrix_server


## Apache2 setup
- install apache2 with modwsgi
- make symlink to connectivity_matrix_server folder in /var/www
- make symlink to connectivity_matrix.conf in /etc/apache2/sites-available
- make the site available - `sudo a2ensite connectivity_matrix.conf`
- edit /etc/apache2/ports.conf - add the line `Listen 8000`
- restart apache2 service