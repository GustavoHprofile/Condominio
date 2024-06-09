from datetime import datetime

class Cadastrar:
    def __init__(self, nome_completo, documento, email, senha, tipo, telefone):
        self.nome_completo = nome_completo
        self.documento = documento
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.telefone = telefone

    def logar(self):
        print(f"{self.nome_completo} logado com sucesso.")

    def realizar_cadastro(self):
        print(f"{self.nome_completo} cadastrado com sucesso.")

    def visualizar_p(self):
        return f"Nome: {self.nome_completo}, Email: {self.email}, Telefone: {self.telefone}"

    def deletar_p(self):
        print(f"Perfil de {self.nome_completo} deletado.")

    def editar_p(self, nome_completo=None, email=None, telefone=None):
        if nome_completo:
            self.nome_completo = nome_completo
        if email:
            self.email = email
        if telefone:
            self.telefone = telefone
        print(f"Perfil de {self.nome_completo} atualizado.")

class Morador(Cadastrar):
    def __init__(self, nome_completo, documento, email, senha, tipo, telefone, endereco):
        super().__init__(nome_completo, documento, email, senha, tipo, telefone)
        self.endereco = endereco

    def abrir_chamado(self):
        print(f"Chamado aberto por {self.nome_completo}.")

    def menu_principal(self):
        print("\nSelecione a opção desejada:")
        print("1. Solicitar Reparo")
        print("2. Enviar Notificação")
        print("3. Fazer Sugestão")
        print("4. Registrar Queixa de Importunação de Sossego")
        opcao = input("Digite o número correspondente à opção desejada: ")
        
        if opcao == '1':
            reparo = self.create_reparo()
            if reparo:
                print("Reparo solicitado com sucesso!")
        elif opcao == '2':
            notificacao = self.create_notificacao()
            print("Notificação enviada com sucesso!")
        elif opcao == '3':
            sugestao = self.create_sugestao()
            print("Sugestão enviada com sucesso!")
        elif opcao == '4':
            queixa = self.create_queixa_sossego()
            print("Queixa registrada com sucesso!")
        else:
            print("Opção inválida. O programa será encerrado.")

    def create_sugestao(self):
        tema = input("Tema da Sugestão: ")
        descricao = input("Descrição da Sugestão: ")
        data = datetime.now()
        return Sugestao(
            autor=self,
            tema=tema,
            data=data,
            descricao=descricao
        )

    def create_reparo(self):
        print("Selecione o tipo de reparo:")
        print("1. Reparo de Via")
        print("2. Limpeza")
        print("3. Reparo de Dutos")
        print("4. Queda de Fiação")
        print("5. Combate à Dengue")
        print("6. Reparo de Iluminação")
        opcao = input("Digite o número correspondente ao tipo de reparo desejado: ")
        if opcao == '1':
            return Reparo(reparo_de_via=True)
        elif opcao == '2':
            return Reparo(limpeza=True)
        elif opcao == '3':
            return Reparo(reparo_de_dutos=True)
        elif opcao == '4':
            return Reparo(queda_de_fiacao=True)
        elif opcao == '5':
            return Reparo(combate_a_dengue=True)
        elif opcao == '6':
            return Reparo(reparo_de_iluminacao=True)
        else:
            print("Opção inválida.")
            return None

    def create_notificacao(self):
        destinatario = input("Digite o nome do destinatário da notificação (portaria, síndico, etc.): ")
        mensagem = input("Digite a mensagem da notificação: ")
        return Notificacao(remetente=self, destinatario=destinatario, mensagem=mensagem)

    def create_queixa_sossego(self):
        descricao = input("Descreva a importunação de sossego: ")
        data = datetime.now()
        return QueixaSossego(autor=self, descricao=descricao, data=data)

class Sindico(Cadastrar):
    def __init__(self, nome_completo, documento, email, senha, tipo, telefone, endereco):
        super().__init__(nome_completo, documento, email, senha, tipo, telefone)
        self.endereco = endereco
    def aprovar_user(self, usuario):
        print(f"{self.nome_completo} aprovou o usuário {usuario.nome_completo}.")

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

    def sugerir(self):
        print(f"Sugestão feita por {self.autor.nome_completo}: {self.descricao}")

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

    def registrar_queixa(self):
        print(f"Queixa registrada por {self.autor.nome_completo}: {self.descricao}")
