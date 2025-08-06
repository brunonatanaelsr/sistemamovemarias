"""
Modelo de beneficiária do sistema.

Este módulo define o modelo SQLAlchemy para as beneficiárias
atendidas pelo Instituto Move Marias.
"""

import uuid
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Date, DateTime, Integer, Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.utils.validators import validate_cpf


class Beneficiaria(db.Model):
    """
    Modelo para beneficiárias do sistema.
    
    Representa as mulheres atendidas pelo Instituto Move Marias.
    """
    
    __tablename__ = 'beneficiarias'
    
    # Campos principais
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    
    # Dados pessoais básicos
    nome_completo = Column(
        String(255),
        nullable=False,
        comment='Nome completo da beneficiária'
    )
    
    cpf = Column(
        String(14),  # Format: 000.000.000-00
        unique=True,
        nullable=False,
        index=True,
        comment='CPF da beneficiária'
    )
    
    rg = Column(
        String(20),
        comment='RG da beneficiária'
    )
    
    orgao_emissor_rg = Column(
        String(20),
        comment='Órgão emissor do RG'
    )
    
    data_emissao_rg = Column(
        Date,
        comment='Data de emissão do RG'
    )
    
    data_nascimento = Column(
        Date,
        nullable=False,
        comment='Data de nascimento da beneficiária'
    )
    
    # Dados de contato e endereço
    endereco = Column(
        Text,
        comment='Endereço completo da beneficiária'
    )
    
    bairro = Column(
        String(100),
        comment='Bairro onde reside'
    )
    
    contato1 = Column(
        String(20),
        nullable=False,
        comment='Telefone de contato principal'
    )
    
    contato2 = Column(
        String(20),
        comment='Telefone de contato secundário'
    )
    
    # Dados do programa
    nis = Column(
        String(11),
        comment='Número de Identificação Social'
    )
    
    referencia = Column(
        String(255),
        comment='Como chegou ao instituto (referência)'
    )
    
    data_inicio_instituto = Column(
        Date,
        comment='Data de início no Instituto'
    )
    
    programa_servico = Column(
        String(255),
        comment='Programa/Oficina/Serviço que participa'
    )
    
    # Status e observações
    ativo = Column(
        db.Boolean,
        default=True,
        nullable=False,
        comment='Indica se a beneficiária está ativa no sistema'
    )
    
    observacoes = Column(
        Text,
        comment='Observações gerais sobre a beneficiária'
    )
    
    # Campos de auditoria
    data_criacao = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Data e hora de criação do registro'
    )
    
    data_atualizacao = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment='Data e hora da última atualização'
    )
    
    # TODO: Adicionar campo para usuário que criou/modificou
    
    # Relacionamentos
    declaracoes_comparecimento = relationship(
        'DeclaracaoComparecimento',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    recibos_beneficio = relationship(
        'ReciboBeneficio',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    anamneses_social = relationship(
        'AnamneseSocial',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    fichas_evolucao = relationship(
        'FichaEvolucao',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    termos_consentimento = relationship(
        'TermoConsentimento',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    visoes_holisticas = relationship(
        'VisaoHolistica',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    rodas_vida = relationship(
        'RodaVida',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    planos_acao = relationship(
        'PlanoAcaoPersonalizado',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    matriculas_projetos = relationship(
        'MatriculaProjetoSocial',
        back_populates='beneficiaria',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __init__(self, nome_completo, cpf, data_nascimento, contato1, **kwargs):
        """
        Inicializar nova beneficiária.
        
        Args:
            nome_completo (str): Nome completo da beneficiária
            cpf (str): CPF da beneficiária
            data_nascimento (date): Data de nascimento
            contato1 (str): Telefone principal
            **kwargs: Outros campos opcionais
        """
        self.nome_completo = nome_completo.strip().title()
        self.cpf = self._format_cpf(cpf)
        self.data_nascimento = data_nascimento
        self.contato1 = contato1
        
        # Campos opcionais
        for field in ['rg', 'orgao_emissor_rg', 'data_emissao_rg', 'endereco', 
                      'bairro', 'contato2', 'nis', 'referencia', 
                      'data_inicio_instituto', 'programa_servico', 'observacoes']:
            if field in kwargs:
                setattr(self, field, kwargs[field])
    
    @staticmethod
    def _format_cpf(cpf):
        """
        Formatar CPF.
        
        Args:
            cpf (str): CPF sem formatação
            
        Returns:
            str: CPF formatado (000.000.000-00)
        """
        # Remover caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Validar CPF
        if not validate_cpf(cpf):
            raise ValueError('CPF inválido')
        
        # Formatar CPF
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    
    @property
    def idade(self):
        """
        Calcular idade atual da beneficiária.
        
        Returns:
            int: Idade em anos
        """
        if not self.data_nascimento:
            return None
        
        hoje = date.today()
        return relativedelta(hoje, self.data_nascimento).years
    
    @property
    def cpf_numeros(self):
        """
        Obter CPF apenas com números.
        
        Returns:
            str: CPF sem formatação
        """
        return ''.join(filter(str.isdigit, self.cpf))
    
    @property
    def paedi_numero(self):
        """
        Gerar número do PAEDI baseado no ID.
        
        Returns:
            str: Número do PAEDI formatado
        """
        # Usar os primeiros 8 caracteres do UUID
        return str(self.id).replace('-', '')[:8].upper()
    
    def get_formularios_preenchidos(self):
        """
        Obter lista de formulários preenchidos pela beneficiária.
        
        Returns:
            dict: Dicionário com contadores de formulários
        """
        return {
            'declaracoes_comparecimento': self.declaracoes_comparecimento.count(),
            'recibos_beneficio': self.recibos_beneficio.count(),
            'anamneses_social': self.anamneses_social.count(),
            'fichas_evolucao': self.fichas_evolucao.count(),
            'termos_consentimento': self.termos_consentimento.count(),
            'visoes_holisticas': self.visoes_holisticas.count(),
            'rodas_vida': self.rodas_vida.count(),
            'planos_acao': self.planos_acao.count(),
            'matriculas_projetos': self.matriculas_projetos.count()
        }
    
    def get_ultimo_atendimento(self):
        """
        Obter data do último atendimento.
        
        Returns:
            datetime: Data do último atendimento ou None
        """
        declaracoes = self.declaracoes_comparecimento.order_by(
            db.desc('data_comparecimento')
        ).first()
        
        if declaracoes:
            return declaracoes.data_comparecimento
        
        return None
    
    def is_active(self):
        """
        Verificar se a beneficiária está ativa.
        
        Returns:
            bool: True se estiver ativa, False caso contrário
        """
        return self.ativo
    
    def to_dict(self, include_relationships=False):
        """
        Converter beneficiária para dicionário.
        
        Args:
            include_relationships (bool): Se deve incluir dados dos relacionamentos
            
        Returns:
            dict: Dados da beneficiária
        """
        data = {
            'id': str(self.id),
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'rg': self.rg,
            'orgao_emissor_rg': self.orgao_emissor_rg,
            'data_emissao_rg': self.data_emissao_rg.isoformat() if self.data_emissao_rg else None,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'idade': self.idade,
            'endereco': self.endereco,
            'bairro': self.bairro,
            'contato1': self.contato1,
            'contato2': self.contato2,
            'nis': self.nis,
            'referencia': self.referencia,
            'data_inicio_instituto': self.data_inicio_instituto.isoformat() if self.data_inicio_instituto else None,
            'programa_servico': self.programa_servico,
            'ativo': self.ativo,
            'observacoes': self.observacoes,
            'paedi_numero': self.paedi_numero,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }
        
        if include_relationships:
            data.update({
                'formularios_preenchidos': self.get_formularios_preenchidos(),
                'ultimo_atendimento': self.get_ultimo_atendimento().isoformat() if self.get_ultimo_atendimento() else None
            })
        
        return data
    
    def __repr__(self):
        """Representação string da beneficiária."""
        return f'<Beneficiaria {self.nome_completo} ({self.cpf})>'
    
    @classmethod
    def find_by_cpf(cls, cpf):
        """
        Buscar beneficiária por CPF.
        
        Args:
            cpf (str): CPF da beneficiária (com ou sem formatação)
            
        Returns:
            Beneficiaria: Beneficiária encontrada ou None
        """
        cpf_formatado = cls._format_cpf(cpf)
        return cls.query.filter_by(cpf=cpf_formatado).first()
    
    @classmethod
    def find_by_id(cls, beneficiaria_id):
        """
        Buscar beneficiária por ID.
        
        Args:
            beneficiaria_id (str|UUID): ID da beneficiária
            
        Returns:
            Beneficiaria: Beneficiária encontrada ou None
        """
        if isinstance(beneficiaria_id, str):
            try:
                beneficiaria_id = uuid.UUID(beneficiaria_id)
            except ValueError:
                return None
        
        return cls.query.filter_by(id=beneficiaria_id).first()
    
    @classmethod
    def search(cls, query, active_only=True):
        """
        Buscar beneficiárias por nome ou CPF.
        
        Args:
            query (str): Termo de busca
            active_only (bool): Se deve buscar apenas beneficiárias ativas
            
        Returns:
            list: Lista de beneficiárias encontradas
        """
        filters = []
        
        # Busca por nome
        if query:
            filters.append(cls.nome_completo.ilike(f'%{query}%'))
            
            # Se o query parece um CPF, buscar por CPF também
            cpf_digits = ''.join(filter(str.isdigit, query))
            if len(cpf_digits) >= 3:
                filters.append(cls.cpf.ilike(f'%{cpf_digits}%'))
        
        base_query = cls.query
        
        if active_only:
            base_query = base_query.filter_by(ativo=True)
        
        if filters:
            from sqlalchemy import or_
            base_query = base_query.filter(or_(*filters))
        
        return base_query.order_by(cls.nome_completo).all()
    
    @classmethod
    def get_active_beneficiarias(cls):
        """
        Obter todas as beneficiárias ativas.
        
        Returns:
            list: Lista de beneficiárias ativas
        """
        return cls.query.filter_by(ativo=True).order_by(cls.nome_completo).all()
    
    @classmethod
    def get_by_programa(cls, programa):
        """
        Obter beneficiárias por programa.
        
        Args:
            programa (str): Nome do programa
            
        Returns:
            list: Lista de beneficiárias do programa
        """
        return cls.query.filter_by(programa_servico=programa, ativo=True).all()
