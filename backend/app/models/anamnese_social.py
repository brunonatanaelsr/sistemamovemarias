"""
Modelo para Anamnese Social.

Este modelo representa a anamnese social completa das beneficiárias,
incluindo informações biopsicossociais e vulnerabilidades.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.extensions import db


class AnamneseSocial(db.Model):
    """
    Modelo para anamnese social das beneficiárias.
    
    Corresponde ao formulário ANAMNESESOCIAL.docx.
    """
    
    __tablename__ = 'anamneses_social'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único da anamnese"
    )
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiarias.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,  # Uma anamnese por beneficiária
        index=True,
        comment="ID da beneficiária"
    )
    
    # Dados da anamnese
    data_anamnese = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Data da realização da anamnese"
    )
    
    profissional_responsavel = Column(
        String(200),
        nullable=False,
        comment="Profissional responsável pela anamnese"
    )
    
    # Observações gerais
    observacoes_importantes = Column(
        Text,
        nullable=True,
        comment="Observações importantes sobre a beneficiária"
    )
    
    # Seção biopsicossocial - Uso de substâncias
    uso_alcool = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Faz uso de álcool?"
    )
    
    uso_drogas_ilicitas = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Faz uso de drogas ilícitas?"
    )
    
    uso_cigarros = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Faz uso de cigarros?"
    )
    
    uso_outros = Column(
        String(500),
        nullable=True,
        comment="Outros usos de substâncias"
    )
    
    # Seção familiar - Transtornos e deficiências
    transtorno_mental_desenvolvimento = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Alguém na família com transtorno mental/desenvolvimento?"
    )
    
    desafios_transtorno = Column(
        Text,
        nullable=True,
        comment="Desafios relacionados ao transtorno"
    )
    
    deficiencia = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Alguém na família com deficiência?"
    )
    
    desafios_deficiencia = Column(
        Text,
        nullable=True,
        comment="Desafios relacionados à deficiência"
    )
    
    idosos_dependentes = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Idosos ou pessoas dependentes na família?"
    )
    
    desafios_idosos = Column(
        Text,
        nullable=True,
        comment="Desafios relacionados a idosos/dependentes"
    )
    
    doenca_cronica_degenerativa = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Alguém com doença crônica ou degenerativa?"
    )
    
    desafios_doenca = Column(
        Text,
        nullable=True,
        comment="Desafios relacionados à doença"
    )
    
    # Vulnerabilidades
    vulnerabilidades = Column(
        ARRAY(String),
        nullable=True,
        comment="Lista de vulnerabilidades identificadas"
    )
    
    # Informações socioeconômicas
    renda_familiar_total = Column(
        String(100),
        nullable=True,
        comment="Renda familiar total aproximada"
    )
    
    fonte_renda_principal = Column(
        String(200),
        nullable=True,
        comment="Principal fonte de renda da família"
    )
    
    situacao_moradia = Column(
        String(200),
        nullable=True,
        comment="Situação de moradia (própria, alugada, cedida, etc.)"
    )
    
    # Rede de apoio
    rede_apoio_familiar = Column(
        Text,
        nullable=True,
        comment="Descrição da rede de apoio familiar"
    )
    
    rede_apoio_comunitaria = Column(
        Text,
        nullable=True,
        comment="Descrição da rede de apoio comunitária"
    )
    
    # Histórico de violências
    historico_violencia = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Histórico de violência?"
    )
    
    tipos_violencia = Column(
        ARRAY(String),
        nullable=True,
        comment="Tipos de violência sofridas"
    )
    
    # Assinaturas
    assinatura_beneficiaria = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Beneficiária assinou a anamnese?"
    )
    
    assinatura_tecnica = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Técnica assinou a anamnese?"
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
        back_populates="anamnese_social",
        lazy="select"
    )
    
    membros_familiares = relationship(
        "MembroFamiliar",
        back_populates="anamnese",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<AnamneseSocial("
            f"id={self.id}, "
            f"beneficiaria_id={self.beneficiaria_id}, "
            f"data={self.data_anamnese.strftime('%d/%m/%Y') if self.data_anamnese else 'N/A'}, "
            f"profissional='{self.profissional_responsavel}'"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'beneficiaria_id': str(self.beneficiaria_id),
            'data_anamnese': self.data_anamnese.isoformat() if self.data_anamnese else None,
            'profissional_responsavel': self.profissional_responsavel,
            'observacoes_importantes': self.observacoes_importantes,
            'uso_alcool': self.uso_alcool,
            'uso_drogas_ilicitas': self.uso_drogas_ilicitas,
            'uso_cigarros': self.uso_cigarros,
            'uso_outros': self.uso_outros,
            'transtorno_mental_desenvolvimento': self.transtorno_mental_desenvolvimento,
            'desafios_transtorno': self.desafios_transtorno,
            'deficiencia': self.deficiencia,
            'desafios_deficiencia': self.desafios_deficiencia,
            'idosos_dependentes': self.idosos_dependentes,
            'desafios_idosos': self.desafios_idosos,
            'doenca_cronica_degenerativa': self.doenca_cronica_degenerativa,
            'desafios_doenca': self.desafios_doenca,
            'vulnerabilidades': self.vulnerabilidades,
            'renda_familiar_total': self.renda_familiar_total,
            'fonte_renda_principal': self.fonte_renda_principal,
            'situacao_moradia': self.situacao_moradia,
            'rede_apoio_familiar': self.rede_apoio_familiar,
            'rede_apoio_comunitaria': self.rede_apoio_comunitaria,
            'historico_violencia': self.historico_violencia,
            'tipos_violencia': self.tipos_violencia,
            'assinatura_beneficiaria': self.assinatura_beneficiaria,
            'assinatura_tecnica': self.assinatura_tecnica,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat(),
            'membros_familiares': [membro.to_dict() for membro in self.membros_familiares] if self.membros_familiares else []
        }
    
    @classmethod
    def find_by_beneficiaria(cls, beneficiaria_id):
        """Busca anamnese por beneficiária."""
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id).first()
    
    @classmethod
    def find_by_vulnerabilidades(cls, vulnerabilidade):
        """Busca anamneses que contenham uma vulnerabilidade específica."""
        return cls.query.filter(
            cls.vulnerabilidades.contains([vulnerabilidade])
        ).all()
    
    @classmethod
    def find_by_profissional(cls, profissional):
        """Busca anamneses por profissional responsável."""
        return cls.query.filter(
            cls.profissional_responsavel.ilike(f'%{profissional}%')
        ).all()
