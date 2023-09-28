from sqlalchemy import Column, String, Integer, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from typing import Union


from Model import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), default='Cliente')
    sobrenome = Column(String(30), nullable=True)
    e_mail = Column(String)
    senha = Column(String)
    
    
    def __init__(self, nome: str, sobrenome: str, e_mail: str, senha: str):
        self.nome = nome
        self.sobrenome = sobrenome
        self.e_mail = e_mail
        self.senha = senha
        

def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Cliente.
        """
        return{
            
            "id": self.id,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "e_mail": self.e_mail,
            "senha": self.senha
           
        }
            
def __repr__(self):
    """
    Retorna uma representação do cliente em forma de texto.
    """
    return f"Cliente (id={self.id}, nome='{self.nome}', sobrenome= '{self.sobrenome}', e_mail= {self.e_mail}, senha='{self.senha}')"



