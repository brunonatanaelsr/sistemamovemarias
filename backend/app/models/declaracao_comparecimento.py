"""
Modelo para Declaração de Comparecimento.

Este modelo representa o registro de comparecimento de uma beneficiária
aos atendimentos do Instituto Move Marias.
"""

import uuid
from datetime import datetime, time
from sqlalchemy import Column, String, DateTime, Time, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import db


class DeclaracaoComparecimento(db.Model):
    """
    Modelo para registro de declarações de comparecimento.
    
    Corresponde ao formulário declaração-modelo2.docx (primeira parte).
    """
    
    __tablename__ = 'declaracoes_comparecimento'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único da declaração"
    )
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiarias.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment="ID da beneficiária que compareceu"
    )
    
    # Dados do comparecimento
    data_comparecimento = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Data do comparecimento"
    )
    
    hora_entrada = Column(
        Time,
        nullable=True,
        comment="Horário de entrada"
    )
    
    hora_saida = Column(
        Time,
        nullable=True,
        comment="Horário de saída"
    )
    
    profissional_responsavel = Column(
        String(200),
        nullable=False,
        comment="Nome da profissional responsável pelo atendimento"
    )
    
    # Informações adicionais
    observacoes = Column(
        Text,
        nullable=True,
        comment="Observações sobre o atendimento"
    )
    
    tipo_atendimento = Column(
        String(100),
        nullable=True,
        comment="Tipo de atendimento realizado"
    )
    
    # Auditoria
    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Data de criação do registro"
    )
    
    atualizado_em = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Data da última atualização"
    )
    
    # Relacionamentos
    beneficiaria = relationship(
        "Beneficiaria",
        back_populates="declaracoes_comparecimento",
        lazy="select"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<DeclaracaoComparecimento("
            f"id={self.id}, "
            f"beneficiaria_id={self.beneficiaria_id}, "
            f"data={self.data_comparecimento.strftime('%d/%m/%Y') if self.data_comparecimento else 'N/A'}, "
            f"profissional='{self.profissional_responsavel}'"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'beneficiaria_id': str(self.beneficiaria_id),
            'data_comparecimento': self.data_comparecimento.isoformat() if self.data_comparecimento else None,
            'hora_entrada': self.hora_entrada.strftime('%H:%M') if self.hora_entrada else None,
            'hora_saida': self.hora_saida.strftime('%H:%M') if self.hora_saida else None,
            'profissional_responsavel': self.profissional_responsavel,
            'observacoes': self.observacoes,
            'tipo_atendimento': self.tipo_atendimento,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @classmethod
    def find_by_beneficiaria(cls, beneficiaria_id):
        """Busca declarações por beneficiária."""
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id).all()
    
    @classmethod
    def find_by_data(cls, data_inicio, data_fim=None):
        """Busca declarações por período."""
        query = cls.query.filter(cls.data_comparecimento >= data_inicio)
        if data_fim:
            query = query.filter(cls.data_comparecimento <= data_fim)
        return query.all()
    
    @classmethod
    def find_by_profissional(cls, profissional):
        """Busca declarações por profissional responsável."""
        return cls.query.filter(
            cls.profissional_responsavel.ilike(f'%{profissional}%')
        ).all()
