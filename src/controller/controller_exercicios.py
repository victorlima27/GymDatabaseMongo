from model.Exercicios import Exercicios
import pandas as pd
from conexion.mongo_queries import MongoQueries

class Controller_Exercicios:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_exercicio(self) -> Exercicios:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        nome_exercicio = input("Digite o nome do exercício: ")
        repeticoes = input("Número de repetições: ")
        grupo_muscular= input("Grupo muscular treinado: ")

        sequence = int(self.mongo.db["exercicios"].count_documents({})+1)

        
        # Insere e persiste o novo cliente
        self.mongo.db["exercicios"].insert_one({"Codigo_Exercicio": sequence, "Repeticoes": repeticoes,"Nome_Exercicio": nome_exercicio,"Grupo_Muscular": grupo_muscular})
        # Recupera os dados do novo cliente criado transformando em um DataFrame

        df_exercicio = self.recupera_exercicio(sequence)


        # Cria um novo objeto Cliente

        codigo = df_exercicio.Codigo_Exercicio.values[0]
        repeticoes = df_exercicio.Repeticoes.values[0]
        grupo_muscular = df_exercicio.Grupo_Muscular.values[0]
        nome = df_exercicio.Nome_Exercicio.values[0]


        novo_exercicio = Exercicios(codigo,repeticoes,grupo_muscular,nome)

        # Exibe os atributos do novo cliente
        print(novo_exercicio.to_string())
        self.mongo.close()
        # Retorna o objeto novo_cliente para utilização posterior, caso necessário
        return novo_exercicio

            



    def atualizar_exercicio(self) -> Exercicios:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect() 
        

        #self.listar_exercicios()
        codigo_exercicio = int(input("Insira o código do exercício a ser alterado"))

        if not self.verifica_existencia_exercicio(codigo_exercicio):


            print("1 - Nome\n 2 - Repetições")
            aux = int(input("Insira qual atributo irá ser alterado"))
            #Alterar nome      
            if aux == 1:

                novo_nome = input("Insira o novo nome: ")

                self.mongo.db["exercicios"].update_one({"Codigo_Exercicio": f"{codigo_exercicio}"}, {"$set": {"Nome_Exercicio": novo_nome}})

                df_exercicio = self.recupera_exercicio(codigo_exercicio)


                codigo = df_exercicio.codigo_exercicio.values[0]
                repeticoes = df_exercicio.repeticoes.values[0]
                grupo_muscular = df_exercicio.grupo_muscular.values[0]
                nome = df_exercicio.nome_exercicio.values[0]
                exercicio_atualizado = Exercicios(codigo,repeticoes,grupo_muscular,nome)


                print(exercicio_atualizado.to_string())


                return exercicio_atualizado
            
            #Alterar Telefone
            elif aux == 2:

                novo_repeticoes = input("Insira o novo número de repetições: ")


                self.mongo.db["exercicios"].update_one({"Codigo_Exercicio": f"{codigo_exercicio}"}, {"$set": {"Repeticoes": novo_repeticoes}})


                codigo = df_exercicio.codigo_exercicio.values[0]
                repeticoes = df_exercicio.repeticoes.values[0]
                grupo_muscular = df_exercicio.grupo_muscular.values[0]
                nome = df_exercicio.nome_exercicio.values[0]
                exercicio_atualizado = Exercicios(codigo,repeticoes,grupo_muscular,nome)
            

                print(exercicio_atualizado.to_string())
            

                return exercicio_atualizado
                    



    def excluir_exercicio(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        #self.listar_exercicios()

        
        codigo_exercicio = int(input("Codigo do exercicio a ser excluído: "))


        # Solicita ao usuário o CPF do Cliente a ser alterado

        # Verifica se o cliente existe na base de dados
        if self.verifica_existencia_exercicio(codigo_exercicio):            

            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_exercicio = pd.DataFrame(list(self.mongo.db["exercicios"].find({"Codigo_Exercicio":f"{codigo_exercicio}"}, {"Repeticoes": 1, "Codigo_Exercicio": 1,"Grupo_Muscular":1,"Nome_Exercicio":1, "_id": 0})))
        

            df_exercicio = self.recupera_exercicio(codigo_exercicio)

            self.mongo.db["exercicios"].delete_one({"Codigo_Exercicio":f"{codigo_exercicio}"})

            print(df_exercicio.to_string())

            codigo = df_exercicio.Codigo_Exercicio.values[0]
            repeticoes = df_exercicio.Repeticoes.values[0]
            grupo_muscular = df_exercicio.Grupo_Muscular.values[0]
            nome = df_exercicio.Nome_Exercicio.values[0]


            exercicio_excluido = Exercicios(codigo,repeticoes,grupo_muscular,nome)

            print("Exercicio removido com sucesso!")
            print(exercicio_excluido.to_string())

        else:
            print(f"O codigo {codigo_exercicio} não existe.")

            

            
    def verifica_existencia_exercicio(self, codigo_exercicio:int=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_exercicio = pd.DataFrame(list(self.mongo.db["exercicios"].find({"Codigo_Exercicio":f"{codigo_exercicio}"}, {"Repeticoes": 1, "Codigo_Exercicio": 1,"Grupo_Muscular":1,"Nome_Exercicio":1, "_id": 0})))
        

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_exercicio.empty




    def recupera_exercicio(self, sequence:int=None, external:bool=False) -> pd.DataFrame:

        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame

        df_exercicio = pd.DataFrame(list(self.mongo.db["exercicios"].find({"Codigo_Exercicio":f"{sequence}"}, {"Repeticoes": 1, "Codigo_Exercicio": 1, "Grupo_Muscular":1, "Nome_Exercicio":1,"_id": 0})))
    
        
        print(df_exercicio.to_string())

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_exercicio



    # def listar_exercicios(self, external:bool=False) -> bool:

    #     query = """db.getCollection('exercicios').find({})"""


    #     if external:
    #         # Cria uma nova conexão com o banco que permite alteração
    #         self.mongo.connect()
    #     print(pd.DataFrame(query))
        
        