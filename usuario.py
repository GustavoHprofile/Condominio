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
    def __init__(self, nome_completo, documento, email, senha, telefone, idU):
        self.nome_completo = nome_completo
        self.documento = documento
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.id = idU

    def cadastrar(self):
        document = {
            'UsDoc': self.documento,
            'UsNom': self.nome_completo,
            'UsEma': self.email,
            'UsSenha' : self.senha,
            'UsEndereco' : '',
            'UsTelefone' : self.telefone
        }
    
    def modificar(self):
        mod = {
            '$set':{
                'UsEma':self.email,
                'UsSenha':self.senha,
                'UsTelefone':self.telefone
            }
        }

        filtro = {'_id':self.id}

        modificacao = coll.update_one(filtro, mod)

        return

        

class Morador(Usuario):
    def __init__(self, nome_completo, documento, email, senha, telefone, idU, endereco):
        super().__init__(nome_completo, documento, email, senha, telefone, idU)
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
            'UsTipo' : '4',
            'UsTelefone' : self.telefone
        }

        coll.insert_one(document)
        return
    
    #Função para puxar os chamados

    def chamados(self):
        documento = []
        
        filtro = {'autor': self.nome_completo}
        
        contagem = coll.count_documents(filtro and {'campo':'Chamado'})

        if contagem == 0:
            documento = 'nenhum'
        else:
            obj = coll.find(filtro and {'campo':'Chamado'})
            for doc  in obj:
                chamado = Chamado( doc['autor'], doc['descricao'], doc['local'], doc['data'], doc['situacao'], doc['tipo'], doc['feedback'], doc['_id'])

                documento.append(chamado)

        return documento
    
    
class Sindico(Usuario):
    def __init__(self, nome_completo, documento, email, senha, telefone, idU, endereco):
        super().__init__(nome_completo, documento, email, senha, telefone, idU)
        self.endereco = endereco
        self.tipo = '1'
      

#Função para puxar os chamados 
    def chamados(self):
        documento = []
        
        filtro = {'campo': 'Chamado'}

        contagem = coll.count_documents(filtro)

        if contagem == 0:
            documento = 'nenhum'
        else:
            obj = coll.find(filtro)
            for doc  in obj:
                chamado = Chamado( doc['autor'], doc['descricao'], doc['local'], doc['data'], doc['situacao'], doc['tipo'], doc['feedback'], doc['_id'])

                documento.append(chamado)

        return documento

#Tratar
    def consultar(self):
        perfis  = []
        
        filtro = {'UsTipo':'4'}
        consulta = coll.count_documents(filtro)
        if consulta >= 1:
            consulta = coll.find(filtro)
            for doc in consulta:
                morador = Morador(doc['UsNom'], doc['UsDoc'], doc['UsEma'], doc['UsSenha'], doc['UsTelefone'], doc['_id'], doc['UsEndereco'])
                perfis.append(morador)
        else:
            perfis = ''
        return perfis

#==========================================================================================================================
class Condominio:
    def __init__(self, nome_cond, cnpj, endereco_c):
        self.nome_cond = nome_cond
        self.cnpj = cnpj
        self.endereco_c = endereco_c


#Chamados ===========================================================================================================
class Chamado:
    def __init__(self, autor, descricao, local, data, situacao, tipo, feedback, idC):
        self.autor = autor
        self.descricao = descricao
        self.local = local
        self.campo = 'Chamado'
        self.data = data
        self.situacao = situacao
        self.tipo = tipo
        self.feedback = feedback
        self.id = idC
    
#Notificação referênte a solicitar
class Notificacao(Chamado):
    def __init__(self, autor, descricao, local,  data, situacao, tipo, feedback, idC, dataprevista):
        super().__init__(autor, descricao, local, data, situacao, tipo, feedback, idC)
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
            'feedback':self.feedback,
            'datapre': self.dataprevista
        }

        coll.insert_one(documento)
        return 

#Reparo referente a reparo
class Reparo(Chamado):
    def __init__(self, autor, descricao, local, data,  situacao, tipo, feedback, idC, coordenadas):
        super().__init__(autor, descricao, local, data, situacao, tipo, feedback, idC)
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
            'feedback':self.feedback,
            'coordenadas': self.cord
        }

        coll.insert_one(document)
        
        return
#Queixa referente a formulario
class Queixa(Chamado):
    def __init__(self, autor, descricao, local, data, situacao, tipo, frequencia, feedback, idC, responsavel):
        super().__init__(autor, descricao, local, data, situacao, tipo, feedback, idC)
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
            'feedback':self.feedback,
            'responsavel': self.responsavel,
            'frequencia' : self.frequencia
        }

        coll.insert_one(document)

        return
#Sugestão  referente a sugestão======================================================================================================
class Sugestao:
    def __init__(self, autor, tema, data, descricao, idG):
        self.autor = autor
        self.tema = tema
        self.data = data
        self.descricao = descricao
        self.campo = 'sug'
        self.id = idG
    
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
