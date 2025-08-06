"""
Modelo para Termo de Consentimento Livre e Esclarecido.

Este modelo representa o TCLE digital para autorização de uso de imagem
e tratamento de dados pessoais em conformidade com a LGPD.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import db


class TermoConsentimento(db.Model):
    """
    Modelo para Termo de Consentimento Livre e Esclarecido.
    
    Corresponde ao formulário TCLE.docx.
    """
    
    __tablename__ = 'termos_consentimento'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único do termo"
    )
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiarias.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,  # Um termo por beneficiária
        index=True,
        comment="ID da beneficiária"
    )
    
    # Dados do consentimento
    data_consentimento = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Data do consentimento"
    )
    
    # Dados pessoais complementares
    nacionalidade = Column(
        String(100),
        nullable=True,
        comment="Nacionalidade da beneficiária"
    )
    
    estado_civil = Column(
        String(50),
        nullable=True,
        comment="Estado civil da beneficiária"
    )
    
    profissao = Column(
        String(200),
        nullable=True,
        comment="Profissão da beneficiária"
    )
    
    # Dados do responsável legal (se aplicável)
    tem_responsavel_legal = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Possui responsável legal?"
    )
    
    nome_responsavel_legal = Column(
        String(200),
        nullable=True,
        comment="Nome do responsável legal"
    )
    
    cpf_responsavel_legal = Column(
        String(14),
        nullable=True,
        comment="CPF do responsável legal"
    )
    
    parentesco_responsavel = Column(
        String(100),
        nullable=True,
        comment="Grau de parentesco do responsável"
    )
    
    # Consentimentos específicos
    uso_imagem_autorizado = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Autorização para uso da imagem"
    )
    
    uso_imagem_finalidades = Column(
        Text,
        nullable=True,
        comment="Finalidades específicas do uso da imagem"
    )
    
    tratamento_dados_autorizado = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Autorização para tratamento de dados pessoais (LGPD)"
    )
    
    finalidades_tratamento_dados = Column(
        Text,
        nullable=True,
        comment="Finalidades do tratamento de dados"
    )
    
    # Compartilhamento de dados
    compartilhamento_autorizado = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Autorização para compartilhamento de dados"
    )
    
    entidades_compartilhamento = Column(
        Text,
        nullable=True,
        comment="Entidades autorizadas ao compartilhamento"
    )
    
    # Período de consentimento
    data_inicio_consentimento = Column(
        DateTime,
        nullable=True,
        comment="Data de início da validade do consentimento"
    )
    
    data_fim_consentimento = Column(
        DateTime,
        nullable=True,
        comment="Data de fim da validade do consentimento"
    )
    
    # Revogação
    consentimento_revogado = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Consentimento foi revogado?"
    )
    
    data_revogacao = Column(
        DateTime,
        nullable=True,
        comment="Data da revogação do consentimento"
    )
    
    motivo_revogacao = Column(
        Text,
        nullable=True,
        comment="Motivo da revogação"
    )
    
    # Testemunhas
    nome_testemunha1 = Column(
        String(200),
        nullable=True,
        comment="Nome da primeira testemunha"
    )
    
    cpf_testemunha1 = Column(
        String(14),
        nullable=True,
        comment="CPF da primeira testemunha"
    )
    
    nome_testemunha2 = Column(
        String(200),
        nullable=True,
        comment="Nome da segunda testemunha"
    )
    
    cpf_testemunha2 = Column(
        String(14),
        nullable=True,
        comment="CPF da segunda testemunha"
    )
    
    # Assinaturas digitais
    assinatura_voluntaria = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Voluntária assinou o termo?"
    )
    
    ip_assinatura_voluntaria = Column(
        String(45),
        nullable=True,
        comment="IP da assinatura da voluntária"
    )
    
    data_assinatura_voluntaria = Column(
        DateTime,
        nullable=True,
        comment="Data/hora da assinatura da voluntária"
    )
    
    assinatura_responsavel_familiar = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Responsável familiar assinou?"
    )
    
    ip_assinatura_responsavel = Column(
        String(45),
        nullable=True,
        comment="IP da assinatura do responsável"
    )
    
    data_assinatura_responsavel = Column(
        DateTime,
        nullable=True,
        comment="Data/hora da assinatura do responsável"
    )
    
    # Profissional responsável
    profissional_responsavel = Column(
        String(200),
        nullable=False,
        comment="Profissional responsável pela coleta do termo"
    )
    
    cargo_profissional = Column(
        String(100),
        nullable=True,
        comment="Cargo do profissional responsável"
    )
    
    # Observações
    observacoes = Column(
        Text,
        nullable=True,
        comment="Observações sobre o termo de consentimento"
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
        back_populates="termo_consentimento",
        lazy="select"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<TermoConsentimento("
            f"id={self.id}, "
            f"beneficiaria_id={self.beneficiaria_id}, "
            f"data={self.data_consentimento.strftime('%d/%m/%Y') if self.data_consentimento else 'N/A'}, "
            f"uso_imagem={self.uso_imagem_autorizado}, "
            f"tratamento_dados={self.tratamento_dados_autorizado}"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'beneficiaria_id': str(self.beneficiaria_id),
            'data_consentimento': self.data_consentimento.isoformat() if self.data_consentimento else None,
            'nacionalidade': self.nacionalidade,
            'estado_civil': self.estado_civil,
            'profissao': self.profissao,
            'tem_responsavel_legal': self.tem_responsavel_legal,
            'nome_responsavel_legal': self.nome_responsavel_legal,
            'cpf_responsavel_legal': self.cpf_responsavel_legal,
            'parentesco_responsavel': self.parentesco_responsavel,
            'uso_imagem_autorizado': self.uso_imagem_autorizado,
            'uso_imagem_finalidades': self.uso_imagem_finalidades,
            'tratamento_dados_autorizado': self.tratamento_dados_autorizado,
            'finalidades_tratamento_dados': self.finalidades_tratamento_dados,
            'compartilhamento_autorizado': self.compartilhamento_autorizado,
            'entidades_compartilhamento': self.entidades_compartilhamento,
            'data_inicio_consentimento': self.data_inicio_consentimento.isoformat() if self.data_inicio_consentimento else None,
            'data_fim_consentimento': self.data_fim_consentimento.isoformat() if self.data_fim_consentimento else None,
            'consentimento_revogado': self.consentimento_revogado,
            'data_revogacao': self.data_revogacao.isoformat() if self.data_revogacao else None,
            'motivo_revogacao': self.motivo_revogacao,
            'nome_testemunha1': self.nome_testemunha1,
            'cpf_testemunha1': self.cpf_testemunha1,
            'nome_testemunha2': self.nome_testemunha2,
            'cpf_testemunha2': self.cpf_testemunha2,
            'assinatura_voluntaria': self.assinatura_voluntaria,
            'data_assinatura_voluntaria': self.data_assinatura_voluntaria.isoformat() if self.data_assinatura_voluntaria else None,
            'assinatura_responsavel_familiar': self.assinatura_responsavel_familiar,
            'data_assinatura_responsavel': self.data_assinatura_responsavel.isoformat() if self.data_assinatura_responsavel else None,
            'profissional_responsavel': self.profissional_responsavel,
            'cargo_profissional': self.cargo_profissional,
            'observacoes': self.observacoes,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @classmethod
    def find_by_beneficiaria(cls, beneficiaria_id):
        """Busca termo por beneficiária."""
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id).first()
    
    @classmethod
    def find_consentimentos_validos(cls):
        """Busca termos com consentimentos válidos (não revogados)."""
        return cls.query.filter_by(consentimento_revogado=False).all()
    
    @classmethod
    def find_consentimentos_revogados(cls):
        """Busca termos com consentimentos revogados."""
        return cls.query.filter_by(consentimento_revogado=True).all()
    
    def revogar_consentimento(self, motivo=None):
        """Revoga o consentimento."""
        self.consentimento_revogado = True
        self.data_revogacao = datetime.utcnow()
        self.motivo_revogacao = motivo
        self.atualizado_em = datetime.utcnow()
    
    def is_consentimento_valido(self):
        """Verifica se o consentimento ainda é válido."""
        if self.consentimento_revogado:
            return False
        
        if self.data_fim_consentimento and datetime.utcnow() > self.data_fim_consentimento:
            return False
        
        return True
    
    @property
    def status_consentimento(self):
        """Retorna o status atual do consentimento."""
        if self.consentimento_revogado:
            return 'revogado'
        elif self.data_fim_consentimento and datetime.utcnow() > self.data_fim_consentimento:
            return 'expirado'
        else:
            return 'ativo'
