from pymongo import MongoClient
import certifi

user = "gustavoprofile762"
senha = "p2rraSit3"
url = f"mongodb+srv://{user}:{senha}@conddb.9svvseo.mongodb.net/CondDb?retryWrites=true&w=majority"

client = MongoClient(url)

db = client['CondDb']
coll = db['Cond']

filtro = {'email':'guga@gmail.com'}

for document in coll.find():
    print(document)