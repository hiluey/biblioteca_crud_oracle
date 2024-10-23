import datetime
import locale
from model.emprestimo import Emprestimo
from model.livro import Livro
from model.usuario import Usuario
from controller.controller_livro import Controller_Livro
from controller.controller_usuario import Controller_Usuario
from conexion.oracle_queries import OracleQueries

from reports.relatorios import Relatorio

class Controller_Emprestimo:

    def __init__(self):
        self.relatorio = Relatorio()
        self.ctrl_usuario = Controller_Usuario()
        self.ctrl_livro = Controller_Livro()

    def inserir_emprestimo(self) -> Emprestimo:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        emprestimo_cadastrado = self.cadastrar_emprestimo(oracle)
        if(emprestimo_cadastrado == None):
            return None

        id_livro = emprestimo_cadastrado.get_livro().get_id_livro()
        id_usuario = emprestimo_cadastrado.get_usuario().get_id_usuario()
        data_emprestimo = emprestimo_cadastrado.get_data_emprestimo()
        data_devolucao_sugerida = emprestimo_cadastrado.get_data_devolucao()

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, id_livro=int(id_livro), id_usuario=int(id_usuario), data_emprestimo=data_emprestimo, data_devolucao_sugerida=data_devolucao_sugerida)
        # Executa o bloco PL/SQL anônimo para inserção do novo objeto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := EMPRESTIMOS_ID_EMPRESTIMO_SEQ.NEXTVAL;
            insert into emprestimos values(:codigo, :id_livro, :id_usuario, to_date(:data_emprestimo,'DD/MM/YYYY'), to_date(:data_devolucao_sugerida,'DD/MM/YYYY'));
        end;
        """, data)
        # Recupera o código da nova entidade
        id_emprestimo = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        novo_emprestimo = Controller_Emprestimo.get_emprestimo_from_dataframe(oracle, id_emprestimo)
        # Exibe os atributos do novo objeto
        print(novo_emprestimo.to_string())
        # Retorna o objeto para utilização posterior, caso necessário
        return novo_emprestimo

    def atualizar_emprestimo(self) -> Emprestimo:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_emprestimo = int(input("Código do Empréstimo que irá alterar: "))        

        # Verifica se a entidade existe na base de dados
        if Controller_Emprestimo.verifica_existencia_emprestimo(oracle, id_emprestimo):
            emprestimo_cadastrado = self.cadastrar_emprestimo(oracle)
            if(emprestimo_cadastrado == None):
                return None

            # Atualiza os dados da entidade existente
            oracle.write(f"update emprestimos set id_livro = '{emprestimo_cadastrado.get_livro().get_id_livro()}', id_usuario = '{emprestimo_cadastrado.get_usuario().get_id_usuario()}', data_emprestimo = to_date('{emprestimo_cadastrado.get_data_emprestimo()}','DD/MM/YYYY'), data_devolucao_sugerida = to_date('{emprestimo_cadastrado.get_data_devolucao()}','DD/MM/YYYY') where id_emprestimo = {id_emprestimo}")

            # Cria um novo objeto atualizado
            emprestimo_atualizado = Controller_Emprestimo.get_emprestimo_from_dataframe(oracle, id_emprestimo)

            # Exibe os atributos do novo objeto
            print(emprestimo_atualizado.to_string())

            # Retorna o objeto para utilização posterior, caso necessário
            return emprestimo_atualizado
        else:
            print(f"O código {id_emprestimo} não existe.")
            return None

    def excluir_emprestimo(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_emprestimo = int(input("Código do Empréstimo que irá excluir: ")) 

        # Verifica se a entidade existe na base de dados
        if not Controller_Emprestimo.verifica_existencia_emprestimo(oracle, id_emprestimo):            
            print(f"O código de empréstimo {id_emprestimo} não existe.")

        # Confirma se o usuário realmente deseja excluir o item selecionado
        confirmar_exclusao = input("Deseja realmente continuar com a exclusão? (S/N): ")
        if confirmar_exclusao.strip().lower() != "s":
            return None

        emprestimo_chave_estrangeira = oracle.sqlToDataFrame(f"select id_emprestimo from devolucoes where id_emprestimo = {id_emprestimo}")
        
        if not emprestimo_chave_estrangeira.empty:
            print(f"O empréstimo de código {id_emprestimo} possui registros dependentes. Deseja excluir mesmo assim? [S/N]")
            opcao = input()

            if opcao.upper() != "S":
                print("Operação cancelada.")
                return None
            
            print("Excluindo registros dependentes...")

        # Recupera os dados da entidade e cria um novo objeto para informar que foi removido
        emprestimo_excluido = Controller_Emprestimo.get_emprestimo_from_dataframe(oracle, id_emprestimo)
        # Revome da tabela
        oracle.write(f"delete from emprestimos where id_emprestimo = {id_emprestimo}")
        # Exibe os atributos do objeto excluído
        print("Empréstimo removido com Sucesso!")
        print(emprestimo_excluido.to_string())

    def cadastrar_emprestimo(self, oracle) -> Emprestimo:
        #Solicita os dados de cadastro
        print("Informe os dados do empréstimo.\n")

        # Lista os usuarios existentes para inserir no item de emprestimo
        self.relatorio.get_relatorio_usuarios()
        codigo_usuario = str(input("\nDigite o código do usuário a fazer o empréstimo: "))
        usuario = Controller_Usuario.valida_usuario(oracle, codigo_usuario)
        if usuario == None:
            return None        

        print("\n\n")

        self.relatorio.get_relatorio_livros_disponiveis()
        codigo_livro = str(input("\nDigite o código do livro a ser emprestado: "))
        livro = Controller_Livro.valida_livro_disponivel(oracle, codigo_livro)
        if livro == None:
            return None

        data_emprestimo = input("Data de empréstimo (DD/MM/YYYY): ")
        while not Controller_Emprestimo.valida_data_format(data_emprestimo):
            print("\nVocê tentou inserir um formato inválido, tente novamente.\n")
            data_emprestimo = input("Data de empréstimo (DD/MM/YYYY): ")

        data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")
        while not Controller_Emprestimo.valida_data_format(data_devolucao):
            print("\nVocê tentou inserir um formato inválido, tente novamente.\n")
            data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")
        
        while not Controller_Emprestimo.valida_data_entrega_devolucao(data_emprestimo, data_devolucao):
            print("\nVocê tentou inserir uma data de devolução menor que a data de entrega, tente novamente.\n")
            data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")

        return Emprestimo(0, livro, usuario, data_emprestimo, data_devolucao)

    @staticmethod
    def verifica_existencia_emprestimo(oracle:OracleQueries, id_emprestimo:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        df_emprestimo = oracle.sqlToDataFrame(f"select id_emprestimo, id_livro, id_usuario, data_emprestimo, data_devolucao_sugerida from emprestimos where id_emprestimo = {id_emprestimo}")
        return not df_emprestimo.empty
    
    @staticmethod
    def get_emprestimo_from_dataframe(oracle:OracleQueries, id_emprestimo:int=None) -> Emprestimo:
        # Recupera os dados transformando em um DataFrame
        df_emprestimo = oracle.sqlToDataFrame(f"select id_emprestimo, id_livro, id_usuario, data_emprestimo, data_devolucao_sugerida from emprestimos where id_emprestimo = {id_emprestimo}")
        # Cria novo objeto a partir do DataFrame
        livro = Controller_Livro.get_livro_from_dataframe(oracle, int(df_emprestimo.id_livro.values[0]))
        usuario = Controller_Usuario.get_usuario_from_dataframe(oracle, int(df_emprestimo.id_usuario.values[0]))
        return Emprestimo(int(df_emprestimo.id_emprestimo.values[0]), livro, usuario, df_emprestimo.data_emprestimo.values[0], df_emprestimo.data_devolucao_sugerida.values[0])
    
    @staticmethod
    def valida_emprestimo(oracle:OracleQueries, codigo_emprestimo:int=None) -> Emprestimo:
        if not Controller_Emprestimo.verifica_existencia_emprestimo(oracle, codigo_emprestimo):
            print(f"O empréstimo de código {codigo_emprestimo} não existe na base.")
            return None
        else:
            return Controller_Emprestimo.get_emprestimo_from_dataframe(oracle, codigo_emprestimo)        

    @staticmethod
    def verifica_emprestimo_aberto(oracle:OracleQueries, id_emprestimo:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(f"""
            SELECT
                empr.id_emprestimo,
                CASE 
                    WHEN 
                        EXISTS (
                            SELECT
                            1
                            FROM
                            devolucoes devo
                            WHERE
                            devo.id_emprestimo = empr.id_emprestimo
                        )
                    THEN 1
                    ELSE 0
                END as devolucao_realizada
            FROM emprestimos empr
            WHERE empr.id_emprestimo = {id_emprestimo}
        """)
        if dataframe.empty:
            return False
        
        return int(dataframe.devolucao_realizada.values[0]) == 0

    @staticmethod
    def valida_data_format(data_string:str=None) -> bool:
        try:
            partes_data = data_string.split("/")
            dia = int(partes_data[0])
            mes = int(partes_data[1])
            ano = int(partes_data[2])

            datetime.datetime(ano, mes, dia)
            return True
        
        except:
            print("Erro ao validar data.")
            return False
        
    @staticmethod
    def valida_data_entrega_devolucao(data_entrega: str, data_devolucao: str) -> bool:
        try:
            def converter_data(data: str) -> datetime:
                partes_data = data.split("/")
                dia = int(partes_data[0])
                mes = int(partes_data[1])
                ano = int(partes_data[2])
                return datetime.datetime(ano, mes, dia)

            data_entrega = converter_data(data_entrega)
            data_devolucao = converter_data(data_devolucao)

            if data_devolucao < data_entrega:
                # Formata a data para exibição
                data_entrega_formatada = data_entrega.strftime('%d/%m/%Y')
                data_devolucao_formatada = data_devolucao.strftime('%d/%m/%Y')
                # Exibe mensagem de erro
                raise Exception(f"Data de Devolução ({data_devolucao_formatada}) menor que a Data de Entrega ({data_entrega_formatada})")

            return True

        except Exception as error:
            print(f"\nErro ao validar data: {error}")
            return False
