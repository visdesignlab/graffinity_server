#!/usr/bin/env bash
curl -X POST -d @edge_match.json http://localhost:8000/match_edge --header Content-Type:application/json
