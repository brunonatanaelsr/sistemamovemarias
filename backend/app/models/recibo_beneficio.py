"""
Modelo para Recibo de Benefício.

Este modelo representa o registro de benefícios recebidos pelas beneficiárias
do Instituto Move Marias.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import db


class ReciboBeneficio(db.Model):
    """
    Modelo para registro de recibos de benefícios.
    
    Corresponde ao formulário declaração-modelo2.docx (segunda parte).
    """
    
    __tablename__ = 'recibos_beneficio'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único do recibo"
    )
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiarias.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment="ID da beneficiária que recebeu o benefício"
    )
    
    # Dados do benefício
    tipo_beneficio = Column(
        String(200),
        nullable=False,
        comment="Descrição do tipo de benefício recebido"
    )
    
    descricao_beneficio = Column(
        Text,
        nullable=True,
        comment="Descrição detalhada do benefício"
    )
    
    valor_beneficio = Column(
        Numeric(10, 2),
        nullable=True,
        comment="Valor monetário do benefício (se aplicável)"
    )
    
    quantidade = Column(
        String(50),
        nullable=True,
        comment="Quantidade de itens do benefício"
    )
    
    data_recebimento = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Data de recebimento do benefício"
    )
    
    # Informações adicionais
    origem_beneficio = Column(
        String(200),
        nullable=True,
        comment="Origem/fonte do benefício"
    )
    
    responsavel_entrega = Column(
        String(200),
        nullable=False,
        comment="Nome do responsável pela entrega"
    )
    
    observacoes = Column(
        Text,
        nullable=True,
        comment="Observações sobre o benefício"
    )
    
    # Status e controle
    status = Column(
        String(50),
        nullable=False,
        default='entregue',
        comment="Status do benefício (entregue, pendente, cancelado)"
    )
    
    numero_recibo = Column(
        String(50),
        nullable=True,
        unique=True,
        comment="Número sequencial do recibo"
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
        back_populates="recibos_beneficio",
        lazy="select"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<ReciboBeneficio("
            f"id={self.id}, "
            f"beneficiaria_id={self.beneficiaria_id}, "
            f"tipo='{self.tipo_beneficio}', "
            f"data={self.data_recebimento.strftime('%d/%m/%Y') if self.data_recebimento else 'N/A'}"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'beneficiaria_id': str(self.beneficiaria_id),
            'tipo_beneficio': self.tipo_beneficio,
            'descricao_beneficio': self.descricao_beneficio,
            'valor_beneficio': float(self.valor_beneficio) if self.valor_beneficio else None,
            'quantidade': self.quantidade,
            'data_recebimento': self.data_recebimento.isoformat() if self.data_recebimento else None,
            'origem_beneficio': self.origem_beneficio,
            'responsavel_entrega': self.responsavel_entrega,
            'observacoes': self.observacoes,
            'status': self.status,
            'numero_recibo': self.numero_recibo,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @classmethod
    def find_by_beneficiaria(cls, beneficiaria_id):
        """Busca recibos por beneficiária."""
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id).all()
    
    @classmethod
    def find_by_tipo(cls, tipo_beneficio):
        """Busca recibos por tipo de benefício."""
        return cls.query.filter(
            cls.tipo_beneficio.ilike(f'%{tipo_beneficio}%')
        ).all()
    
    @classmethod
    def find_by_periodo(cls, data_inicio, data_fim=None):
        """Busca recibos por período."""
        query = cls.query.filter(cls.data_recebimento >= data_inicio)
        if data_fim:
            query = query.filter(cls.data_recebimento <= data_fim)
        return query.all()
    
    @classmethod
    def find_by_status(cls, status):
        """Busca recibos por status."""
        return cls.query.filter_by(status=status).all()
    
    def gerar_numero_recibo(self):
        """Gera número sequencial para o recibo."""
        if not self.numero_recibo:
            ano = self.data_recebimento.year
            count = ReciboBeneficio.query.filter(
                db.extract('year', ReciboBeneficio.data_recebimento) == ano
            ).count()
            self.numero_recibo = f"RB-{ano}-{count + 1:04d}"
