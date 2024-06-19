from flask import Flask, render_template, request, redirect, url_for, current_app,  jsonify
from usuario import Morador, Notificacao, Reparo, Sugestao, Sindico, Queixa
from pymongo import MongoClient, errors
import certifi
from datetime import datetime
from bson.objectid import ObjectId

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


    
app = Flask(__name__)
app.config['logado'] = False
app.config['reparos'] = False

#NODE
@app.route('/receive-date', methods=['POST'])
def receive_date():
    data = request.get_json()
    received_date = data.get('date')
    print(f"Data recebida: {received_date}")

    # Processar a data conforme necessário
    # ...

    return jsonify({"status": "success", "received_date": received_date})

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Função para logar 
@app.route('/log', methods=['POST'])
def log():
    login = request.form.get('login')
    senha = request.form.get('senha')
    
    filtro = {'UsEma': login}

    documento = coll.find_one(filtro)
    
    if (documento is not None and senha == documento['UsSenha']):

        #tipo de usuário
        if(documento['UsTipo'] == '1'):
            usuario = Sindico(documento['UsNom'], documento['UsDoc'], documento['UsEma'], documento['UsSenha'], documento['UsTelefone'], documento['_id'], documento['UsEndereco'])

            current_app.config['logado'] = usuario
            usu = current_app.config['logado']

            if(usu.chamados()):
                chamados = usu.chamados()
                return render_template('chamados.html', usu = usu, chamados = chamados)
            else:
                return render_template('home.html', usu=usu)    
        else:
            usuario = Morador(documento['UsNom'], documento['UsDoc'], documento['UsEma'], documento['UsSenha'], documento['UsTelefone'], documento['_id'], documento['UsEndereco'])
            current_app.config['logado'] = usuario
            return render_template('home.html', usu = usuario)
    else:
        return render_template('index.html')
# Log Out 
@app.route('/logout')
def logout():
    current_app.config['logado'] = False
    return render_template('index.html')


#Páginas
@app.route('/home')
def home():
    if current_app.config['logado'] != False:
        usu = current_app.config['logado']
        return render_template('home.html',usu = usu)
    else:
        return render_template('index.html')

 
# Rota para cadastrar um novo usuário
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome_completo = request.form.get('nome_completo')
        documento = request.form.get('documento')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        idU = ''

        usuario = Morador(nome_completo, documento, email, senha, telefone, idU, endereco)

        cad = usuario.cadastrar()

        return redirect(url_for('home'))
    return render_template('cadastrar.html')


@app.route('/chamados')
def listar_chamados():
    if current_app.config['logado'] != False:
        usu = current_app.config['logado']
        chamados = usu.chamados()
        if(chamados != 'nenhum'):
            return render_template('chamados.html', usu = usu, chamados = chamados)
        else:
            return render_template('home.html', usu=usu)    
    else:
        return render_template('index.html')


@app.route('/formulario')
def formulario():
    if(current_app.config['logado'] != False):
        usu = current_app.config['logado']
        chamado = ''
        return render_template('formulario.html', usu = usu, chamado = chamado)
    else:
        return render_template('index.html')
    
@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')
    

#ROTAS DO REPARO =============================================================================================================
@app.route('/dutos')
def dutos():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Reparo de Dutos'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')
    
@app.route('/ilum')
def ilum():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Reparo na Iluminação'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')

@app.route('/limp')
def limp():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Limpeza'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')

@app.route('/other')
def other():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Outros'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')

@app.route('/via')
def via():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Reparo na via'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')

@app.route('/fia')
def fia():
    if(current_app.config['logado'] != False):
        Tipochamado = 'Reparo na Fiação'
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html', usu = usu, Tipochamado = Tipochamado, chamado = chamado)
    else:
        return render_template('index.html')


#===================================================================================================================
@app.route('/reparo')
def reparo():
    if(current_app.config['logado'] != False):
        usu = current_app.config['logado'] 
        chamado = ''
        return render_template('reparo.html',usu = usu, chamado = chamado)
    else:
        return render_template('index.html')
    
@app.route('/sugestao')
def sugestao():
    if(current_app.config['logado'] != False):
        usu = current_app.config['logado']
        chamado = ''
        return render_template('sugestao.html', usu = usu, chamado = chamado)
    else:
        return render_template('index.html')

#NOTIFICAÇÃO
@app.route('/solicitar')
def solicitar():
    if(current_app.config['logado'] != False):
        usu = current_app.config['logado']
        chamado = ''
        return render_template('solicitar.html', usu = usu, chamado = chamado)
    else:
        return render_template('index.html')

@app.route('/excluir.html')
def excluir():
    if(current_app.config['logado'] != False):
        return render_template('excluir.html', nome = current_app.config['logado']['UsNom'], email = current_app.config['logado']['UsEma'], endereco = current_app.config['logado']['UsEndereco'], tel = current_app.config['logado']['UsTelefone'])
    else:
        return render_template('index.html')


#inserir chamados ===============================================================================================

#NOTIFICAÇÕES
@app.route('/noti',  methods=['GET', 'POST'])
def noti():
    usu = current_app.config['logado']
    if request.method == 'POST':
        descricao = request.form.get('descricao')
        local = request.form.get('local')
        dataprevista = request.form.get('dataprevista')
        autor = request.form.get('autor')
        data = 'hoje'
        situacao = 'Não Tratado'
        tipo = 'tubulacao'
        feedback = ''
        idC = ''
        
        solicitar = Notificacao( autor, descricao, local, data, situacao, tipo, feedback, idC, dataprevista)
        solicitar.inserir()

        return redirect(url_for('home'))
    return render_template('home.html',usu)

#REPAROS
@app.route('/rep', methods=['GET', 'POST'])
def rep():
    usu = current_app.config['logado']
    if request.method == 'POST':
        autor = request.form.get('autor')
        descricao = request.form.get('descricao')
        local = request.form.get('local')
        coordenadas = request.form.get('coordenadas')
        data = 'hoje'
        situacao = 'Não Tratado'
        tipo = ''
        feedback = ''
        idC = ''

        
        obj = Reparo(autor, descricao, local, data,  situacao, tipo, feedback, idC, coordenadas)

        obj.inserir()

        return redirect(url_for('home'))
    return render_template('home.html', usu = usu)

#QUEIXA
@app.route('/que', methods=['GET', 'POST'])
def que():
    usu = current_app.config['logado']
    if request.method == 'POST':
        autor = request.form.get('autor')
        descricao = request.form.get('descricao')
        local = request.form.get('local')
        data = request.form.get('data')
        frequencia = request.form.get('freq')
        responsavel = request.form.get('resp')
        situacao = 'Não Tratado'
        tipo = 'Queixa'
        feedback = ''
        idC = ''

        obj = Queixa(autor, descricao, local, data, situacao, tipo, feedback, idC,  frequencia, responsavel) 

        obj.inserir()

        return redirect(url_for('home'))
    return render_template('home.html', usu = usu)

#SUGESTÃO

@app.route('/sug', methods=['GET', 'POST'])
def sug():
    usu = current_app.config['logado']
    if request.method == 'POST':
        autor = usu.nome_completo
        tema = request.form.get('tema')
        data = request.form.get('data')
        descri = request.form.get('desc') 
        idG = ''
        sugestao = Sugestao(autor, tema, data, descri, idG)

        sugestao.inserir()

        return redirect(url_for('home'))
    
#TRATAR/EDITAR===============================================================================================================================
@app.route('/Notificacao')
def notificacao():
    idC = request.args.get('var')
    doc = ObjectId(idC)
    filtro = {'_id':doc}
    documento = coll.find_one(filtro)

    chamado = Notificacao(documento['autor'], documento['descricao'], documento['local'],documento['data'], documento['situacao'], documento['tipo'], documento['feedback'], documento['_id'], documento['datapre'])
    usu = current_app.config['logado']
    return render_template('solicitar.html', usu = usu, chamado = chamado)

@app.route('/Queixa')
def Que():
    idC = request.args.get('var')
    doc = ObjectId(idC)
    filtro = {'_id':doc}
    documento = coll.find_one(filtro)

    chamado = Queixa(documento['autor'], documento['descricao'], documento['local'], documento['data'], documento['situacao'], documento['tipo'], documento['feedback'], documento['_id'],  documento['frequencia'], documento['responsavel']) 
    usu = current_app.config['logado']
    return render_template('formulario.html', usu = usu, chamado = chamado)

@app.route('/Reparo')
def Repair():
    idC = request.args.get('var')
    doc = ObjectId(idC)
    filtro = {'_id':doc}
    documento = coll.find_one(filtro)

    chamado = Reparo(documento['autor'], documento['descricao'], documento['local'], documento['data'], documento['situacao'], documento['tipo'], documento['feedback'], documento['_id'], documento['coordenadas']) 
                                                    
    usu = current_app.config['logado']
    return render_template('reparo.html', usu = usu, chamado = chamado)

#TRATAMENTO 
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if request.method == 'POST':
        idC = request.form.get('idC')
        feed = request.form.get('feedback')
        situ = request.form.get('situ')

        modifica = {
            "$set": {
                'feedback': feed,
                'situacao': situ
            }
        }

        identificacao = ObjectId(idC)

        filtro = {'_id': identificacao}

        mod = coll.update_one(filtro, modifica)
    usu = current_app.config['logado']
    chamados = usu.chamados()
    return render_template('chamados.html', usu = usu, chamados = chamados)
if __name__ == '__main__':
    app.run(debug=True)