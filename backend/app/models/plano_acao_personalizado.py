"""
Modelo para Plano de Ação Personalizado.

Este modelo representa o plano de ação individual criado para cada
beneficiária, com objetivos, metas e ações específicas.
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
from enum import Enum
from app.extensions import db


class StatusPlano(Enum):
    """Status do plano de ação."""
    RASCUNHO = "rascunho"
    ATIVO = "ativo"
    PAUSADO = "pausado"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"


class PrioridadeAcao(Enum):
    """Prioridade da ação."""
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class StatusAcao(Enum):
    """Status da ação."""
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
    ADIADA = "adiada"


class PlanoAcaoPersonalizado(db.Model):
    """
    Modelo para plano de ação personalizado da beneficiária.
    
    Representa um plano estruturado com objetivos, metas e ações
    específicas para o desenvolvimento da beneficiária.
    """
    
    __tablename__ = 'plano_acao_personalizado'
    
    # Chave primária
    id = Column(Integer, primary_key=True)
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(Integer, ForeignKey('beneficiarias.id'), nullable=False)
    beneficiaria = relationship('Beneficiaria', back_populates='planos_acao')
    
    # Dados básicos do plano
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    objetivo_principal = Column(Text, nullable=False)
    
    # Datas
    data_inicio = Column(Date, nullable=False)
    data_fim_prevista = Column(Date, nullable=False)
    data_fim_real = Column(Date)
    
    # Status e controle
    status = Column(SQLEnum(StatusPlano), nullable=False, default=StatusPlano.RASCUNHO)
    profissional_responsavel = Column(String(255), nullable=False)
    
    # Avaliação inicial
    situacao_atual = Column(Text)
    situacao_desejada = Column(Text)
    recursos_disponiveis = Column(Text)
    obstaculos_identificados = Column(Text)
    
    # Indicadores de sucesso
    indicadores_sucesso = Column(Text)
    criterios_avaliacao = Column(Text)
    
    # Observações e notas
    observacoes = Column(Text)
    
    # Revisões e acompanhamento
    data_ultima_revisao = Column(DateTime)
    proxima_revisao = Column(DateTime)
    frequencia_revisao = Column(String(50))  # semanal, quinzenal, mensal
    
    # Relacionamento com ações
    acoes = relationship('AcaoPlano', back_populates='plano', cascade='all, delete-orphan')
    
    # Campos de auditoria
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    criado_por = Column(String(255))
    atualizado_por = Column(String(255))
    ativo = Column(Boolean, nullable=False, default=True)
    
    def __init__(self, **kwargs):
        """Inicializar novo plano de ação."""
        super().__init__(**kwargs)
    
    def __repr__(self):
        """Representação string do objeto."""
        return f'<PlanoAcao {self.id} - {self.titulo}>'
    
    def to_dict(self, include_acoes=True):
        """
        Converter objeto para dicionário.
        
        Args:
            include_acoes (bool): Se deve incluir as ações
            
        Returns:
            dict: Dados do plano de ação
        """
        data = {
            'id': self.id,
            'beneficiaria_id': self.beneficiaria_id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'objetivo_principal': self.objetivo_principal,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim_prevista': self.data_fim_prevista.isoformat() if self.data_fim_prevista else None,
            'data_fim_real': self.data_fim_real.isoformat() if self.data_fim_real else None,
            'status': self.status.value if self.status else None,
            'profissional_responsavel': self.profissional_responsavel,
            'situacao_atual': self.situacao_atual,
            'situacao_desejada': self.situacao_desejada,
            'recursos_disponiveis': self.recursos_disponiveis,
            'obstaculos_identificados': self.obstaculos_identificados,
            'indicadores_sucesso': self.indicadores_sucesso,
            'criterios_avaliacao': self.criterios_avaliacao,
            'observacoes': self.observacoes,
            'data_ultima_revisao': self.data_ultima_revisao.isoformat() if self.data_ultima_revisao else None,
            'proxima_revisao': self.proxima_revisao.isoformat() if self.proxima_revisao else None,
            'frequencia_revisao': self.frequencia_revisao,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'ativo': self.ativo
        }
        
        if include_acoes and self.acoes:
            data['acoes'] = [acao.to_dict() for acao in self.acoes if acao.ativa]
        
        return data
    
    def calcular_progresso(self):
        """
        Calcular progresso do plano baseado nas ações.
        
        Returns:
            dict: Dados de progresso
        """
        if not self.acoes:
            return {
                'total_acoes': 0,
                'acoes_concluidas': 0,
                'percentual': 0,
                'status_geral': 'Sem ações definidas'
            }
        
        acoes_ativas = [acao for acao in self.acoes if acao.ativa]
        total_acoes = len(acoes_ativas)
        acoes_concluidas = len([acao for acao in acoes_ativas if acao.status == StatusAcao.CONCLUIDA])
        
        percentual = round((acoes_concluidas / total_acoes) * 100, 2) if total_acoes > 0 else 0
        
        if percentual == 100:
            status_geral = "Concluído"
        elif percentual >= 75:
            status_geral = "Quase concluído"
        elif percentual >= 50:
            status_geral = "Em bom andamento"
        elif percentual >= 25:
            status_geral = "Em andamento"
        else:
            status_geral = "Iniciando"
        
        return {
            'total_acoes': total_acoes,
            'acoes_concluidas': acoes_concluidas,
            'percentual': percentual,
            'status_geral': status_geral
        }
    
    def get_acoes_atrasadas(self):
        """
        Obter ações em atraso.
        
        Returns:
            list: Lista de ações atrasadas
        """
        hoje = datetime.utcnow().date()
        acoes_atrasadas = []
        
        for acao in self.acoes:
            if (acao.ativa and 
                acao.data_prevista and 
                acao.data_prevista < hoje and 
                acao.status not in [StatusAcao.CONCLUIDA, StatusAcao.CANCELADA]):
                acoes_atrasadas.append(acao)
        
        return acoes_atrasadas
    
    def get_proximas_acoes(self, dias=7):
        """
        Obter ações dos próximos dias.
        
        Args:
            dias (int): Número de dias para buscar
            
        Returns:
            list: Lista de próximas ações
        """
        hoje = datetime.utcnow().date()
        data_limite = hoje + timedelta(days=dias)
        proximas_acoes = []
        
        for acao in self.acoes:
            if (acao.ativa and 
                acao.data_prevista and 
                hoje <= acao.data_prevista <= data_limite and 
                acao.status == StatusAcao.PENDENTE):
                proximas_acoes.append(acao)
        
        return sorted(proximas_acoes, key=lambda x: x.data_prevista)
    
    def ativar_plano(self):
        """Ativar o plano de ação."""
        self.status = StatusPlano.ATIVO
        if not self.data_ultima_revisao:
            self.data_ultima_revisao = datetime.utcnow()
        self.calcular_proxima_revisao()
    
    def concluir_plano(self):
        """Concluir o plano de ação."""
        self.status = StatusPlano.CONCLUIDO
        self.data_fim_real = datetime.utcnow().date()
    
    def calcular_proxima_revisao(self):
        """Calcular data da próxima revisão."""
        if not self.frequencia_revisao:
            return
        
        hoje = datetime.utcnow()
        
        if self.frequencia_revisao == 'semanal':
            self.proxima_revisao = hoje + timedelta(weeks=1)
        elif self.frequencia_revisao == 'quinzenal':
            self.proxima_revisao = hoje + timedelta(weeks=2)
        elif self.frequencia_revisao == 'mensal':
            self.proxima_revisao = hoje + timedelta(days=30)
    
    @classmethod
    def get_by_beneficiaria(cls, beneficiaria_id, status=None):
        """
        Obter planos de ação de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            status (StatusPlano): Filtro por status
            
        Returns:
            list: Lista de planos de ação
        """
        query = cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(cls.data_inicio.desc()).all()
    
    @classmethod
    def get_planos_para_revisao(cls, dias=7):
        """
        Obter planos que precisam de revisão.
        
        Args:
            dias (int): Dias de antecedência
            
        Returns:
            list: Planos para revisão
        """
        data_limite = datetime.utcnow() + timedelta(days=dias)
        
        return cls.query.filter(
            cls.status == StatusPlano.ATIVO,
            cls.proxima_revisao <= data_limite,
            cls.ativo == True
        ).all()
    
    def validar_dados(self):
        """
        Validar dados do plano de ação.
        
        Returns:
            list: Lista de erros encontrados
        """
        erros = []
        
        if not self.titulo:
            erros.append('Título é obrigatório')
        
        if not self.objetivo_principal:
            erros.append('Objetivo principal é obrigatório')
        
        if not self.profissional_responsavel:
            erros.append('Profissional responsável é obrigatório')
        
        if not self.data_inicio:
            erros.append('Data de início é obrigatória')
        
        if not self.data_fim_prevista:
            erros.append('Data de fim prevista é obrigatória')
        
        if (self.data_inicio and self.data_fim_prevista and 
            self.data_fim_prevista <= self.data_inicio):
            erros.append('Data de fim deve ser posterior à data de início')
        
        if (self.data_fim_real and self.data_inicio and 
            self.data_fim_real < self.data_inicio):
            erros.append('Data de fim real não pode ser anterior à data de início')
        
        return erros


class AcaoPlano(db.Model):
    """
    Modelo para ações específicas do plano.
    
    Representa uma ação individual dentro do plano de ação,
    com responsável, prazo e status próprios.
    """
    
    __tablename__ = 'acao_plano'
    
    # Chave primária
    id = Column(Integer, primary_key=True)
    
    # Relacionamento com plano
    plano_id = Column(Integer, ForeignKey('plano_acao_personalizado.id'), nullable=False)
    plano = relationship('PlanoAcaoPersonalizado', back_populates='acoes')
    
    # Dados da ação
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    responsavel = Column(String(255))  # Pode ser a beneficiária ou profissional
    
    # Datas e prazos
    data_prevista = Column(Date)
    data_realizada = Column(Date)
    
    # Status e prioridade
    status = Column(SQLEnum(StatusAcao), nullable=False, default=StatusAcao.PENDENTE)
    prioridade = Column(SQLEnum(PrioridadeAcao), default=PrioridadeAcao.MEDIA)
    
    # Resultados
    resultado_esperado = Column(Text)
    resultado_obtido = Column(Text)
    observacoes = Column(Text)
    
    # Controle
    ordem = Column(Integer, default=0)  # Ordem de execução
    
    # Campos de auditoria
    criada_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizada_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    ativa = Column(Boolean, nullable=False, default=True)
    
    def __init__(self, **kwargs):
        """Inicializar nova ação."""
        super().__init__(**kwargs)
    
    def __repr__(self):
        """Representação string do objeto."""
        return f'<AcaoPlano {self.id} - {self.titulo}>'
    
    def to_dict(self):
        """
        Converter objeto para dicionário.
        
        Returns:
            dict: Dados da ação
        """
        return {
            'id': self.id,
            'plano_id': self.plano_id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'data_prevista': self.data_prevista.isoformat() if self.data_prevista else None,
            'data_realizada': self.data_realizada.isoformat() if self.data_realizada else None,
            'status': self.status.value if self.status else None,
            'prioridade': self.prioridade.value if self.prioridade else None,
            'resultado_esperado': self.resultado_esperado,
            'resultado_obtido': self.resultado_obtido,
            'observacoes': self.observacoes,
            'ordem': self.ordem,
            'criada_em': self.criada_em.isoformat() if self.criada_em else None,
            'atualizada_em': self.atualizada_em.isoformat() if self.atualizada_em else None,
            'ativa': self.ativa
        }
    
    def concluir_acao(self, resultado_obtido=None):
        """
        Concluir a ação.
        
        Args:
            resultado_obtido (str): Resultado obtido
        """
        self.status = StatusAcao.CONCLUIDA
        self.data_realizada = datetime.utcnow().date()
        if resultado_obtido:
            self.resultado_obtido = resultado_obtido
    
    def verificar_atraso(self):
        """
        Verificar se a ação está em atraso.
        
        Returns:
            bool: True se estiver em atraso
        """
        hoje = datetime.utcnow().date()
        return (self.data_prevista and 
                self.data_prevista < hoje and 
                self.status not in [StatusAcao.CONCLUIDA, StatusAcao.CANCELADA])
    
    def dias_atraso(self):
        """
        Calcular dias de atraso.
        
        Returns:
            int: Número de dias em atraso (0 se não estiver atrasada)
        """
        if not self.verificar_atraso():
            return 0
        
        hoje = datetime.utcnow().date()
        return (hoje - self.data_prevista).days
