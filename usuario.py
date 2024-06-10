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
        self.tipo = '0'
    #Função de Cadastor da rota /cadastrar
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
    
    #Função para puxar os chamados

    def chamados(self):
        documento = []
        
        filtro = {'autor': self.nome_completo}

        obj = coll.find(filtro)

        for doc  in obj:
            chamado = Chamado( doc['autor'], doc['descricao'], doc['local'], doc['data'], doc['situacao'], doc['tipo'])

            documento.append(chamado)

        return documento
    
    
class Sindico(Usuario):
    def __init__(self, nome_completo, documento, email, senha, telefone, endereco):
        super().__init__(nome_completo, documento, email, senha, telefone)
        self.endereco = endereco
        self.tipo = '1'
      

#Função para puxar os chamados 
    def chamados(self):
        documento = []
        
        filtro = {'campo': 'Chamado'}

        obj = coll.find(filtro)

        for doc  in obj:
            chamado = Chamado( doc['autor'], doc['descricao'], doc['local'], doc['data'], doc['situacao'], doc['tipo'])

            documento.append(chamado)

        return documento

#Tratar
    def tratar():
        return

#==========================================================================================================================
class Condominio:
    def __init__(self, nome_cond, cnpj, endereco_c):
        self.nome_cond = nome_cond
        self.cnpj = cnpj
        self.endereco_c = endereco_c


#Chamados ===========================================================================================================
class Chamado:
    def __init__(self, autor, descricao, local, data, situacao, tipo):
        self.autor = autor
        self.descricao = descricao
        self.local = local
        self.campo = 'Chamado'
        self.data = data
        self.situacao = situacao
        self.tipo = tipo
    
#Notificação referênte a solicitar
class Notificacao(Chamado):
    def __init__(self, autor, descricao, local,  data, situacao, tipo, dataprevista):
        super().__init__(autor, descricao, local, data, situacao, tipo)
        self.dataprevista = dataprevista
        self.tipo = 'Notificacao'

    def inserir(self):
        documento = {
            'autor': self.autor,
            'descricao': self.descricao,
            'local':self.local,
            'campo': self.campo,
            'data': self.data,
            'situacao': self.situacao,
            'tipo':self.tipo,
            'datapre': self.dataprevista
        }

        coll.insert_one(documento)
        return 

#Reparo referente a reparo
class Reparo(Chamado):
    def __init__(self, autor, descricao, local, data,  situacao, tipo, coordenadas):
        super().__init__(autor, descricao, local, data, situacao, tipo)
        self.cord = coordenadas
        self.tipo = 'Reparo'
    
    def inserir(self):
        document = {
            'autor': self.autor,
            'descricao': self.descricao,
            'local':self.local,
            'campo': self.campo,
            'data': self.data,
            'situacao': self.situacao,
            'tipo': self.tipo,
            'coordenadas': self.cord
        }

        coll.insert_one(document)
        
        return
#Queixa referente a formulario
class Queixa(Chamado):
    def __init__(self, autor, descricao, local, data, situacao, tipo, frequencia, responsavel):
        super().__init__(autor, descricao, local, data, situacao, tipo)
        self.responsavel = responsavel
        self.frequencia = frequencia

    def inserir(self):
        document = {
            'autor': self.autor,
            'descricao': self.descricao,
            'local':self.local,
            'campo': self.campo,
            'data': self.data,
            'situacao': self.situacao,
            'tipo': self.tipo,
            'responsavel': self.responsavel,
            'frequencia' : self.frequencia
        }

        coll.insert_one(document)

        return
#Sugestão ======================================================================================================
class Sugestao:
    def __init__(self, autor, tema, data, descricao):
        self.autor = autor
        self.tema = tema
        self.data = data
        self.descricao = descricao
        self.campo = 'sug'
    
    def inserir(self):
        documento = {
            'campo': self.campo,
            'autor': self.autor,
            'tema': self.tema,
            'data': self.data,
            'descricao': self.descricao
        }

        coll.insert_one(documento)

        return
