#!/usr/bin/env bash

function sedeasy {
  sed -i "s/$(echo $1 | sed -e 's/\([[\/.*]\|\]\)/\\&/g')/$(echo $2 | sed -e 's/[\/&]/\\&/g')/g" $3/conf/neo4j-server.properties
}

function clone_neo4j {
  local name=${1:-other}
  local port=${2:-7475}
  local dest=${3:-~/neo4j_${name}d}
  local datadir=${4:-data/graph.db}

  echo ${name} ${port} ${dest} ${datadir}

  basedir='/var/lib/neo4j'

  mkdir ${dest}
  mkdir ${dest}/conf

  ln -s ${basedir}/bin ${dest}
  ln -s ${basedir}/lib ${dest}
  ln -s ${basedir}/plugins ${dest}
  ln -s ${basedir}/system ${dest}

  #create config links
  ln -s ${basedir}/conf/* ${dest}/conf
  #replace the config with a new one
  rm ${dest}/conf/neo4j-server.properties
  cp ${basedir}/conf/neo4j-server.properties ${dest}/conf/neo4j-server.properties
  sedeasy 7474 ${port} ${dest}
  sedeasy "data/graph.db" "${datadir}" ${dest}
  sedeasy "https.enabled=true" "https.enabled=false" ${dest}
  sedeasy "dbms.security.auth_enabled=true" "dbms.security.auth_enabled=false" ${dest}

  mkdir ${dest}/data
  ln -s ${basedir}/data/keystore ${dest}/data

  ln -s ${dest}/bin/neo4j ~/neo4j_${name}

  echo "done start using ~/neo4j_${name} start"
}

function interactive {
  read -p "Enter id: [other]" name
  name=${name:-other}
  read -p "Enter destination: [~/neo4j_${name}d]" dest
  dest=${dest:-~/neo4j_${name}d}
  read -p "Enter port: [7475]" port
  port=${port:-7475}
  read -p "Enter data directory: [data/graph.db]" datadir
  datadir=${datadir:-data/graph.db}

  clone_neo4j ${name} ${port} ${dest} ${datadir}
}

if [ $# -eq 0 ] ; then
  interactive
else
  clone_neo4j $@
fi