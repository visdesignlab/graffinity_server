{
  "query": "MATCH p = (a:Actor)-[*1..4]-(d:Director) WHERE a.name in ['Claude Jade', 'Woody Allen', 'Samuel L. Jackson', 'Clint Eastwood', 'Armin Mueller-Stahl', 'Robert De Niro', 'Marisa Mell', 'Gérard Depardieu', 'Russ Meyer'] AND d.name in ['Woody Allen', 'Clint Eastwood', 'Jackie Chan', 'Robert De Niro', 'Gérard Depardieu', 'Dennis Hopper', 'Danny DeVito','Steve Buscemi'] return p limit 1000;"
  "graph_name": "movies"
}
