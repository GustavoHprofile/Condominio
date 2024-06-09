from flask import Flask, render_template, request, redirect, url_for, current_app,  jsonify
from usuario import Morador, Notificacao, Reparo, Sugestao
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

# Função para inserir usuário no MongoDB
def insert_usuario(usuario):
    coll.insert_one({
        "UsDoc": usuario.documento,
        "UsNom": usuario.nome_completo,
        "UsEma": usuario.email,
        "UsSenha": usuario.senha,
        "UsEndereco": usuario.endereco,
        "UsTipo": usuario.tipo,
        "UsTelefone": usuario.telefone
    })

# Função para inserir notificação no MongoDB
def insert_notificacao(notificacao):
    coll.insert_one({
        "Campo":"Chamado",
        "NomeT": "Notificacao",
        "Autor":notificacao['autor'],
        "Local": notificacao['local'],
        "Descricao": notificacao['descricao'],
        "Data": notificacao['data'],
        "DataPre": notificacao['datapre'],
        "Situ": notificacao['situ']
    })

# Função para inserir reparo no MongoDB
def insert_reparo(reparo):
    coll.insert_one({
        "Campo":"Chamado",
        "NomeT": "Reparo",
        "Tipo":reparo.tipo,
        "Cod":reparo.cord,  
        "Situ":reparo.situ,
        "Local": reparo.local,
        "Descricao": reparo.descricao,
        "Data": reparo.data,
        "Autor": reparo.autor
    })
#Função para inserir sugestões no MongoDB
def insert_queixa(sugestao):
    coll.insert_one({
        "Campo":"Chamado",
        "NomeT":"Queixa",
        "Autor":sugestao.autor,
        "Tema":sugestao.tema,
        "Data":sugestao.data,
        "Descricao":sugestao.descricao
    })
#Função para inserir Queixas 
def insert_sugestoes(sugestao):
    coll.insert_one({
        "Campo":"Chamado",
        "NomeT":"Sugestão",
        "Autor":sugestao.autor,
        "Tema":sugestao.tema,
        "Data":sugestao.data,
        "Descricao":sugestao.descricao
})
    
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

    if documento is not None and senha == documento['UsSenha']:
        current_app.config['logado'] = documento
        if documento['UsTipo'] == '1':
            return redirect(url_for('listar_chamados'))
        else:
            return redirect(url_for('home'))
        
# Log Out 
@app.route('/logout')
def logout():
    current_app.config['logado'] = False
    return render_template('index.html')

@app.route('/home')
def home():
    if current_app.config['logado'] != False:
        return render_template('home.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'])
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

        usuario = Morador(
            nome_completo=nome_completo,
            documento=documento,
            email=email,
            senha=senha,
            tipo="0",
            telefone=telefone,
            endereco=endereco
        )

        insert_usuario(usuario)

        return redirect(url_for('home'))  # Redireciona para a página inicial após criar o cadastro

    return render_template('cadastrar.html')

@app.route('/chamados')
def listar_chamados():
    if current_app.config['logado'] != False:
        if current_app.config['logado']['UsTipo'] == 0:
            autor = current_app.config['logado']['UsDoc']
            filtro = {'Autor':autor}
        else:
            filtro = {'Campo':'Chamado'}
        chamado = coll.find(filtro)
        chamados = []
        for document in chamado:
            doc = {
                'Autor':document['Autor'],
                'Descricao':document['Descricao'],
                'Local':document['Local'],
                'Data':document['Data'],
                'NomeT':document['NomeT'],
                'Situ':document['Situ']
            }
            chamados.append(doc)
        return render_template('chamados.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'], chamados=chamados)
    else:
        return render_template('index.html')


@app.route('/formulario')
def formulario():
    if(current_app.config['logado'] != False):
        return render_template('formulario.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'])
    else:
        return render_template('index.html')
    
@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

       
    
@app.route('/reparo')
def reparo():
    if(current_app.config['logado'] != False):
        if(current_app.config['logado']['UsTipo'] == 0):
            filtro = {'UsDoc':current_app.config['logado']['UsDoc']}

            rps = coll.find(filtro)
            return render_template('reparo.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'], rps=rps)
        else:
            rps = coll.find()
            return render_template('reparo.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'], rps=rps)
    else:
        return render_template('index.html')

@app.route('/excluir.html')
def excluir():
    if(current_app.config['logado'] != False):
        return render_template('excluir.html', nome=current_app.config['logado']['UsNom'], email=current_app.config['logado']['UsEma'], endereco=current_app.config['logado']['UsEndereco'], tel=current_app.config['logado']['UsTelefone'])
    else:
        return render_template('index.html')

# Rota para solicitar uma nova notificação

@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar():
    if(current_app.config['logado'] != False):
        if request.method == 'POST':
            local = request.form.get('local')
            descricao = request.form.get('mensagem')
            dataprevista = request.form.get('dataprevista')
            autor = current_app.config['logado']['UsDoc']
            data='hoje'
            situacao = ""

            notificacao = {
                        "Campo":"Chamado",
                        "NomeT": "Notificacao",
                        'Autor':autor, 
                        'Local' : local, 
                        'Descricao' : descricao, 
                        'Data' : data, 
                        'DataPre' : dataprevista, 
                        'Situ': situacao
                        }
            coll.insert_one(notificacao)
            return redirect(url_for('home'))  # Redireciona para a página inicial após criar a notificação

    return render_template('solicitar.html')

@app.route('/sugestao', methods=['GET', 'POST'])
def sugestao():
    if request.method == 'POST':
        tema = request.form.get('destinatario')
        descricao = request.form.get('mensagem')
        data = request.form.get('dataprevista')

        autor = current_app.config['logado']['UsDoc']
        notificacao = Sugestao(autor, tema, data, descricao)
        insert_sugestoes(notificacao)
        return redirect(url_for('home'))  # Redireciona para a página inicial após criar a notificação

    return render_template('sugestao.html')

# Rota para relatar uma queixa de sossego
@app.route('/formulario', methods=['GET', 'POST'])
def queixasossego():
    if request.method == 'POST':
        tema = request.form.get('destinatario')
        descricao = request.form.get('mensagem')
        data = request.form.get('dataprevista')

        autor = current_app.config['logado']['UsDoc']
        notificacao = Sugestao(autor, tema, data, descricao)
        insert_queixa(notificacao)
        return redirect(url_for('home'))  
    
    return render_template('sugestao.html')

@app.route('/reparo', methods=['GET', 'POST'])
def duto():
    if(current_app.config['logado']!=False):
        if request.method == 'POST':
            local = request.form.get('local')
            descricao = request.form.get('mensagem')
            cordenada = request.form.get('coordenadas')
            tipo="Tubulação"
            situ = ""
            data = datetime.now()

            # Supondo que o autor seja o usuário logado
            autor = current_app.config['logado']['UsDoc'] 
            
            reparo = Reparo(local, descricao, data, autor, situ, tipo, cordenada)

            insert_reparo(reparo)
        return redirect(url_for('home'))  # Redireciona para a página inicial após criar o reparo

    return render_template('reparo.html')


if __name__ == '__main__':
    app.run(debug=True)
