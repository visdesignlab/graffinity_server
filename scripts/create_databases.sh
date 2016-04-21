#!/usr/bin/env bash
# modified from https://github.com/Caleydo/pathfinder_graph/_deploy

#search for the right parent directory such that we have a common start directory
while [[ ! -f "run.sh" ]] && [[ ! -f "Vagrantfile" ]]
do
  cd ..
done

mkdir -p _data/
cd _data
basedir=`pwd`

dbprefix="/home/`whoami`/neo4j_"

function setup {
  #install_neo4j
  createdb marclab_test 7475
  createdb marclab_22jan16 7474
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
    echo ${datafile}
    echo 'Could not find file in the directory. Giving up.'
    exit
  fi

  #unzip
  mkdir -p "${db}d/data/graph.db"
  tar -xzf ${datafile} -C "${db}d/data/graph.db"

  #fix permissions
  chown -R `whoami` ${db}d/data/graph.db

  managedb ${name} start
}

function managedb {
  local name=${1:-vis}
  local db=${dbprefix}${name}
  local cmd=${2:-stop}

  (exec ${db} ${cmd})
}

setup
