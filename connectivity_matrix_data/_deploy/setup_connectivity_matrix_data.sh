#!/usr/bin/env bash

#search for the right parent directory such that we have a common start directory
while [[ ! -f "run.sh" ]] && [[ ! -f "Vagrantfile" ]]
do
  cd ..
done

function install_neo4j {
  ##########################
  # neo4j
  # following debian.neo4j.org

  if [ $(dpkg-query -W -f='${Status}' neo4j 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    #neo4j add to packages
    wget -O - http://debian.neo4j.org/neotechnology.gpg.key| sudo apt-key add - # Import our signing key
    echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list # Create an Apt sources.list file

    sudo apt-get update
    sudo apt-get install -y neo4j

    #TODO change the neo4j-server.properties e.g using grep or sed
    #listens to all connections even from outside by uncomenting a config line
    sudo sed -i '/^#.*0.0.0.0/s/^#//' /etc/neo4j/neo4j-server.properties
    #disable authorization by default
    sudo sed -i '/dbms.security.auth_enabled=true/s/dbms.security.auth_enabled=false/' /etc/neo4j/neo4j-server.properties
    #stop server:
    sudo service neo4j-service stop
    #access the browser interface via: http://localhost:7474/

    #disable autostart
    sudo update-rc.d -f neo4j-service disable
  else
    echo "neo4j already installed"
  fi
}


mkdir -p _data/
cd _data
basedir=`pwd`

baseurl="https://googledrive.com/host/0B9R1KaxZIq6UQVQ2V2NTdzYwY00/"
#baseurl="https://googledrive.com/host/0B7lah7E3BqlAfmNnQ3ptNUhtbG1fWklkemVGc0xnZkNyZ21lUi15aFlIb3NSZ2FWOTR3NHM/"
#pluginname="neo4j-k-shortest-paths-plugin-2.2.3-SNAPSHOT.jar"

dbprefix="/home/`whoami`/neo4j_"

function sedeasy {
  sed -i "s/$(echo $1 | sed -e 's/\([[\/.*]\|\]\)/\\&/g')/$(echo $2 | sed -e 's/[\/&]/\\&/g')/g" $3
}

#function fixplugin {
#  local dbdir=$1
#  if [ ! -e ${pluginname} ] ; then
#    #download if not existing
#    wget --timestamping -O ${pluginname} "${baseurl}/${pluginname}"
#  fi

  #create the link to the plugin itself
#  if [ ! -e "${dbdir}/plugins/${pluginname}" ] ; then
#    #remove the shared link and create a real one
#    rm -r ${dbdir}/plugins
#    mkdir -p ${dbdir}/plugins
#    ln -s "${basedir}/${pluginname}" "${dbdir}/plugins/"
#  fi

  #change the config file
#  sedeasy "#org.neo4j.server.thirdparty_jaxrs_classes=org.neo4j.examples.server.unmanaged=/examples/unmanaged" "org.neo4j.server.thirdparty_jaxrs_classes=org.caleydo.neo4j.plugins.kshortestpaths=/caleydo" ${dbdir}/conf/neo4j-server.properties
#}

function updateplugin {
  #download if not existing
  wget --timestamping -O ${pluginname} "${baseurl}/${pluginname}"
}

function createdb {
  local name=${1:-vis}
  local port=${2:-7475}
  local db=${dbprefix}${name}
  if [ -d ${db}d ] ; then
    return 0
  fi
  #clone db
  ../scripts/clone_neo4j.sh ${name} ${port}
  
  #fix plugin setting
  #fixplugin ${db}d

  #download the data
  local datafile="neo4j_${name}.tar.gz"
  if [ ! -e ${datafile} ] ; then
    #download if not existing
    wget -O ${datafile} "${baseurl}/${datafile}"
  fi
  #unzip
  mkdir -p "${db}d/data/graph.db"
  tar -xzf ${datafile} -C "${db}d/data/graph.db"
  #fix permissions
  chown -R `whoami` ${db}d/data/graph.db

  managedb ${name} start
}

function updatedb {
  local name=${1:-vis}
  local db=${dbprefix}${name}

  managedb ${name} stop

  #download the data
  local datafile="neo4j_${name}.tar.gz"
  #download if not existing
  wget --timestamping -O ${datafile} "${baseurl}/${datafile}"
  #unzip
  rm -r "${db}d/data/graph.db"
  mkdir -p "${db}d/data/graph.db"
  tar -xzf ${datafile} -C "${db}d/data/graph.db"
  #fix permissions
  chown -R `whoami` ${db}d/data/graph.db

  managedb ${name} start
}

function exportdb {


  local name=${1:-vis}
  local db=${dbprefix}${name}
  local datafile="neo4j_${name}.tar.gz"
#  managedb ${1} stop

  local dataDir=$(pwd)
  cd "${db}d/data/graph.db/"
  tar -zcvf ${datafile} *
  mv ${datafile} "${dataDir}/${datafile}"

}
function managedb {
  local name=${1:-vis}
  local db=${dbprefix}${name}
  local cmd=${2:-stop}

  (exec ${db} ${cmd})
}

function uninstalldb {
  local name=${1:-vis}
  local db=${dbprefix}${name}

  managedb ${name} stop
  rm -rf ${db}d
}

function setup {
  install_neo4j
  createdb marclab_test 7474
}

function update {
  updateplugin
  managedb marclab_test restart
}

function uninstall {
#  uninstalldb dblp
#  uninstalldb pathways
#  uninstalldb dot
  uninstalldb marclab_test

  #remove plugin
  rm -f "${baseurl}/${pluginname}"
}

#command switch
case "$1" in
update)
  update
  ;;
uninstall)
  uninstall
  ;;
updatedb)
  shift
  updatedb $@
  ;;
exportdb)
  shift
  exportdb $@
  ;;
createdb)
  shift
  createdb $@
  ;;
*)
  setup
  ;;
esac
