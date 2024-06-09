from pymongo import MongoClient, errors
from usuario import Morador, Sindico, Condominio, Sugestao, Reparo, Notificacao, QueixaSossego
from datetime import datetime
import certifi

# Conexão com o MongoDB
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

# Funções de inserção
def insert_usuario(usuario):
    db.users.insert_one({
        "UsDoc": usuario.documento,
        "UsNom": usuario.nome_completo,
        "UsEma": usuario.email,
        "UsEndereco": usuario.endereco,
        "UsTipo": usuario.tipo
    })

def insert_condominio(condominio):
    db.condominio.insert_one({
        "ConCn": condominio.cnpj,
        "NCon": condominio.nome_cond,
        "EndCon": condominio.endereco_c
    })

def insert_sugestao(sugestao):
    db.sugestao.insert_one({
        "SugTema": sugestao.tema,
        "SugData": sugestao.data,
        "SugDesc": sugestao.descricao,
        "SugDoc": sugestao.autor.documento
    })

def insert_reparo(reparo):
    db.reparo.insert_one({
        "RpLocal": reparo.local,
        "RpDescricao": reparo.descricao,
        "RpData": reparo.data,
        "RpImagemL": reparo.imagemLocal,
        "RpDocumento": reparo.autor.documento
    })

def insert_notificacao(notificacao):
    db.notificacao.insert_one({
        "NotLocal": notificacao.destinatario,
        "NotDescricao": notificacao.mensagem,
        "NotData": notificacao.data_envio,
        "NotDocumento": notificacao.remetente.documento,
        "NotDataPre": notificacao.dataprevista,
        "NotSitu": notificacao.situacao
    })

def insert_importunacao(importunacao):
    db.importunacao.insert_one({
        "ImpLocal": importunacao.local,
        "ImpDescricao": importunacao.descricao,
        "ImpData": importunacao.data,
        "ImpResponsa": importunacao.responsavel,
        "ImpDocumento": importunacao.autor.documento,
        "ImpFreque": importunacao.frequencia
    })

# Função para criar um morador
def create_morador():
    while True:
        nome_completo = input("Nome Completo: ")
        if nome_completo.replace(" ", "").isalpha() and " " in nome_completo:
            break
        else:
            print("Por favor, insira um nome completo válido.")

    documento = input("Documento (formato: 111.111.111-11): ")
    email = input("Email: ")
    senha = input("Senha: ")
    tipo = "0"
    telefone = input("Telefone (formato: 99999-9999): ")
    endereco = input("Endereço: ")

    # Criando um objeto Morador e retornando-o
    return Morador(
        nome_completo=nome_completo,
        documento=documento,
        email=email,
        senha=senha,
        tipo="0",
        telefone=telefone,
        endereco=endereco,
    )

# Função para criar um síndico
def create_sindico():
    while True:
        nome_completo = input("Nome Completo: ")
        if nome_completo.replace(" ", "").isalpha() and " " in nome_completo:
            break
        else:
            print("Por favor, insira um nome completo válido.")

    documento = input("Documento (formato: 111.111.111-11): ")
    email = input("Email: ")
    senha = input("Senha: ")
    tipo = "1"
    telefone = input("Telefone (formato: 99999-9999): ")
    endereco = input("Endereço: ")

    # Criando um objeto Sindico e retornando-o
    return Sindico(
        nome_completo=nome_completo,
        documento=documento,
        email=email,
        senha=senha,
        tipo=tipo,
        telefone=telefone,
        endereco=endereco
    )

# Função para criar um condomínio
def create_condominio():
    nome_cond = input("Nome do Condomínio: ")
    cnpj = input("CNPJ: ")
    endereco_c = input("Endereço do Condomínio: ")
    return Condominio(
        nome_cond=nome_cond,
        cnpj=cnpj,
        endereco_c=endereco_c
    )

# Função para criar uma sugestão
def create_sugestao(morador):
    tema = input("Tema da Sugestão: ")
    descricao = input("Descrição da Sugestão: ")
    data = datetime.now()
    return Sugestao(
        autor=morador,
        tema=tema,
        data=data,
        descricao=descricao
    )

# Função para criar um reparo
def create_reparo(morador):
    print("Selecione o tipo de reparo:")
    print("1. Reparo de Via")
    print("2. Limpeza")
    print("3. Reparo de Dutos")
    print("4. Queda de Fiação")
    print("5. Combate à Dengue")
    print("6. Reparo de Iluminação")

    opcao = input("Digite o número correspondente ao tipo de reparo desejado: ")
    local = input("Local do reparo: ")
    descricao = input("Descrição do reparo: ")
    data = datetime.now()

    # Perguntar se o usuário tem uma imagem para o reparo
    tem_imagem = input("Você tem uma imagem do local? (s/n): ").lower()
    imagemLocal = ""
    if tem_imagem == 's':
        imagemLocal = input("Imagem do local (caminho do arquivo): ")

    reparo_de_via = False
    limpeza = False
    reparo_de_dutos = False
    queda_de_fiacao = False
    combate_a_dengue = False
    reparo_de_iluminacao = False

    if opcao == '1':
        reparo_de_via = True
    elif opcao == '2':
        limpeza = True
    elif opcao == '3':
        reparo_de_dutos = True
    elif opcao == '4':
        queda_de_fiacao = True
    elif opcao == '5':
        combate_a_dengue = True
    elif opcao == '6':
        reparo_de_iluminacao = True
    else:
        print("Opção inválida.")
        return None

    if morador:
        return Reparo(
            autor=morador,
            local=local,
            descricao=descricao,
            data=data,
            imagemLocal=imagemLocal,
            reparo_de_via=reparo_de_via,
            limpeza=limpeza,
            reparo_de_dutos=reparo_de_dutos,
            queda_de_fiacao=queda_de_fiacao,
            combate_a_dengue=combate_a_dengue,
            reparo_de_iluminacao=reparo_de_iluminacao
        )

# Função para criar uma notificação
def create_notificacao(morador):
    destinatario = input("Digite o nome do destinatário da notificação (portaria, síndico, etc.): ")
    mensagem = input("Digite a mensagem da notificação: ")
    data_envio = datetime.now()
    dataprevista = input("Data prevista (DD-MM-AAAA): ")
    situacao = ""
    return Notificacao(
        remetente=morador,
        destinatario=destinatario,
        mensagem=mensagem,
        data_envio=data_envio,
        dataprevista=dataprevista,
        situacao=situacao
    )

# Função para criar uma queixa de importunação de sossego
def create_queixa_sossego(morador):
    local = input("Local da importunação: ")
    descricao = input("Descreva a importunação de sossego: ")
    data = datetime.now()
    responsavel = input("Nome do responsável pela importunação: ")
    frequencia = input("Frequência da importunação: ")
    return QueixaSossego(
        local=local,
        descricao=descricao,
        data=data,
        responsavel=responsavel,
        autor=morador,
        frequencia=frequencia
    )

# Menu principal
def menu_principal(morador):
    while True:
        print("\nMenu Principal:")
        print("1. Solicitar Reparo")
        print("2. Enviar Notificação")
        print("3. Enviar Sugestão")
        print("4. Registrar Queixa de Importunação de Sossego")
        print("5. Sair")

        opcao = input("Digite o número correspondente à opção desejada: ")

        if opcao == '1':
            reparo = create_reparo(morador)
            if reparo:
                insert_reparo(reparo)
                print("Reparo solicitado com sucesso!")
        elif opcao == '2':
            notificacao = create_notificacao(morador)
            insert_notificacao(notificacao)
            print("Notificação enviada com sucesso!")
        elif opcao == '3':
            sugestao = create_sugestao(morador)
            insert_sugestao(sugestao)
            print("Sugestão enviada com sucesso!")
        elif opcao == '4':
            queixa = create_queixa_sossego(morador)
            insert_importunacao(queixa)
            print("Queixa de importunação de sossego registrada com sucesso!")
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Criação de usuário e login
while True:
    print("\nSelecione uma opção:")
    print("1. Criar Morador")
    print("2. Criar Síndico")
    print("3. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")

    if opcao == '1':
        morador = create_morador()
        insert_usuario(morador)
        print("Morador criado com sucesso!")
        menu_principal(morador)
        break
    elif opcao == '2':
        sindico = create_sindico()
        insert_usuario(sindico)
        print("Síndico criado com sucesso!")
        break
    elif opcao == '3':
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
