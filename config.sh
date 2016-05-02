wget -O - https://debian.neo4j.org/neotechnology.gpg.key | apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' >/tmp/neo4j.list
mv /tmp/neo4j.list /etc/apt/sources.list.d
apt-get -qqy update
apt-get -qqy install neo4j=2.3.2
apt-get -qqy install python-flask
apt-get -qqy install python-pip
apt-get -qqy install git
pip install Flask-WTF
pip install Flask-RESTful
pip install Flask-ReqArgs
pip install json
pip install Flask-Cors
pip install py2neo
