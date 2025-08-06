"""
Modelo para Matrícula em Projetos Sociais.

Este modelo representa a participação da beneficiária em projetos
sociais, cursos, oficinas e outras atividades oferecidas pela organização.
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Date, Float
from sqlalchemy.orm import relationship
from enum import Enum
from app.extensions import db


class TipoProjeto(Enum):
    """Tipos de projetos sociais."""
    CURSO_PROFISSIONALIZANTE = "curso_profissionalizante"
    OFICINA_ARTESANATO = "oficina_artesanato"
    GRUPO_TERAPEUTICO = "grupo_terapeutico"
    ATIVIDADE_ESPORTIVA = "atividade_esportiva"
    CURSO_ALFABETIZACAO = "curso_alfabetizacao"
    CAPACITACAO_DIGITAL = "capacitacao_digital"
    GRUPO_MULHERES = "grupo_mulheres"
    ATIVIDADE_CULTURAL = "atividade_cultural"
    PROJETO_GERACAORENDA = "projeto_geracao_renda"
    OUTRO = "outro"


class StatusMatricula(Enum):
    """Status da matrícula no projeto."""
    INSCRITA = "inscrita"
    MATRICULADA = "matriculada"
    ATIVA = "ativa"
    CONCLUIDA = "concluida"
    DESISTENTE = "desistente"
    TRANSFERIDA = "transferida"
    SUSPENSA = "suspensa"
    CANCELADA = "cancelada"


class TipoFrequencia(Enum):
    """Tipos de frequência das atividades."""
    DIARIA = "diaria"
    SEMANAL = "semanal"
    QUINZENAL = "quinzenal"
    MENSAL = "mensal"
    INTENSIVA = "intensiva"
    LIVRE = "livre"


class MatriculaProjetoSocial(db.Model):
    """
    Modelo para matrícula da beneficiária em projetos sociais.
    
    Controla a participação da beneficiária em diversos projetos,
    cursos e atividades oferecidas pela organização.
    """
    
    __tablename__ = 'matricula_projeto_social'
    
    # Chave primária
    id = Column(Integer, primary_key=True)
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(Integer, ForeignKey('beneficiarias.id'), nullable=False)
    beneficiaria = relationship('Beneficiaria', back_populates='matriculas_projetos')
    
    # Dados do projeto
    nome_projeto = Column(String(255), nullable=False)
    tipo_projeto = Column(SQLEnum(TipoProjeto), nullable=False)
    descricao_projeto = Column(Text)
    objetivo_projeto = Column(Text)
    
    # Dados da matrícula
    data_inscricao = Column(Date, nullable=False, default=date.today)
    data_matricula = Column(Date)
    status_matricula = Column(SQLEnum(StatusMatricula), nullable=False, default=StatusMatricula.INSCRITA)
    
    # Período do projeto
    data_inicio = Column(Date)
    data_fim_prevista = Column(Date)
    data_fim_real = Column(Date)
    
    # Organização da atividade
    carga_horaria_total = Column(Integer)  # em horas
    frequencia = Column(SQLEnum(TipoFrequencia))
    dias_semana = Column(String(100))  # Ex: "Segunda, Quarta, Sexta"
    horario = Column(String(100))  # Ex: "14:00 às 16:00"
    local = Column(String(255))
    
    # Responsáveis
    instrutor_responsavel = Column(String(255))
    coordenador_projeto = Column(String(255))
    
    # Requisitos e documentação
    requisitos_ingresso = Column(Text)
    documentos_necessarios = Column(Text)
    documentos_entregues = Column(Text)
    
    # Acompanhamento
    objetivos_pessoais = Column(Text)  # Objetivos da beneficiária
    expectativas = Column(Text)
    motivacao = Column(Text)
    
    # Avaliação e resultados
    avaliacao_inicial = Column(Text)
    avaliacao_intermediaria = Column(Text)
    avaliacao_final = Column(Text)
    nota_final = Column(Float)  # 0-10
    certificado_emitido = Column(Boolean, default=False)
    data_certificado = Column(Date)
    
    # Frequência e participação
    total_faltas = Column(Integer, default=0)
    percentual_frequencia = Column(Float)  # 0-100
    participacao_atividades = Column(Text)
    
    # Observações e feedback
    observacoes_instrutor = Column(Text)
    observacoes_coordenacao = Column(Text)
    feedback_beneficiaria = Column(Text)
    sugestoes_melhoria = Column(Text)
    
    # Motivo de saída (se aplicável)
    motivo_desistencia = Column(Text)
    data_desistencia = Column(Date)
    
    # Encaminhamentos
    encaminhamentos_posteriores = Column(Text)
    projetos_sugeridos = Column(Text)
    
    # Campos de auditoria
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    criado_por = Column(String(255))
    atualizado_por = Column(String(255))
    ativo = Column(Boolean, nullable=False, default=True)
    
    def __init__(self, **kwargs):
        """Inicializar nova matrícula."""
        super().__init__(**kwargs)
    
    def __repr__(self):
        """Representação string do objeto."""
        return f'<MatriculaProjeto {self.id} - {self.nome_projeto}>'
    
    def to_dict(self):
        """
        Converter objeto para dicionário.
        
        Returns:
            dict: Dados da matrícula
        """
        return {
            'id': self.id,
            'beneficiaria_id': self.beneficiaria_id,
            'nome_projeto': self.nome_projeto,
            'tipo_projeto': self.tipo_projeto.value if self.tipo_projeto else None,
            'descricao_projeto': self.descricao_projeto,
            'objetivo_projeto': self.objetivo_projeto,
            'data_inscricao': self.data_inscricao.isoformat() if self.data_inscricao else None,
            'data_matricula': self.data_matricula.isoformat() if self.data_matricula else None,
            'status_matricula': self.status_matricula.value if self.status_matricula else None,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim_prevista': self.data_fim_prevista.isoformat() if self.data_fim_prevista else None,
            'data_fim_real': self.data_fim_real.isoformat() if self.data_fim_real else None,
            'carga_horaria_total': self.carga_horaria_total,
            'frequencia': self.frequencia.value if self.frequencia else None,
            'dias_semana': self.dias_semana,
            'horario': self.horario,
            'local': self.local,
            'instrutor_responsavel': self.instrutor_responsavel,
            'coordenador_projeto': self.coordenador_projeto,
            'requisitos_ingresso': self.requisitos_ingresso,
            'documentos_necessarios': self.documentos_necessarios,
            'documentos_entregues': self.documentos_entregues,
            'objetivos_pessoais': self.objetivos_pessoais,
            'expectativas': self.expectativas,
            'motivacao': self.motivacao,
            'avaliacao_inicial': self.avaliacao_inicial,
            'avaliacao_intermediaria': self.avaliacao_intermediaria,
            'avaliacao_final': self.avaliacao_final,
            'nota_final': self.nota_final,
            'certificado_emitido': self.certificado_emitido,
            'data_certificado': self.data_certificado.isoformat() if self.data_certificado else None,
            'total_faltas': self.total_faltas,
            'percentual_frequencia': self.percentual_frequencia,
            'participacao_atividades': self.participacao_atividades,
            'observacoes_instrutor': self.observacoes_instrutor,
            'observacoes_coordenacao': self.observacoes_coordenacao,
            'feedback_beneficiaria': self.feedback_beneficiaria,
            'sugestoes_melhoria': self.sugestoes_melhoria,
            'motivo_desistencia': self.motivo_desistencia,
            'data_desistencia': self.data_desistencia.isoformat() if self.data_desistencia else None,
            'encaminhamentos_posteriores': self.encaminhamentos_posteriores,
            'projetos_sugeridos': self.projetos_sugeridos,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'ativo': self.ativo
        }
    
    def calcular_dias_projeto(self):
        """
        Calcular número de dias do projeto.
        
        Returns:
            int: Número de dias entre início e fim
        """
        if not self.data_inicio:
            return 0
        
        data_fim = self.data_fim_real or self.data_fim_prevista
        if not data_fim:
            return 0
        
        return (data_fim - self.data_inicio).days
    
    def calcular_progresso(self):
        """
        Calcular progresso do projeto baseado nas datas.
        
        Returns:
            dict: Dados de progresso
        """
        if not self.data_inicio or not self.data_fim_prevista:
            return {
                'percentual': 0,
                'dias_decorridos': 0,
                'dias_restantes': 0,
                'status': 'Não iniciado'
            }
        
        hoje = date.today()
        dias_totais = (self.data_fim_prevista - self.data_inicio).days
        
        if hoje < self.data_inicio:
            return {
                'percentual': 0,
                'dias_decorridos': 0,
                'dias_restantes': (self.data_inicio - hoje).days,
                'status': 'Aguardando início'
            }
        
        if self.data_fim_real:
            return {
                'percentual': 100,
                'dias_decorridos': (self.data_fim_real - self.data_inicio).days,
                'dias_restantes': 0,
                'status': 'Finalizado'
            }
        
        dias_decorridos = (hoje - self.data_inicio).days
        dias_restantes = max(0, (self.data_fim_prevista - hoje).days)
        
        percentual = min(100, round((dias_decorridos / dias_totais) * 100, 2)) if dias_totais > 0 else 0
        
        if hoje > self.data_fim_prevista:
            status = 'Em atraso'
        elif percentual >= 90:
            status = 'Finalizando'
        elif percentual >= 50:
            status = 'Em andamento'
        else:
            status = 'Iniciando'
        
        return {
            'percentual': percentual,
            'dias_decorridos': dias_decorridos,
            'dias_restantes': dias_restantes,
            'status': status
        }
    
    def matricular_beneficiaria(self):
        """Confirmar matrícula da beneficiária."""
        self.status_matricula = StatusMatricula.MATRICULADA
        self.data_matricula = date.today()
    
    def ativar_participacao(self):
        """Ativar participação no projeto."""
        self.status_matricula = StatusMatricula.ATIVA
        if not self.data_inicio:
            self.data_inicio = date.today()
    
    def concluir_projeto(self, nota_final=None, emitir_certificado=False):
        """
        Concluir participação no projeto.
        
        Args:
            nota_final (float): Nota final da beneficiária
            emitir_certificado (bool): Se deve emitir certificado
        """
        self.status_matricula = StatusMatricula.CONCLUIDA
        self.data_fim_real = date.today()
        
        if nota_final is not None:
            self.nota_final = nota_final
        
        if emitir_certificado:
            self.certificado_emitido = True
            self.data_certificado = date.today()
    
    def registrar_desistencia(self, motivo):
        """
        Registrar desistência da beneficiária.
        
        Args:
            motivo (str): Motivo da desistência
        """
        self.status_matricula = StatusMatricula.DESISTENTE
        self.data_desistencia = date.today()
        self.motivo_desistencia = motivo
    
    def calcular_percentual_frequencia(self, aulas_dadas=None):
        """
        Calcular percentual de frequência.
        
        Args:
            aulas_dadas (int): Total de aulas dadas (opcional)
        """
        if aulas_dadas and self.total_faltas is not None:
            aulas_frequentadas = aulas_dadas - self.total_faltas
            self.percentual_frequencia = round((aulas_frequentadas / aulas_dadas) * 100, 2)
    
    def verificar_situacao_frequencia(self, limite_minimo=75.0):
        """
        Verificar situação da frequência.
        
        Args:
            limite_minimo (float): Percentual mínimo de frequência
            
        Returns:
            dict: Situação da frequência
        """
        if self.percentual_frequencia is None:
            return {
                'situacao': 'Não calculada',
                'aprovada': None,
                'observacao': 'Frequência não foi calculada'
            }
        
        aprovada = self.percentual_frequencia >= limite_minimo
        
        if aprovada:
            situacao = 'Aprovada'
            observacao = f'Frequência de {self.percentual_frequencia}% está acima do mínimo'
        else:
            situacao = 'Reprovada'
            observacao = f'Frequência de {self.percentual_frequencia}% está abaixo do mínimo de {limite_minimo}%'
        
        return {
            'situacao': situacao,
            'aprovada': aprovada,
            'observacao': observacao,
            'percentual': self.percentual_frequencia
        }
    
    @classmethod
    def get_by_beneficiaria(cls, beneficiaria_id, status=None):
        """
        Obter matrículas de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            status (StatusMatricula): Filtro por status
            
        Returns:
            list: Lista de matrículas
        """
        query = cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)
        
        if status:
            query = query.filter_by(status_matricula=status)
        
        return query.order_by(cls.data_inscricao.desc()).all()
    
    @classmethod
    def get_matriculas_ativas(cls):
        """
        Obter todas as matrículas ativas.
        
        Returns:
            list: Lista de matrículas ativas
        """
        return cls.query.filter_by(
            status_matricula=StatusMatricula.ATIVA,
            ativo=True
        ).all()
    
    @classmethod
    def get_por_tipo_projeto(cls, tipo_projeto):
        """
        Obter matrículas por tipo de projeto.
        
        Args:
            tipo_projeto (TipoProjeto): Tipo do projeto
            
        Returns:
            list: Lista de matrículas
        """
        return cls.query.filter_by(
            tipo_projeto=tipo_projeto,
            ativo=True
        ).order_by(cls.data_inscricao.desc()).all()
    
    @classmethod
    def get_estatisticas_projetos(cls):
        """
        Obter estatísticas dos projetos.
        
        Returns:
            dict: Estatísticas dos projetos
        """
        from sqlalchemy import func
        
        # Total de matrículas por status
        stats_status = db.session.query(
            cls.status_matricula,
            func.count(cls.id)
        ).filter(cls.ativo == True).group_by(cls.status_matricula).all()
        
        # Total por tipo de projeto
        stats_tipo = db.session.query(
            cls.tipo_projeto,
            func.count(cls.id)
        ).filter(cls.ativo == True).group_by(cls.tipo_projeto).all()
        
        # Matrículas ativas
        ativas = cls.query.filter_by(
            status_matricula=StatusMatricula.ATIVA,
            ativo=True
        ).count()
        
        # Certificados emitidos
        certificados = cls.query.filter_by(
            certificado_emitido=True,
            ativo=True
        ).count()
        
        return {
            'total_matriculas': cls.query.filter_by(ativo=True).count(),
            'matriculas_ativas': ativas,
            'certificados_emitidos': certificados,
            'por_status': {status.value: count for status, count in stats_status},
            'por_tipo': {tipo.value: count for tipo, count in stats_tipo}
        }
    
    def validar_dados(self):
        """
        Validar dados da matrícula.
        
        Returns:
            list: Lista de erros encontrados
        """
        erros = []
        
        if not self.nome_projeto:
            erros.append('Nome do projeto é obrigatório')
        
        if not self.tipo_projeto:
            erros.append('Tipo do projeto é obrigatório')
        
        if not self.data_inscricao:
            erros.append('Data de inscrição é obrigatória')
        
        if (self.data_matricula and self.data_inscricao and 
            self.data_matricula < self.data_inscricao):
            erros.append('Data de matrícula não pode ser anterior à inscrição')
        
        if (self.data_inicio and self.data_fim_prevista and 
            self.data_fim_prevista <= self.data_inicio):
            erros.append('Data de fim deve ser posterior à data de início')
        
        if (self.data_fim_real and self.data_inicio and 
            self.data_fim_real < self.data_inicio):
            erros.append('Data de fim real não pode ser anterior ao início')
        
        if self.nota_final is not None and (self.nota_final < 0 or self.nota_final > 10):
            erros.append('Nota final deve estar entre 0 e 10')
        
        if (self.percentual_frequencia is not None and 
            (self.percentual_frequencia < 0 or self.percentual_frequencia > 100)):
            erros.append('Percentual de frequência deve estar entre 0 e 100')
        
        if self.total_faltas is not None and self.total_faltas < 0:
            erros.append('Total de faltas não pode ser negativo')
        
        return erros
