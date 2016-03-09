"""Runs a local server."""
from connectivity_matrix_server import app

app.debug = True
app.run(host='0.0.0.0', port=8000)


