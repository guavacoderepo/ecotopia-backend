# import ssl
from pymongo import MongoClient


# mongo = MongoClient('mongodb://localhost:27017')


mongo = MongoClient("mongodb+srv://guava:guava@cluster0.ukn1jcw.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
# mongo = client.get_database("Cluster0")
# mongo = MongoClient("mongodb://guava:guava@ac-mow2e6c-shard-00-00.ukn1jcw.mongodb.net:27017,ac-mow2e6c-shard-00-01.ukn1jcw.mongodb.net:27017,ac-mow2e6c-shard-00-02.ukn1jcw.mongodb.net:27017/?ssl=true&replicaSet=atlas-qthnpq-shard-0&authSource=admin&retryWrites=true&w=majority")
