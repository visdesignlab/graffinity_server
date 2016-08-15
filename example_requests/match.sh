#!/usr/bin/env bash
curl -X POST -d @flights_match.json http://localhost:8000/match --header Content-Type:application/json
