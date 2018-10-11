import os

from py2neo.database import Graph

h = os.environ.get('GRAPHENEDB_HOST', 'localhost')
u = os.environ.get('NEO4J_USERNAME', 'neo4j')
p = os.environ.get('NEO4J_PASSWORD', '111111')

graph = Graph(host=h, user=u, password=p)


def query_on_constraint(constraint):
    matcher = NodeMatcher(graph)
    return graph.nodes.match('Label', Constraint=constraint).first()


def list_all():
    return list(graph.nodes.match('Label'))
