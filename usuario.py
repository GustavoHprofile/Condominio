from flask import Flask, render_template, request, redirect, url_for, current_app,  jsonify
from pymongo import MongoClient, errors
import certifi
from datetime import datetime


# Conexão com o MongoDB
user = "gustavoprofile762"
senha = "p2rraSit3"
url = f"mongodb+srv://{user}:{senha}@conddb.9svvseo.mongodb.net/?retryWrites=true&w=majority&appName=CondDb"

try:
    client = MongoClient(url,
        tls=True,
        tlsAllowInvalidCertificates=False,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000
        )
    db = client['CondDb']
    coll = db['Cond']
    client.server_info()
    print("Conexão bem-sucedida ao MongoDB")
except errors.ServerSelectionTimeoutError as err:
    print(f"Erro ao conectar ao MongoDB: {err}")
    exit()
except Exception as e:
    print(f"Outro erro ocorreu: {e}")
    exit()


#Classes
class Usuario:
    def __init__(self, nome_completo, documento, email, senha, telefone):
        self.nome_completo = nome_completo
        self.documento = documento
        self.email = email
        self.senha = senha
        self.telefone = telefone

    def cadastrar(self):
        document = {
            'UsDoc': self.documento,
            'UsNom': self.nome_completo,
            'UsEma': self.email,
            'UsSenha' : self.senha,
            'UsEndereco' : '',
            'UsTelefone' : self.telefone
        }

        

class Morador(Usuario):
    def __init__(self, nome_completo, documento, email, senha, telefone, endereco):
        super().__init__(nome_completo, documento, email, senha, telefone)
        self.endereco = endereco
    def cadastrar(self):
        document = {
            'UsDoc': self.documento,
            'UsNom': self.nome_completo,
            'UsEma': self.email,
            'UsSenha' : self.senha,
            'UsEndereco' : self.endereco,
            'UsTipo' : '0',
            'UsTelefone' : self.telefone
        }

        coll.insert_one(document)

        return 
       
class Sindico(Usuario):
    def __init__(self, nome_completo, documento, email, senha, telefone, endereco):
        super().__init__(nome_completo, documento, email, senha, telefone)
        self.endereco = endereco
    def cadastrar(self):
        document = {
            'UsDoc': self.documento,
            'UsNom': self.nome_completo,
            'UsEma': self.email,
            'UsSenha' : self.senha,
            'UsEndereco' : '',
            'UsTipo' : '1',
            'UsTelefone' : self.telefone
        }

        if(coll.insert_one(document)):
            return 'ok'
        else:
            return 'nok'

class Condominio:
    def __init__(self, nome_cond, cnpj, endereco_c):
        self.nome_cond = nome_cond
        self.cnpj = cnpj
        self.endereco_c = endereco_c

class Sugestao:
    def __init__(self, autor, tema, data, descricao):
        self.autor = autor
        self.tema = tema
        self.data = data
        self.descricao = descricao

class Notificacao:
    def __init__(self, mensagem, data, dataprevista, situacao, autor, local):
        self.autor = autor,
        self.mensagem = mensagem
        self.data = data
        self.dataprevista = dataprevista
        self.situacao = situacao
        self.local = local
        
class Reparo:
    def __init__(self, local, descricao, data, autor, situ, tipo, cordenadas):
        self.local = local
        self.descricao = descricao
        self.cord = cordenadas
        self.data = data
        self.autor = autor
        self.tipo = tipo 
        self.situ = situ
        

class QueixaSossego:
    def __init__(self, local, descricao, data, responsavel, autor, frequencia):
        self.local = local
        self.descricao = descricao
        self.data = data
        self.responsavel = responsavel
        self.autor = autor
        self.frequencia = frequencia
