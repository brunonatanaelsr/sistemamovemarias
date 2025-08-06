"""
Modelo para Visão Holística da Beneficiária.

Este modelo representa a avaliação holística da situação da beneficiária,
incluindo aspectos físicos, emocionais, sociais, espirituais e familiares.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.extensions import db


class AspectosAvaliacao(Enum):
    """Aspectos avaliados na visão holística."""
    FISICO = "fisico"
    EMOCIONAL = "emocional"
    SOCIAL = "social"
    ESPIRITUAL = "espiritual"
    FAMILIAR = "familiar"
    PROFISSIONAL = "profissional"
    FINANCEIRO = "financeiro"


class NivelSituacao(Enum):
    """Nível de situação em cada aspecto."""
    CRITICO = "critico"
    PREOCUPANTE = "preocupante"
    ESTAVEL = "estavel"
    BOM = "bom"
    EXCELENTE = "excelente"


class VisaoHolistica(db.Model):
    """
    Modelo para avaliação holística da beneficiária.
    
    Representa uma avaliação completa da situação da beneficiária
    em diferentes aspectos da vida, permitindo uma visão integral
    das necessidades e potencialidades.
    """
    
    __tablename__ = 'visao_holistica'
    
    # Chave primária
    id = Column(Integer, primary_key=True)
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(Integer, ForeignKey('beneficiarias.id'), nullable=False)
    beneficiaria = relationship('Beneficiaria', back_populates='visoes_holisticas')
    
    # Dados da avaliação
    data_avaliacao = Column(DateTime, nullable=False, default=datetime.utcnow)
    profissional_responsavel = Column(String(255), nullable=False)
    
    # Aspectos físicos
    situacao_fisica = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_fisica = Column(Text)
    
    # Aspectos emocionais
    situacao_emocional = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_emocional = Column(Text)
    
    # Aspectos sociais
    situacao_social = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_social = Column(Text)
    
    # Aspectos espirituais
    situacao_espiritual = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_espiritual = Column(Text)
    
    # Aspectos familiares
    situacao_familiar = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_familiar = Column(Text)
    
    # Aspectos profissionais
    situacao_profissional = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_profissional = Column(Text)
    
    # Aspectos financeiros
    situacao_financeira = Column(SQLEnum(NivelSituacao), nullable=True)
    observacoes_financeira = Column(Text)
    
    # Avaliação geral
    pontos_fortes = Column(Text)
    areas_melhoria = Column(Text)
    objetivos_principais = Column(Text)
    observacoes_gerais = Column(Text)
    
    # Próximos passos
    proximas_acoes = Column(Text)
    data_proxima_avaliacao = Column(DateTime)
    
    # Campos de auditoria
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    criado_por = Column(String(255))
    atualizado_por = Column(String(255))
    ativo = Column(Boolean, nullable=False, default=True)
    
    def __init__(self, **kwargs):
        """Inicializar nova avaliação holística."""
        super().__init__(**kwargs)
    
    def __repr__(self):
        """Representação string do objeto."""
        return f'<VisaoHolistica {self.id} - Beneficiária {self.beneficiaria_id}>'
    
    def to_dict(self):
        """
        Converter objeto para dicionário.
        
        Returns:
            dict: Dados da avaliação holística
        """
        return {
            'id': self.id,
            'beneficiaria_id': self.beneficiaria_id,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'profissional_responsavel': self.profissional_responsavel,
            'situacao_fisica': self.situacao_fisica.value if self.situacao_fisica else None,
            'observacoes_fisica': self.observacoes_fisica,
            'situacao_emocional': self.situacao_emocional.value if self.situacao_emocional else None,
            'observacoes_emocional': self.observacoes_emocional,
            'situacao_social': self.situacao_social.value if self.situacao_social else None,
            'observacoes_social': self.observacoes_social,
            'situacao_espiritual': self.situacao_espiritual.value if self.situacao_espiritual else None,
            'observacoes_espiritual': self.observacoes_espiritual,
            'situacao_familiar': self.situacao_familiar.value if self.situacao_familiar else None,
            'observacoes_familiar': self.observacoes_familiar,
            'situacao_profissional': self.situacao_profissional.value if self.situacao_profissional else None,
            'observacoes_profissional': self.observacoes_profissional,
            'situacao_financeira': self.situacao_financeira.value if self.situacao_financeira else None,
            'observacoes_financeira': self.observacoes_financeira,
            'pontos_fortes': self.pontos_fortes,
            'areas_melhoria': self.areas_melhoria,
            'objetivos_principais': self.objetivos_principais,
            'observacoes_gerais': self.observacoes_gerais,
            'proximas_acoes': self.proximas_acoes,
            'data_proxima_avaliacao': self.data_proxima_avaliacao.isoformat() if self.data_proxima_avaliacao else None,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'ativo': self.ativo
        }
    
    def calcular_score_geral(self):
        """
        Calcular score geral da avaliação holística.
        
        Returns:
            float: Score de 0 a 100 baseado nas avaliações
        """
        scores = {
            NivelSituacao.CRITICO: 0,
            NivelSituacao.PREOCUPANTE: 25,
            NivelSituacao.ESTAVEL: 50,
            NivelSituacao.BOM: 75,
            NivelSituacao.EXCELENTE: 100
        }
        
        aspectos = [
            self.situacao_fisica,
            self.situacao_emocional,
            self.situacao_social,
            self.situacao_espiritual,
            self.situacao_familiar,
            self.situacao_profissional,
            self.situacao_financeira
        ]
        
        # Filtrar aspectos avaliados
        aspectos_avaliados = [a for a in aspectos if a is not None]
        
        if not aspectos_avaliados:
            return 0.0
        
        total_score = sum(scores[aspecto] for aspecto in aspectos_avaliados)
        return round(total_score / len(aspectos_avaliados), 2)
    
    def get_aspectos_criticos(self):
        """
        Obter aspectos em situação crítica.
        
        Returns:
            list: Lista de aspectos críticos
        """
        aspectos_criticos = []
        
        aspectos_map = {
            'fisica': self.situacao_fisica,
            'emocional': self.situacao_emocional,
            'social': self.situacao_social,
            'espiritual': self.situacao_espiritual,
            'familiar': self.situacao_familiar,
            'profissional': self.situacao_profissional,
            'financeira': self.situacao_financeira
        }
        
        for nome, situacao in aspectos_map.items():
            if situacao == NivelSituacao.CRITICO:
                aspectos_criticos.append(nome)
        
        return aspectos_criticos
    
    def get_aspectos_positivos(self):
        """
        Obter aspectos em boa situação.
        
        Returns:
            list: Lista de aspectos positivos
        """
        aspectos_positivos = []
        
        aspectos_map = {
            'fisica': self.situacao_fisica,
            'emocional': self.situacao_emocional,
            'social': self.situacao_social,
            'espiritual': self.situacao_espiritual,
            'familiar': self.situacao_familiar,
            'profissional': self.situacao_profissional,
            'financeira': self.situacao_financeira
        }
        
        for nome, situacao in aspectos_map.items():
            if situacao in [NivelSituacao.BOM, NivelSituacao.EXCELENTE]:
                aspectos_positivos.append(nome)
        
        return aspectos_positivos
    
    @classmethod
    def get_by_beneficiaria(cls, beneficiaria_id, limit=None):
        """
        Obter avaliações holísticas de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            limit (int): Limite de registros
            
        Returns:
            list: Lista de avaliações holísticas
        """
        query = cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)\
                        .order_by(cls.data_avaliacao.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @classmethod
    def get_ultima_avaliacao(cls, beneficiaria_id):
        """
        Obter última avaliação holística de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            
        Returns:
            VisaoHolistica: Última avaliação ou None
        """
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)\
                       .order_by(cls.data_avaliacao.desc())\
                       .first()
    
    def validar_dados(self):
        """
        Validar dados da avaliação holística.
        
        Returns:
            list: Lista de erros encontrados
        """
        erros = []
        
        if not self.profissional_responsavel:
            erros.append('Profissional responsável é obrigatório')
        
        if not self.data_avaliacao:
            erros.append('Data da avaliação é obrigatória')
        
        if self.data_avaliacao and self.data_avaliacao > datetime.utcnow():
            erros.append('Data da avaliação não pode ser futura')
        
        if (self.data_proxima_avaliacao and 
            self.data_avaliacao and 
            self.data_proxima_avaliacao <= self.data_avaliacao):
            erros.append('Data da próxima avaliação deve ser posterior à atual')
        
        return erros
