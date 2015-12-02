from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
u = os.environ.get('NEO4J_USERNAME')
p = os.environ.get('NEO4J_PASSWORD')

if u and p:
    authenticate(url.strip('http://'), u, p)

graph = Graph(url + '/db/data/')


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one("User", "username", self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_asset(self, name, asset_id, specs):
        user = self.find()
        asset = Asset(asset_id=asset_id)
        asset.add(user, name, specs)

    def get_assets(self):
        query = """
        MATCH (user:User)-[:OWNS]->(asset:Asset)<-[:APPLIES_TO]-(spec:Spec)
        WHERE user.username = {username}
        RETURN asset, COLLECT(spec.name) AS specs
        ORDER BY asset.asset_id DESC
        """
        return graph.cypher.execute(query, username=self.username)


class Asset:
    def __init__(self, asset_id):
        self.asset_id = asset_id

    def find(self):
        asset = graph.find_one("Asset", "asset_id", self.asset_id)
        return asset

    def add(self, user, name, specs):
        asset = self.find()
        if not asset:
            asset = Node(
                "Asset",
                id=str(uuid.uuid4()),
                name=name,
                asset_id=self.asset_id,
                timestamp=timestamp(),
                date=date()
            )
            rel = Relationship(user, "OWNS", asset)
            graph.create(rel)

            specs = [x.strip() for x in specs.split('|')]
            for t in set(specs):
                spec = graph.merge_one("Spec", "name", t)
                rel = Relationship(spec, "APPLIES_TO", asset)
                graph.create(rel)


def get_recent_assets():
    query = """
    MATCH (user:User)-[:OWNS]->(asset:Asset)<-[:APPLIES_TO]-(spec:Spec)
    RETURN user.username AS username, asset, COLLECT(spec.name) AS specs
    ORDER BY asset.timestamp DESC LIMIT 10
    """

    return graph.cypher.execute(query)


def get_asset_by_id(asset_id):
    query = """
    MATCH (user:User)-[:OWNS]->(asset:Asset)<-[:APPLIES_TO]-(spec:Spec)
    WHERE asset.asset_id = {asset_id}
    RETURN user.username AS username, asset, COLLECT(spec.name) AS specs
    """
    return graph.cypher.execute(query, asset_id=asset_id)


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%F')
