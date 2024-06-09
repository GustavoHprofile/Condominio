from pymongo import MongoClient, errors
import certifi

# Configurações de conexão
user = "gustavoprofile762"
senha = "p2rraSit3"
url = f"mongodb+srv://{user}:{senha}@conddb.9svvseo.mongodb.net/CondDb?retryWrites=true&w=majority"

try:
    client = MongoClient(
        url,
        tls=True,
        tlsAllowInvalidCertificates=False,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000
    )
    db = client['CondDb']
    coll = db['Cond']
    client.server_info()  # Força uma chamada para verificar a conexão
    print("Conexão bem-sucedida ao MongoDB")
except errors.ServerSelectionTimeoutError as err:
    print(f"Erro ao conectar ao MongoDB: {err}")
    exit()
except Exception as e:
    print(f"Outro erro ocorreu: {e}")
    exit()

# Teste de inserção de documento
try:
    test_doc = {
        'Document': '23898128808',
        'Nome': 'Gustavo Henrique dos Santos',
        'Email': 'guga@gmail.com',
        'Endereco': 'Rua Uruguai',
        'Tipo': '0'
    }
    result = coll.insert_one(test_doc)
    print(f"Documento inserido com _id: {result.inserted_id}")
except Exception as e:
    print(f"Erro ao inserir documento: {e}")
