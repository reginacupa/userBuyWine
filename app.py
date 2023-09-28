from flask_openapi3 import OpenAPI, Info, Tag
from flask import request, redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from Model import Cliente, Session
from logger import logger
from Schema import *
from Schema import ErrorSchema

from flask_cors import CORS

info = Info(title="Cliente Api", version="1.0.0")

app = OpenAPI(__name__, info=info)
CORS(app)


# Definindo as tags
home_tag = Tag(name="Documentação", description="Descrição de documentação: Swagger")

cliente_tag = Tag(
    name="Cliente", description="Cadastro, visualização e remoção de clientes à base"
)

@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")




@app.get("/clientes", tags=[cliente_tag],
    responses={"200": ListagemClienteSchema, "404": ErrorSchema},
)

def get_clientes():
    """Faz a busca por todos os clientes cadastrados
    Retorna uma apresentação da listagem de clientes."""

    logger.info(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.info(f"%d clientes encontrados" % len(clientes))
        # retorna a representação do cliente
        return apresenta_clientes(clientes), 200
    

    
@app.post( "/post_cliente", tags=[cliente_tag],
    responses={"200": ClienteSchema, "409": ErrorSchema, "400": ErrorSchema},
)

def add_cliente(form: ClienteSchema):
    """Cadastra um novo cliente à base de dados"""
    """Retorna uma apresentação do cliente"""

    print(form)
    cliente = Cliente(
        nome=form.nome,
        sobrenome=form.sobrenome,
        e_mail=form.e_mail,
        senha=form.senha
        
    )
    logger.info(f"Adicionando cliente de nome: '{cliente.nome}'")

    try:
        # criando conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        # efetivando o camando de adição de novo cliente na tabela
        session.commit()
        logger.info("Adicionado cliente: %s" % cliente)
        return apresenta_cliente(cliente), 200

    except Exception as e:
        # caso erro fora do previsto
        error_msg = "Não foi possível cadastrar novo cliente  :("
        logger.warning(f"Erro ao adicionar produto '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

    except IntegrityError as e:
        # duplicidade do nome é a provavel razão do IntegrityError
        error_msg = "Cliente de mesmo nome e sobrenome já salvo na base  :/ "
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    


@app.delete("/delete_cliente",tags=[cliente_tag],
    responses={"200": ClienteDelSchema, "404": ErrorSchema},
)

def del_cliente(query: ClienteSchemaId):
    """Deleta um produto a partir do id informado
    Retorna uma mensagem de confirmação da remoção."""

    cliente_id = query.id
    logger.info(f"Deletando dados sobre cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.id == cliente_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Deletado cliente #{cliente_id}")
        return {"mesage": "Cliente removido", "id": cliente_id}, 200
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :( "
        logger.warning(f"Erro ao deletar cliente #'{cliente_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    

@app.get( "/busca_cliente",tags=[cliente_tag],
    responses={"200": ListagemClienteSchema, "404": ErrorSchema},
)
def busca_cliente(query: ClienteBuscaPorNomeSchema):
    """Faz a busca por clientes em que o termo passando nome.

    Retorna uma representação dos clientes.
    """
    nome = query.nome
    logger.info(f"Fazendo a busca por nome com o termo: {nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    clientes = (
        session.query(Cliente).filter(Cliente.nome.ilike(f"%{nome}%")).all()
    )

    if not clientes:
        # se não há clientes cadastrados
        return {"produtos": []}, 200
    else:
        logger.info(f"%d clientes encontrados" % len(clientes))
        # retorna a representação dos clientes
        return apresenta_clientes(clientes), 200
    

@app.put( "/cliente",
    tags=[cliente_tag],
    responses={"200": ClienteSchemaId, "404": ErrorSchema},
)
def update_cliente(query: ClienteSchemaId, form: ClienteUpdateSchema):
    """Edita um cliente a partir do id informado

    Retorna uma mensagem de confirmação da edição.
    """
    cliente_id = query.id
    Stringpi = str(cliente_id)
    logger.debug(f"Editando dados sobre o cliente #{Stringpi}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = (
        # cliente.nome == cliente_nome).first()
        session.query(Cliente)
        .filter(Cliente.id == cliente_id)
        .first()
    )
    count.nome = form.nome
    count.sobrenome = form.sobrenome
    count.e_mail = form.e_mail
    count.senha = form.senha
    
    print("nome")
    print(count.nome)
    print(count.sobrenome)
    print(count.e_mail)
    print(count.senha)

    session.commit()
    return apresenta_cliente(count), 200


if __name__ == "__main__":
    app.run(debug=True)