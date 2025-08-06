"""
Modelo para Membro Familiar.

Este modelo representa os membros da família de uma beneficiária,
relacionado à anamnese social para análise socioeconômica familiar.
"""

import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Date, ForeignKey, Boolean, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from app.extensions import db
from app.utils.validators import calcular_idade


class MembroFamiliar(db.Model):
    """
    Modelo para membros familiares das beneficiárias.
    
    Relacionado à AnamneseSocial para análise socioeconômica familiar.
    """
    
    __tablename__ = 'membros_familiares'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único do membro familiar"
    )
    
    # Relacionamento com anamnese social
    anamnese_id = Column(
        UUID(as_uuid=True),
        ForeignKey('anamneses_social.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment="ID da anamnese social"
    )
    
    # Dados pessoais
    nome = Column(
        String(200),
        nullable=False,
        comment="Nome completo do membro familiar"
    )
    
    parentesco = Column(
        String(100),
        nullable=False,
        comment="Grau de parentesco com a beneficiária"
    )
    
    data_nascimento = Column(
        Date,
        nullable=True,
        comment="Data de nascimento do membro"
    )
    
    idade = Column(
        Integer,
        nullable=True,
        comment="Idade do membro (calculada automaticamente)"
    )
    
    sexo = Column(
        String(20),
        nullable=True,
        comment="Sexo do membro familiar"
    )
    
    estado_civil = Column(
        String(50),
        nullable=True,
        comment="Estado civil do membro"
    )
    
    # Informações educacionais
    escolaridade = Column(
        String(100),
        nullable=True,
        comment="Nível de escolaridade"
    )
    
    estudando = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Está estudando atualmente?"
    )
    
    # Informações profissionais
    trabalha = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Trabalha atualmente?"
    )
    
    profissao = Column(
        String(200),
        nullable=True,
        comment="Profissão/ocupação"
    )
    
    tipo_trabalho = Column(
        String(100),
        nullable=True,
        comment="Tipo de trabalho (formal, informal, autônomo, etc.)"
    )
    
    renda = Column(
        Numeric(10, 2),
        nullable=True,
        comment="Renda mensal individual"
    )
    
    # Informações de saúde
    tem_deficiencia = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Possui alguma deficiência?"
    )
    
    tipo_deficiencia = Column(
        String(200),
        nullable=True,
        comment="Tipo de deficiência (se aplicável)"
    )
    
    problemas_saude = Column(
        String(500),
        nullable=True,
        comment="Problemas de saúde conhecidos"
    )
    
    # Dependência
    dependente = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="É dependente de cuidados especiais?"
    )
    
    tipo_dependencia = Column(
        String(200),
        nullable=True,
        comment="Tipo de dependência (se aplicável)"
    )
    
    # Observações
    observacoes = Column(
        String(1000),
        nullable=True,
        comment="Observações adicionais sobre o membro"
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
    anamnese = relationship(
        "AnamneseSocial",
        back_populates="membros_familiares",
        lazy="select"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<MembroFamiliar("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"parentesco='{self.parentesco}', "
            f"idade={self.idade}, "
            f"trabalha={self.trabalha}"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'anamnese_id': str(self.anamnese_id),
            'nome': self.nome,
            'parentesco': self.parentesco,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'idade': self.idade,
            'sexo': self.sexo,
            'estado_civil': self.estado_civil,
            'escolaridade': self.escolaridade,
            'estudando': self.estudando,
            'trabalha': self.trabalha,
            'profissao': self.profissao,
            'tipo_trabalho': self.tipo_trabalho,
            'renda': float(self.renda) if self.renda else None,
            'tem_deficiencia': self.tem_deficiencia,
            'tipo_deficiencia': self.tipo_deficiencia,
            'problemas_saude': self.problemas_saude,
            'dependente': self.dependente,
            'tipo_dependencia': self.tipo_dependencia,
            'observacoes': self.observacoes,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @validates('data_nascimento')
    def validate_data_nascimento(self, key, data_nascimento):
        """Valida data de nascimento e calcula idade."""
        if data_nascimento:
            # Calcular idade automaticamente
            self.idade = calcular_idade(data_nascimento)
        return data_nascimento
    
    @classmethod
    def find_by_anamnese(cls, anamnese_id):
        """Busca membros por anamnese."""
        return cls.query.filter_by(anamnese_id=anamnese_id).all()
    
    @classmethod
    def find_trabalhadores(cls, anamnese_id):
        """Busca membros que trabalham em uma família."""
        return cls.query.filter_by(
            anamnese_id=anamnese_id,
            trabalha=True
        ).all()
    
    @classmethod
    def find_dependentes(cls, anamnese_id):
        """Busca membros dependentes em uma família."""
        return cls.query.filter_by(
            anamnese_id=anamnese_id,
            dependente=True
        ).all()
    
    @classmethod
    def calcular_renda_total(cls, anamnese_id):
        """Calcula renda total da família."""
        membros = cls.query.filter_by(anamnese_id=anamnese_id).all()
        total = sum(
            membro.renda for membro in membros 
            if membro.renda is not None
        )
        return float(total) if total else 0.0
    
    @classmethod
    def get_estatisticas_familia(cls, anamnese_id):
        """Obtém estatísticas da composição familiar."""
        membros = cls.query.filter_by(anamnese_id=anamnese_id).all()
        
        return {
            'total_membros': len(membros),
            'trabalhadores': len([m for m in membros if m.trabalha]),
            'dependentes': len([m for m in membros if m.dependente]),
            'estudando': len([m for m in membros if m.estudando]),
            'com_deficiencia': len([m for m in membros if m.tem_deficiencia]),
            'renda_total': cls.calcular_renda_total(anamnese_id),
            'idade_media': sum(m.idade for m in membros if m.idade) / len([m for m in membros if m.idade]) if any(m.idade for m in membros) else 0
        }
