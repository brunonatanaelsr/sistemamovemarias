"""
Modelo para Ficha de Evolução.

Este modelo representa o histórico de evolução e acompanhamento
das beneficiárias do Instituto Move Marias.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import db


class FichaEvolucao(db.Model):
    """
    Modelo para ficha de evolução das beneficiárias.
    
    Corresponde ao formulário FICHADEEVOLUÇÃO.docx.
    """
    
    __tablename__ = 'fichas_evolucao'
    
    # Identificação
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="Identificador único da ficha de evolução"
    )
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(
        UUID(as_uuid=True),
        ForeignKey('beneficiarias.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
        comment="ID da beneficiária"
    )
    
    # Dados da evolução
    data_evolucao = Column(
        DateTime,
        nullable=False,
        index=True,
        comment="Data da evolução/atendimento"
    )
    
    tipo_atendimento = Column(
        String(100),
        nullable=False,
        comment="Tipo de atendimento realizado"
    )
    
    descricao = Column(
        Text,
        nullable=False,
        comment="Descrição detalhada da evolução/movimentação"
    )
    
    responsavel = Column(
        String(200),
        nullable=False,
        comment="Nome do profissional responsável pelo registro"
    )
    
    # Avaliação e progressos
    objetivos = Column(
        Text,
        nullable=True,
        comment="Objetivos trabalhados na sessão"
    )
    
    progressos_observados = Column(
        Text,
        nullable=True,
        comment="Progressos observados"
    )
    
    dificuldades_encontradas = Column(
        Text,
        nullable=True,
        comment="Dificuldades encontradas"
    )
    
    # Encaminhamentos e orientações
    encaminhamentos = Column(
        Text,
        nullable=True,
        comment="Encaminhamentos realizados"
    )
    
    orientacoes_dadas = Column(
        Text,
        nullable=True,
        comment="Orientações fornecidas"
    )
    
    proximos_passos = Column(
        Text,
        nullable=True,
        comment="Próximos passos planejados"
    )
    
    # Participação e engajamento
    participacao_beneficiaria = Column(
        String(50),
        nullable=True,
        comment="Nível de participação (baixa, média, alta)"
    )
    
    engajamento = Column(
        String(50),
        nullable=True,
        comment="Nível de engajamento (baixo, médio, alto)"
    )
    
    # Comparecimento
    compareceu = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="A beneficiária compareceu ao atendimento?"
    )
    
    motivo_falta = Column(
        String(500),
        nullable=True,
        comment="Motivo da falta (se não compareceu)"
    )
    
    # Assinaturas
    assinatura_beneficiaria = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Beneficiária assinou a ficha?"
    )
    
    assinatura_responsavel_familiar = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Responsável familiar assinou?"
    )
    
    # Observações adicionais
    observacoes_gerais = Column(
        Text,
        nullable=True,
        comment="Observações gerais sobre o atendimento"
    )
    
    # Status
    status = Column(
        String(50),
        nullable=False,
        default='concluido',
        comment="Status do atendimento (agendado, concluido, cancelado)"
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
        back_populates="fichas_evolucao",
        lazy="select"
    )
    
    def __repr__(self):
        """Representação string do modelo."""
        return (
            f"<FichaEvolucao("
            f"id={self.id}, "
            f"beneficiaria_id={self.beneficiaria_id}, "
            f"data={self.data_evolucao.strftime('%d/%m/%Y') if self.data_evolucao else 'N/A'}, "
            f"tipo='{self.tipo_atendimento}', "
            f"responsavel='{self.responsavel}'"
            f")>"
        )
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            'id': str(self.id),
            'beneficiaria_id': str(self.beneficiaria_id),
            'data_evolucao': self.data_evolucao.isoformat() if self.data_evolucao else None,
            'tipo_atendimento': self.tipo_atendimento,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'objetivos': self.objetivos,
            'progressos_observados': self.progressos_observados,
            'dificuldades_encontradas': self.dificuldades_encontradas,
            'encaminhamentos': self.encaminhamentos,
            'orientacoes_dadas': self.orientacoes_dadas,
            'proximos_passos': self.proximos_passos,
            'participacao_beneficiaria': self.participacao_beneficiaria,
            'engajamento': self.engajamento,
            'compareceu': self.compareceu,
            'motivo_falta': self.motivo_falta,
            'assinatura_beneficiaria': self.assinatura_beneficiaria,
            'assinatura_responsavel_familiar': self.assinatura_responsavel_familiar,
            'observacoes_gerais': self.observacoes_gerais,
            'status': self.status,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }
    
    @classmethod
    def find_by_beneficiaria(cls, beneficiaria_id, limit=None):
        """Busca fichas de evolução por beneficiária."""
        query = cls.query.filter_by(beneficiaria_id=beneficiaria_id).order_by(
            cls.data_evolucao.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def find_by_periodo(cls, data_inicio, data_fim=None, beneficiaria_id=None):
        """Busca fichas por período."""
        query = cls.query.filter(cls.data_evolucao >= data_inicio)
        if data_fim:
            query = query.filter(cls.data_evolucao <= data_fim)
        if beneficiaria_id:
            query = query.filter_by(beneficiaria_id=beneficiaria_id)
        return query.order_by(cls.data_evolucao.desc()).all()
    
    @classmethod
    def find_by_responsavel(cls, responsavel):
        """Busca fichas por profissional responsável."""
        return cls.query.filter(
            cls.responsavel.ilike(f'%{responsavel}%')
        ).order_by(cls.data_evolucao.desc()).all()
    
    @classmethod
    def find_by_tipo_atendimento(cls, tipo_atendimento):
        """Busca fichas por tipo de atendimento."""
        return cls.query.filter(
            cls.tipo_atendimento.ilike(f'%{tipo_atendimento}%')
        ).order_by(cls.data_evolucao.desc()).all()
    
    @classmethod
    def get_ultimas_evolucoes(cls, beneficiaria_id, quantidade=5):
        """Obtém as últimas evoluções de uma beneficiária."""
        return cls.query.filter_by(
            beneficiaria_id=beneficiaria_id
        ).order_by(
            cls.data_evolucao.desc()
        ).limit(quantidade).all()
    
    @classmethod
    def get_estatisticas_atendimentos(cls, beneficiaria_id):
        """Obtém estatísticas de atendimentos de uma beneficiária."""
        fichas = cls.query.filter_by(beneficiaria_id=beneficiaria_id).all()
        
        total_atendimentos = len(fichas)
        comparecimentos = len([f for f in fichas if f.compareceu])
        faltas = total_atendimentos - comparecimentos
        
        return {
            'total_atendimentos': total_atendimentos,
            'comparecimentos': comparecimentos,
            'faltas': faltas,
            'percentual_comparecimento': (comparecimentos / total_atendimentos * 100) if total_atendimentos > 0 else 0,
            'ultimo_atendimento': fichas[0].data_evolucao.isoformat() if fichas else None
        }
