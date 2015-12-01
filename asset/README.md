## Usage

Make sure [Neo4j](http://neo4j.com/download/other-releases/) is running first!

Set environment variables `NEO4J_USERNAME` and `NEO4J_PASSWORD` to your username and password, respectively:

```
$ export NEO4J_USERNAME=username
$ export NEO4J_PASSWORD=password
```

Or, set `dbms.security.auth_enabled=false` in `conf/neo4j-server.properties`.

Add the export to venv in the next step is also a good way to use in development environment.

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

[http://localhost:5000](http://localhost:5000)
