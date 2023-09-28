from pydantic import BaseModel
from typing import Optional, List
from Model.Cliente import Cliente


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser retornado
    """
    nome: str = "Maria"
    sobrenome: str = "Souza"
    e_mail: str = "maria_souza@kakaka.com"
    senha: str = "wawawawa"


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente
    """
    id: int = 1
    nome: str = "Maria"
    sobrenome: str = "Souza"
    e_mail: str = "maria_souza@kakaka.com"
    senha: str = "wawawawa"


class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome: str = "Maria"


class ListagemClienteSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    cliente: List[ClienteViewSchema]


class ClienteUpdateSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    nome: str = "Maria"
    sobrenome: str = "Souza"
    e_mail: str = "maria_souza@kakaka.com"
    senha: str = "wawawawa"


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "sobrenome": cliente.sobrenome,
            "e_mail": cliente.e_mail,
            "senha": cliente.senha
        })

    return {"clientes": result}


def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "sobrenome": cliente.sobrenome,
        "e_mail": cliente.e_mail,
        "senha": cliente.senha
    }


class ClienteBuscaPorNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome: str = "Maria"


class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str = " Cliente excluído com sucesso"
    id: int = "1"


class ClienteSchemaId(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no id do cliente.
    """
    id: int = 1
