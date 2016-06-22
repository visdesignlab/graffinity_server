#!/usr/bin/env bash
curl -X POST -d @bad_data.json http://localhost:8000/ --header Content-Type:application/json
