#!/usr/bin/env bash
curl -X POST -d @example_hello_movies_data.json http://localhost:8000/ --header Content-Type:application/json
